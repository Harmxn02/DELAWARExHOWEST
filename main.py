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

    data = {"messages": messages, "max_tokens": 2000, "temperature": 0.7}

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
                Your role is to analyze the project outline document, and for each task to estimate man-days, suggest fitting roles, and outline potential issues.

                Limit yourself to 10 detailed tasks for now. The tasks should be 1 specific task in the project. For example "Create the login screen for the web-app", and not "Frontend development".

                Please generate detailed estimations in JSON format as shown below. Follow these guidelines, and don't include comments in the JSON structure:


                1. **MSCW**: The priority of the task. The options are: "1 Must Have", "2 Should Have", "3 Could Have"
                2. **Area**: The area of the project where the task belongs. The options are: "01 Analyze & Design", "03 Setup", "04 Development"
                3. **Module**: The software engineering domain of the task. The options are: "Overall", "Frontend", "Middleware", "Infra", "IoT", "Security"
                4. **Feature**: What exactly is being done in the task. The options are: "General", "Technical Lead", "Project Manager", "Sprint Artifacts & Meetings", "Technical Analysis", "Functional Analysis", "User Experience (UX)", "User Interface (UI)", "Security Review", "Go-Live support", "Setup Environment + Azure", "Setup Projects", "Authentication & Authorizations", "Monitoring", "Notifications", "Settings" , "Filtering / search"
                5. **Task**: Summarize the task in a detailed sentence or two.
                6. **Profile**: The role of the person who will perform the task. The options are: "0 Blended FE dev", "0 Blended MW dev", "0 Blended Overall dev, 0 Blended XR dev", "1 Analyst", "2 Consultant Technical", "3 Senior Consultant Technical", "4 Lead Expert", "5 Manager", "6 Senior Manager", "7 DPH Consultant Technical", "8 DPH Senior Consultant Technical", "9 DPH Lead Expert/Manager"
                7. **MinDays**: The estimated minimum number of days required to complete the task.
                8. **RealDays**: The average or most likely number of days required to complete the task.
                9. **MaxDays**: The estimated maximum number of days required to complete the task.
                10. **Contingency**: for this write "I don't know what this feature means -HS"
                11. **EstimatedDays**: this is a formula that calculates the estimated days based on the MinDays, RealDays, and MaxDays. The formula is: (MinDays + (4 * RealDays) + (4 * MaxDays)) / 9. Make sure to round up to the nearest whole number.
                12. **EstimatedPrice**: this is a formula that calculates the estimated price based on the EstimatedDays and the cost of the Profile. For now use 200 as the cost per day. The formula is: EstimatedDays * 200.
                13. **Potential Issues**: List potential risks or issues that might arise, such as “security concerns,” “data compliance requirements,” or “scope changes.”

                
                General pointers:
                    - Keep the estimated days low. Anywhere from 0 for MinDays to 4 days for MaxDays is a good estimate.
                    - Make sure not to use the same Area for every task. Try to distribute the tasks across different Areas.
                    - Make sure to use a wide variety of Profiles for the tasks. Don't use the same Profile for every task.


                Return the response in this JSON structure:
                
                ```json
                {
                    "list_of_all_tasks": [
                        {
                            "MSCW": "1 Must Have",
                            "Area": "01 Analyze & Design",
                            "Module": "Overall",
                            "Feature": "General",
                            "Task": "Task 1 description",
                            "Profile": "1 Analyst",
                            "MinDays": 1,
                            "RealDays": 2,
                            "MaxDays": 3,
                            "Contingency": "I don't know what this feature means -HS",
                            "EstimatedDays": 3,
                            "EstimatedPrice": 600,
                            "potential_issues": [
                                "Issue 1",
                                "Issue 2",
                                "Issue 3"
                            ]
                        },
                        // Additional tasks follow
                    ]    
                }
                ```
            """
            answer = ask_openai(user_question, extracted_text)

            if answer:
                with open("response.json", "w") as f:
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