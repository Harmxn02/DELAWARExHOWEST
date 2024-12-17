"""
This script uploads multiple Excel files
from an Azure Blob Storage container
to an Azure Cognitive Search index.
"""


import io
import json
import pandas as pd
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import re
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
    
    # Load the Excel file into a DataFrame
    df = pd.read_excel(excel_file)

    # Convert DataFrame rows to JSON objects
    documents = []
    current_id = start_id
    for _, row in df.iterrows():
        document = {
            "id": str(current_id),
            "Task": row.get("Task", ""),
            "MSCW": row.get("MSCW", ""),
            "Area": row.get("Area", ""),
            "Module": row.get("Module", ""),
            "Feature": row.get("Feature", ""),
            "Profile": row.get("Profile", ""),
            "MinDays": row.get("MinDays", 0),
            "RealDays": row.get("RealDays", 0),
            "MaxDays": row.get("MaxDays", 0),
            "Contingency": row.get("Contingency", 0),
            "EstimatedDays": row.get("EstimatedDays", 0),
            "EstimatedPrice": row.get("EstimatedPrice", 0),
            "PotentialIssues": ", ".join(row["potential_issues"]) if isinstance(row.get("potential_issues"), list) else "",
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

    # Create a SearchClient for Azure Cognitive Search
    client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
    )
    
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
