import json
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
import re
from dotenv import load_dotenv

load_dotenv()


def sanitize_key(key):
    """
    Sanitize the document key to meet Azure Cognitive Search requirements.

    Args:
        key (str): The original document key.

    Returns:
        str: A sanitized version of the key.
    """
    # Replace all invalid characters with underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_\-]', '_', key)
    return sanitized



def upload_tasks_from_folder(folder_path, endpoint, api_key, index_name):
    """
    Upload tasks from all JSON files in a folder to Azure Cognitive Search.

    Args:
        folder_path (str): The path to the folder containing the JSON files.
        endpoint (str): The endpoint URL for the Azure Cognitive Search service.
        api_key (str): The API key for accessing the Azure Cognitive Search service.
        index_name (str): The name of the index to upload the data to.

    Returns:
        None
    """
    # Create a SearchClient
    client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(api_key))

    # Loop through all JSON files in the specified folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):  # Ensure we're only processing JSON files
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_path}")
            
            # Open the JSON file and load its data
            with open(file_path, 'r') as f:
                project_data = json.load(f)
                
                # Parse and format tasks for uploading
                documents = []
                for task in project_data:
                    sanitized_task = sanitize_key(task["Task"])
                    document = {
                        "Task": sanitized_task, # Removing all symbols
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
                        "PotentialIssues": ", ".join(task["potential_issues"]),  # Converting list to string
                    }
                    documents.append(document)

                # Upload the documents to the search index
                result = client.upload_documents(documents)
                print(f"Successfully uploaded documents from {file_name}: {result}")
    
    print("All files have been uploaded.")

# Example Usage:
folder_path = "./app/export/fake_data_json/"  # Path to the folder containing your JSON files

# Azure configuration
endpoint = str(os.getenv("AZURE_SEARCH_ENDPOINT"))
api_key = str(os.getenv("AZURE_SEARCH_API_KEY"))
index_name = str(os.getenv("AZURE_SEARCH_INDEX_NAME"))

# Upload tasks from all JSON files in the folder to Azure Cognitive Search
upload_tasks_from_folder(folder_path, endpoint, api_key, index_name)
