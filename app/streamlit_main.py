import os
import time
import requests
import pandas as pd
import streamlit as st
from azure.storage.blob import BlobServiceClient, ContentSettings
import config
import io
import random as rnd


def upload_pdf_to_azure(uploaded_file):
    try:
        # Initialize the BlobServiceClient with the connection string
        blob_service_client = BlobServiceClient.from_connection_string(config.AZURE_STORAGE_CONNECTION_STRING)
        
        # Get a client for the container
        container_client = blob_service_client.get_container_client(config.AZURE_CONTAINER_NAME)
        
        # Ensure container exists, create if not
        if not container_client.exists():
            container_client.create_container()

        # Extract the filename from the uploaded file
        blob_name = uploaded_file.name
        
        # Create a blob client for the file
        blob_client = container_client.get_blob_client(blob_name)
        
        # Upload the file directly from the uploaded_file object
        blob_client.upload_blob(uploaded_file, overwrite=True, content_settings=ContentSettings(content_type='application/pdf'))
        
        # Construct the URL to the uploaded blob
        blob_url = f"https://{config.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{config.AZURE_CONTAINER_NAME}/{blob_name}"

        st.success(f"Upload successful. File URL: {blob_url}")
        return blob_url

    except Exception as e:
        st.error(f"An error occurred during upload: {str(e)}")
        return None


def analyze_pdf(pdf_path_or_url, is_url=False):
    analyze_url = f"{config.DOC_INTEL_ENDPOINT}/formrecognizer/documentModels/prebuilt-read:analyze?api-version=2023-07-31"
    headers = {
        "Content-Type": "application/json" if is_url else "application/octet-stream",
        "Ocp-Apim-Subscription-Key": config.DOC_INTEL_API_KEY,
    }

    try:
        if is_url:
            data = {"urlSource": pdf_path_or_url}
            response = requests.post(analyze_url, headers=headers, json=data)
        else:
            response = requests.post(analyze_url, headers=headers, data=pdf_path_or_url.read())

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
                if "analyzeResult" in result_json and "content" in result_json["analyzeResult"]:
                    return result_json["analyzeResult"]["content"]
                else:
                    st.warning("No content found in the analysis response.")
                    return None
        else:
            st.error(f"Error in initiating analysis: {response.json()}")
            return None
    except Exception as e:
        st.error(f"An error occurred during PDF analysis: {str(e)}")
        return None


