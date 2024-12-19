"""
This script does the following tasks:
1. It creates an AI Search index (or re-creates it if it already exists) based on a JSON configuration file.
2. It uploads multiple Excel files from an Azure Blob Storage container to an Azure Search index in the correct format.

Usage steps:
1. Upload the files you want to use for your knowledge base to the Azure Blob Storage container, in our case 'knowledge-base'
2. Run this script

! Make sure to run this script in your terminal from the `/scripts/` directory, or it won't find the JSON-configuration file. 
! You can also just move the JSON configuration file here, and update the path in the script.

If everything went well, you should see the index created and the documents uploaded to the Azure Search service..
Whenever you update the knowledge base, simply run this script again, it will re-create the index and use/upload the new data.
"""


import io
import json
import pandas as pd
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

load_dotenv()  # Ensure this is called before accessing environment variables

# Load environment variables from the secrets.toml
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_KNOWLEDGE_BASE_CONTAINER_NAME = os.getenv("AZURE_KNOWLEDGE_BASE_CONTAINER_NAME")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

if not AZURE_STORAGE_CONNECTION_STRING:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set. Check your environment variables.")


def load_index_configuration(file_path):
    """
    Load the search index configuration from a JSON file.

    Args:
        file_path (str): Path to the configuration JSON file.

    Returns:
        dict: The index configuration.
    """
    with open(file_path, 'r') as config_file:
        return json.load(config_file)


def ensure_index_exists(index_client, index_name, config_path):
    """
    Ensure the Azure Cognitive Search index exists by creating it if necessary.

    Args:
        index_client (SearchIndexClient): The Azure Search Index client.
        index_name (str): The name of the search index.
        config_path (str): Path to the index configuration file.

    Returns:
        None
    """
    try:
        if index_client.get_index(index_name):
            print(f"Index '{index_name}' exists. Deleting and re-creating it.")
            index_client.delete_index(index_name)
    except Exception as e:
        print(f"Index '{index_name}' does not exist or error occurred: {e}")

    # Load and create the index from configuration
    index_config = load_index_configuration(config_path)
    index = SearchIndex(**index_config)
    index_client.create_index(index)
    print(f"Index '{index_name}' has been created.")


def get_next_id(client):
    """
    Retrieve the current highest ID from the Azure Cognitive Search index and calculate the next ID.

    Args:
        client (SearchClient): The Azure Search client.

    Returns:
        int: The next ID to use.
    """
    highest_id = 0
    try:
        # Query the index to find the highest current ID
        results = client.search(search_text="*", select="id", top=1)
        for result in results:
            highest_id = int(result.get("id", 0))
            break
    except Exception as e:
        print(f"Error retrieving the highest ID: {e}")

    return highest_id + 1


def excel_to_json(blob_data, start_id):
    """
    Convert Excel file data to JSON objects.

    Args:
        blob_data (bytes): The Excel file content as bytes.
        start_id (int): The starting ID for the JSON objects.

    Returns:
        list: A list of JSON objects formatted for the Azure Search index.
    """
    
    # Wrap blob_data in BytesIO to read it as a file-like object
    excel_file = io.BytesIO(blob_data)
    df = pd.read_excel(excel_file, sheet_name=None)
    sheet = None
    
    # Check for specific sheets
    if "Tasks" in df:
        sheet = df["Tasks"]
    elif "Sheet1" in df:
        sheet = df["Sheet1"]
    else:
        print("No valid sheet ('Tasks' or 'Sheet1') found. Skipping this file.")
        return []

    # Ensure numeric fields are cast to integers
    numeric_fields = ["MinDays", "RealDays", "MaxDays", "EstimatedDays", "EstimatedPrice"]
    for field in numeric_fields:
        if field in sheet.columns:
            sheet[field] = (
                sheet[field]
                .fillna(0)
                .apply(lambda x: int(float(str(x).strip('%')) if isinstance(x, str) and x.endswith('%') else x))
            )    
    
    # Ensure the "contingency" field is always a string
    if "Contingency" in sheet.columns:
        sheet["Contingency"] = sheet["Contingency"].fillna("0").astype(str)
    
    # Ensure all fields are cast to strings if needed
    string_fields = ["Task", "MSCW", "Area", "Module", "Feature", "Profile", "PotentialIssues"]
    for field in string_fields:
        if field in sheet.columns:
            sheet[field] = sheet[field].fillna("").astype(str)


    # Convert DataFrame rows to JSON objects
    documents = []
    current_id = start_id
    for _, row in sheet.iterrows():
        document = {
            "id": str(current_id),  # ID must always be a string
            "Task": row.get("Task", ""),
            "MSCW": row.get("MSCW", ""),
            "Area": row.get("Area", ""),
            "Module": row.get("Module", ""),
            "Feature": row.get("Feature", ""),
            "Profile": row.get("Profile", ""),
            "MinDays": int(row.get("MinDays", 0)),
            "RealDays": int(row.get("RealDays", 0)),
            "MaxDays": int(row.get("MaxDays", 0)),
            "Contingency": row.get("Contingency", "0"),  # String field
            "EstimatedDays": int(row.get("EstimatedDays", 0)),
            "EstimatedPrice": float(row.get("EstimatedPrice", 0)),  # Ensure float for Edm.Double
            "PotentialIssues": row.get("PotentialIssues", ""),
        }
        documents.append(document)
        current_id += 1

    return documents


def upload_tasks_from_blob_storage():
    """
    Upload tasks from Excel files in an Azure Blob Storage container to Azure Cognitive Search.

    Returns:
        None
    """
    # Create BlobServiceClient to connect to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_KNOWLEDGE_BASE_CONTAINER_NAME)

    # Create a SearchIndexClient for Azure Cognitive Search
    index_client = SearchIndexClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
    )

    # Create a SearchClient for Azure Cognitive Search
    client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
    )
    
    # Ensure the search index exists
    config_path = r"../documents/Azure/AI Search/search_index_configuration.json"
    ensure_index_exists(index_client, AZURE_SEARCH_INDEX_NAME, config_path)
    
    # Get the starting ID
    next_id = get_next_id(client)

    # List and process all Excel blobs in the container
    all_documents = []  # Combine documents from all Excel files
    for blob in container_client.list_blobs():
        if blob.name.endswith(".xlsx"):  # Process only Excel files
            print(f"Processing Excel file: {blob.name}")

            # Download the blob content
            blob_client = container_client.get_blob_client(blob)
            blob_data = blob_client.download_blob().readall()

            # Convert Excel content to JSON objects
            documents = excel_to_json(blob_data, next_id)
            all_documents.extend(documents)

            # Increment the ID for the next file's data
            next_id += len(documents)

    # Upload all documents to the search index
    if all_documents:
        result = client.upload_documents(all_documents)
        print(f"Successfully uploaded {len(all_documents)} documents: {result}")
    else:
        print("No Excel files found or no data to upload.")

    print("All Excel files have been processed and uploaded.")


# Execute the upload
upload_tasks_from_blob_storage()
