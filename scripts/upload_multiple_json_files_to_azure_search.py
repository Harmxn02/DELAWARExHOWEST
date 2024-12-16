import json
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import re
import os

load_dotenv()  # Ensure this is called before accessing environment variables

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not connection_string:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set. Check your environment variables.")
else:
    print(f"Connection string loaded: {connection_string[:20]}...")  # Prints first 20 characters for verification

# Load environment variables from the secrets.toml
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_KNOWLEDGE_BASE_CONTAINER_NAME = os.getenv("AZURE_KNOWLEDGE_BASE_CONTAINER_NAME")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

def sanitize_key(key):
    """
    Sanitize the document key to meet Azure Cognitive Search requirements.

    Args:
        key (str): The original document key.

    Returns:
        str: A sanitized version of the key.
    """
    sanitized = re.sub(r'[^a-zA-Z0-9_\-]', '_', key)
    return sanitized


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
        results = client.search(search_text="*", select="id", orderby="id desc", top=1)
        for result in results:
            highest_id = int(result["id"])
            break
    except Exception as e:
        print(f"Error retrieving the highest ID: {e}")

    return highest_id + 1


def upload_tasks_from_blob_storage():
    """
    Upload tasks from JSON files in an Azure Blob Storage container to Azure Cognitive Search.

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

    # List and process all JSON blobs in the container
    for blob in container_client.list_blobs():
        if blob.name.endswith(".json"):  # Process only JSON files
            print(f"Processing blob: {blob.name}")

            # Download the blob content
            blob_client = container_client.get_blob_client(blob)
            blob_data = blob_client.download_blob().readall()
            project_data = json.loads(blob_data)

            # Parse and format tasks for uploading
            documents = []
            for task in project_data:
                sanitized_task = sanitize_key(task["Task"])
                document = {
                    "id": str(next_id),  # Use auto-incremented ID
                    "Task": sanitized_task,
                    "MSCW": task["MSCW"],
                    "Area": task["Area"],
                    "Module": task["Module"],
                    "Feature": task["Feature"],
                    "Profile": task["Profile"],
                    "MinDays": task["MinDays"],
                    "RealDays": task["RealDays"],
                    "MaxDays": task["MaxDays"],
                    "Contingency": task["Contingency"],
                    "EstimatedDays": task["EstimatedDays"],
                    "EstimatedPrice": task["EstimatedPrice"],
                    "PotentialIssues": ", ".join(task.get("potential_issues", [])),  # Converting list to string
                }
                documents.append(document)
                next_id += 1    # Increment the ID for the next document

            # Upload the documents to the search index
            result = client.upload_documents(documents)
            print(f"Successfully uploaded documents from {blob.name}: {result}")

    print("All blobs have been uploaded.")

# Execute the upload
upload_tasks_from_blob_storage()
