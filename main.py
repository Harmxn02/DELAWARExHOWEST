import requests
import time
import config

import tkinter as tk
from tkinter import filedialog, messagebox

from azure.storage.blob import BlobServiceClient, ContentSettings
import os


def upload_pdf_to_azure(file_path):
    try:
        # Initialize the BlobServiceClient with the connection string
        blob_service_client = BlobServiceClient.from_connection_string(config.AZURE_STORAGE_CONNECTION_STRING)
        
        # Get a client for the container
        container_client = blob_service_client.get_container_client(config.AZURE_CONTAINER_NAME)
        
        # Ensure container exists, create if not
        if not container_client.exists():
            container_client.create_container()

        # Extract the filename to use it as the blob name
        blob_name = os.path.basename(file_path)
        
        # Create a blob client for the file
        blob_client = container_client.get_blob_client(blob_name)
        
        # Upload the file with appropriate content type for PDF
        with open(file_path, "rb") as file:
            blob_client.upload_blob(file, overwrite=True, content_settings=ContentSettings(content_type='application/pdf'))
        
        # Construct the URL to the uploaded blob
        blob_url = f"https://{config.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{config.AZURE_CONTAINER_NAME}/{blob_name}"

        print("Upload successful. File URL:", blob_url)
        return blob_url

    except Exception as e:
        print("An error occurred during upload:", str(e))
        return None


# Function to analyze the PDF using Document Intelligence
def analyze_pdf(pdf_path_or_url, is_url=False):
    analyze_url = f"{config.DOC_INTEL_ENDPOINT}/formrecognizer/documentModels/prebuilt-read:analyze?api-version=2023-07-31"
    headers = {
        "Content-Type": "application/json" if is_url else "application/octet-stream",
        "Ocp-Apim-Subscription-Key": config.DOC_INTEL_API_KEY,
    }

    if is_url:
        data = {"urlSource": pdf_path_or_url}
        response = requests.post(analyze_url, headers=headers, json=data)
    else:
        with open(pdf_path_or_url, "rb") as file:
            response = requests.post(analyze_url, headers=headers, data=file.read())

    if response.status_code == 202:
        operation_location = response.headers["Operation-Location"]
        while True:
            result_response = requests.get(
                operation_location,
                headers={"Ocp-Apim-Subscription-Key": config.DOC_INTEL_API_KEY},
            )
            result_json = result_response.json()

            if result_json["status"] in ["succeeded", "failed"]:
                break
            time.sleep(1)

        # Check if the analysis succeeded
        if result_json["status"] == "succeeded":
            if (
                "analyzeResult" in result_json
                and "content" in result_json["analyzeResult"]
            ):
                extracted_text = result_json["analyzeResult"]["content"]
                return extracted_text
            else:
                print("No content found in the response.")
                return None
    else:
        print("Error in initiating analysis:", response.json())
        return None


# Function to query OpenAI
def ask_openai(question, context):
    headers = {"Content-Type": "application/json", "api-key": config.OPENAI_API_KEY}

    # Create the messages array for the chat model
    messages = [
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]

    data = {"messages": messages, "max_tokens": 750, "temperature": 0.7}

    response = requests.post(config.OPENAI_ENDPOINT, headers=headers, json=data)

    # Check the response status code
    print("OpenAI response status code:", response.status_code)

    # Print raw response for debugging
    try:
        # print("Raw OpenAI response text:", response.text)  # For debugging
        if response.status_code == 200:
            return response.json()["choices"][0]["message"][
                "content"
            ].strip()  # Updated structure
        else:
            print(
                "Error in OpenAI request:", response.json()
            )  # To see the error details
            return None
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response from OpenAI.")
        return None


# GUI to select a PDF file
def select_pdf():
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")),
    )

    if file_path:
        # Upload to Azure and get the file URL
        pdf_url = upload_pdf_to_azure(file_path)
        print("Uploaded file available at:", pdf_url)

        # Analyze the PDF
        extracted_text = analyze_pdf(pdf_url, is_url=True)

        if extracted_text:
            user_question = """
                Your role is to analyze the project outline document for each task to estimate man-days, suggest fitting roles, and outline potential issues.

                Limit yourself to 3 tasks for now.

                Please generate detailed estimations in JSON format as shown below. Follow these guidelines, and don't include comments in the JSON structure:

                1. **Task Description**: Summarize the task in a detailed sentence or two.
                2. **Fitting Employees**: Recommend appropriate roles (like "Backend Developer," "UI Designer," "Project Manager") and estimate the number of employees required for each task.
                3. **Estimated Days**: Provide three estimates for the duration of each task:
                    - "min": Minimum number of days if everything goes smoothly.
                    - "most likely": Average or most likely number of days required.
                    - "max": Maximum number of days if there are delays or added complexity.
                4. **Potential Issues**: List potential risks or issues that might arise, such as “security concerns,” “data compliance requirements,” or “scope changes.”

                Return the response in this JSON structure:
                
                ```json
                {
                    "list_of_all_tasks": {
                        "task 1": {
                            "description": "Task Description",
                            "fitting_employees": [
                                {
                                    "role": "Role Name",
                                    "count": 2
                                }
                            ],
                            "estimated_days": {
                                "min": 5,
                                "most_likely": 6,
                                "max": 7
                            },
                            "potential_issues": [
                                "Issue 1",
                                "Issue 2",
                                "Issue 3"
                            ]
                        },
                        "task 2": {
                            "description": "Another Task Description",
                            "fitting_employees": [
                                {
                                    "role": "Another Role",
                                    "count": 1
                                }
                            ],
                            "estimated_days": {
                                "min": 2,
                                "most_likely": 4,
                                "max": 6
                            },
                            "potential_issues": [
                                "Issue A",
                                "Issue B"
                            ]
                        }
                        // Additional tasks follow
                    }
                }
                ```
            """  # Example question
            answer = ask_openai(user_question, extracted_text)

            if answer:
                with open("answer.json", "w") as f:
                    f.write(answer)
                messagebox.showinfo("Success", "Analysis completed and saved as answer.json!")
            else:
                messagebox.showerror("Error", "Failed to get a response from OpenAI.")
        else:
            messagebox.showerror("Error", "Failed to analyze PDF.")


root = tk.Tk()
root.title("DELWARExHOWEST - PDF Estimation Generator")
root.geometry("400x200")

upload_button = tk.Button(root, text="Upload and Analyze PDF", command=select_pdf)
upload_button.pack(expand=True)

root.mainloop()    