def ask_openai(question, context):
    headers = {"Content-Type": "application/json", "api-key": config.OPENAI_API_KEY}

    messages = [{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}]
    data = {"messages": messages, "max_tokens": 2000, "temperature": 0.7}

    try:
        response = requests.post(config.OPENAI_ENDPOINT, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            st.error(f"Error in OpenAI request: {response.json()}")
            return None
    except Exception as e:
        st.error(f"An error occurred during OpenAI query: {str(e)}")
        return None

#region Generate fake data and store in Azure storageaccount

# Headers for the Excel file
HEADERS = [
    "MSCW", "Area", "Module", "Feature", "Task", "Profile", "MinDays", "RealDays", 
    "MaxDays", "Contingency", "EstimatedDays", "EstimatedPrice", "potential_issues"
]

# Lists for randomization
MSCW_OPTIONS = ["1 Must Have", "2 Should Have", "3 Could Have"]
AREAS = ["01 Analyze & Design", "02 Architecture", "03 Setup", "04 Development"]
MODULES = ["Overall", "Frontend", "Middleware", "Security"]
FEATURES = [
    "Technical Analysis", "Setup Environment + Azure", "User Interface (UI)", 
    "Authentication & Authorizations", "Filtering / search", "Notifications", 
    "Appointment Scheduling System", "Security Review", "Settings"
]
PROFILES = [
    "Consultant Technical", "Senior Consultant Technical", "Blended FE dev", 
    "Blended MW dev", "Fullstack Developer", "UI Designer", "Project Manager", 
    "Quality Assurance Engineer", "Lead Expert"
]
POTENTIAL_ISSUES = [
    "Scope creep", "Integration issues with Azure", "Cross-browser compatibility issues", 
    "Usability challenges", "API security vulnerabilities", "Performance issues", 
    "Security vulnerabilities", "Calendar integration errors"
]

# Generate a single random project entry
def generate_fake_project():
    mscw = rnd.choice(MSCW_OPTIONS)
    area = rnd.choice(AREAS)
    module = rnd.choice(MODULES)
    feature = rnd.choice(FEATURES)
    task = f"Task: {feature} for {module}"  # Example task description
    profile = f"{rnd.randint(1, 4)} {rnd.choice(PROFILES)}"
    min_days = rnd.randint(3, 7)
    most_likely_days = rnd.randint(min_days + 1, min_days + 3)
    max_days = rnd.randint(most_likely_days + 1, most_likely_days + 4)
    contingency = f"Contingency info for {feature}"  # Example contingency text
    estimated_days = most_likely_days + 2  # Add buffer for estimated days
    estimated_price = estimated_days * 200  # Example price calculation
    potential_issues = rnd.sample(POTENTIAL_ISSUES, 2)  # Pick 2 rnd issues
    
    # Return a dictionary representing the row
    return {
        "MSCW": mscw,
        "Area": area,
        "Module": module,
        "Feature": feature,
        "Task": task,
        "Profile": profile,
        "MinDays": min_days,
        "RealDays": most_likely_days,
        "MaxDays": max_days,
        "Contingency": contingency,
        "EstimatedDays": estimated_days,
        "EstimatedPrice": estimated_price,
        "potential_issues": potential_issues,
    }

# Generate a dataset with fake projects
def generate_dataset(num_projects=10):
    return [generate_fake_project() for _ in range(num_projects)]

# Save the dataset to an Excel file
def save_data_to_excel(fake_data, output_dir="export/fake data", file_name="fake_data.xlsx"):
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    output_path = os.path.join(output_dir, file_name)
    
    # Save to Excel
    df = pd.DataFrame(fake_data)
    df.to_excel(output_path, index=False)
    print(f"Fake data project created at: {output_path}")

#endregion

# Streamlit App
st.title("DELWARExHOWEST - PDF Estimation Generator")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    with st.spinner("Uploading and analyzing PDF..."):
        pdf_url = upload_pdf_to_azure(uploaded_file)

        if pdf_url:
            extracted_text = analyze_pdf(pdf_url, is_url=True)

            if extracted_text:
                st.success("PDF analysis complete!")
                # st.text_area("Extracted Text", extracted_text, height=300)

                # Prepare question for OpenAI
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
                    - It is possible for a task to be done within a day, so don't hesitate to use 0 for MinDays, and 0.5 for RealDays.
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

                with st.spinner("Querying OpenAI..."):
                    answer = ask_openai(user_question, extracted_text)

                if answer:
                    st.success("OpenAI analysis complete!")
                    # st.json(answer)

                    # Save response to a JSON file
                    json_file_path = "./response.json"
                    with open(json_file_path, "w") as f:
                        f.write(answer)

                    # Convert JSON to DataFrame and export
                    try:
                        df = pd.read_json(json_file_path)
                        if 'list_of_all_tasks' in df:
                            df = pd.json_normalize(df['list_of_all_tasks'])

                            # Export to CSV and download button
                            df.to_csv('./export/response.csv', index=False)
                            st.download_button(
                                label="Download CSV",
                                data=df.to_csv(index=False),
                                file_name="response.csv",
                                mime="text/csv"
                            )


                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                                df.to_excel(writer, index=False, sheet_name="Tasks")
                            excel_buffer.seek(0)

                            st.download_button(
                                label="Download Excel",
                                data=excel_buffer,
                                file_name="response.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            
                        else:
                            st.error("Failed to extract tasks: Check the prompt or OpenAI response structure.")
                    except Exception as e:
                        st.error(f"Error while processing OpenAI response: {str(e)}")
