import os
import time
import requests
import pandas as pd
import streamlit as st
from azure.storage.blob import BlobServiceClient, ContentSettings
from util.query_roles_and_rates_from_db import fetch_roles_and_rates
import io
import json

#region PDF Upload and Analysis
def upload_pdf_to_azure(uploaded_file):
    """
    Uploads a PDF file to an Azure Blob Storage container.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            st.secrets["AZURE_STORAGE_CONNECTION_STRING"]
        )

        container_client = blob_service_client.get_container_client(
            st.secrets["AZURE_CONTAINER_NAME"]
        )

        if not container_client.exists():
            container_client.create_container()

        blob_name = uploaded_file.name
        blob_client = container_client.get_blob_client(blob_name)

        blob_client.upload_blob(
            uploaded_file,
            overwrite=True,
            content_settings=ContentSettings(content_type="application/pdf"),
        )

        blob_url = f"https://{st.secrets['AZURE_STORAGE_ACCOUNT_NAME']}.blob.core.windows.net/{st.secrets['AZURE_CONTAINER_NAME']}/{blob_name}"
        
        st.success(f"Upload successful. File URL: {blob_url}")
        return blob_url

    except Exception as e:
        st.error(f"An error occurred during upload: {str(e)}")
        return None

def analyze_pdf(pdf_path_or_url, is_url=False):
    """
    Analyzes a PDF document using the Azure Form Recognizer service.
    """
    analyze_url = f"{st.secrets['DOC_INTEL_ENDPOINT']}/formrecognizer/documentModels/prebuilt-read:analyze?api-version=2023-07-31"
    headers = {
        "Content-Type": "application/json" if is_url else "application/octet-stream",
        "Ocp-Apim-Subscription-Key": st.secrets["DOC_INTEL_API_KEY"],
    }

    try:
        if is_url:
            data = {"urlSource": pdf_path_or_url}
            response = requests.post(analyze_url, headers=headers, json=data)
        else:
            response = requests.post(
                analyze_url, headers=headers, data=pdf_path_or_url.read()
            )

        if response.status_code == 202:
            operation_location = response.headers["Operation-Location"]
            while True:
                result_response = requests.get(
                    operation_location,
                    headers={
                        "Ocp-Apim-Subscription-Key": st.secrets["DOC_INTEL_API_KEY"]
                    },
                )
                result_json = result_response.json()

                if result_json["status"] in ["succeeded", "failed"]:
                    break
                time.sleep(1)

            if result_json["status"] == "succeeded":
                if (
                    "analyzeResult" in result_json
                    and "content" in result_json["analyzeResult"]
                ):
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
#endregion

#region AI Search and Task Estimation
def generate_search_query(pdf_content, user_prompt):
    openai_prompt = f"""
    Context:
    You are helping to create a project timeline. The user has provided a PDF document with project details and additional requirements.

    PDF Content:
    {pdf_content}

    Additional User Requirements:
    {user_prompt}

    Instructions:
    - Write a query to search for tasks relevant to the described project.
    - The query should focus on finding tasks with clear roles, responsibilities, or descriptions relevant to the project.
    - Consider both the PDF content and additional requirements when forming the query.
    - Aim for tasks that are high-priority or foundational to the type of project described.
    - Keep the query concise but descriptive enough to retrieve meaningful results.

    Query:
    """

    headers = {
        "Content-Type": "application/json",
        "api-key": st.secrets["OPENAI_API_KEY"],
    }
    data = {
        "messages": [{"role": "user", "content": openai_prompt}],
        "max_tokens": 150,
        "temperature": 0.7,
    }

    try:
        response = requests.post(
            st.secrets["OPENAI_ENDPOINT"], headers=headers, json=data
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            st.error(f"Error in OpenAI query generation: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred during query generation: {str(e)}")
        return None

def query_azure_ai_search(generated_query):
    headers = {
        "Content-Type": "application/json",
        "api-key": st.secrets["AZURE_SEARCH_API_KEY"],
    }
    
    search_url = f"{st.secrets['AZURE_SEARCH_ENDPOINT']}/indexes/{st.secrets['AZURE_SEARCH_INDEX_NAME']}/docs/search?api-version=2021-04-30-Preview"

    search_data = {
        "search": generated_query,
        "top": 5,
    }

    try:
        response = requests.post(search_url, headers=headers, json=search_data)
        if response.status_code == 200:
            search_results = response.json()
            return search_results['value']
        else:
            st.error(f"Error querying AI Search: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error while querying Azure AI Search: {str(e)}")
        return None

def construct_estimation_prompt(search_results, pdf_content, user_prompt):
    tasks = "\n\n".join([
        f"MSCW: {result['MSCW']}\nArea: {result['Area']}\nModule: {result['Module']}\nFeature: {result['Feature']}\nTask: {result['Task']}\nProfile: {result['Profile']}\nMinDays: {result.get('MinDays', 'N/A')}\nRealDays: {result.get('RealDays', 'N/A')}\nMaxDays: {result.get('MaxDays', 'N/A')}\n% Contingency: {result.get('Contingency', 'N/A')}\nEstimatedDays: {result.get('EstimatedDays', 'N/A')}\nEstimatedPrice: {result.get('EstimatedPrice', 'N/A')}\nPotential Issues: {', '.join(result.get('PotentialIssues', []))}" 
        for result in search_results
    ])
    
    tasks_json = [json.dumps(result, indent=4) for result in search_results]
    tasks_json_output = '[\n' + ',\n'.join(tasks_json) + '\n]'
    st.json(tasks_json_output)

    return f"""
    Context:
    The user has described their project as follows:
    {user_prompt}

    The following tasks were retrieved based on the user's project description:
    {tasks}

    Instructions:
        - Create a detailed project estimation from the user prompt using these tasks.
        Do not blindly copy the tasks but use them as a guideline to create the new estimated tasks.
        - For each task:
            - Provide a clear timeline (in days) for its completion.
            - Identify any risks, delays, or dependencies that could impact the task.
            - Include the task's estimated price (based on the Profile and EstimatedDays) and any required resources or roles.
        - Calculate the overall project duration, including potential buffer times for dependencies or risks.
        - Present the estimation in a structured format, such as a table or JSON.

    General pointers:
        - Keep the estimated days low. Anywhere from 0 for MinDays to 4 days for MaxDays is a good estimate.
        - Make sure that you think about how many tasks there need to be. Don't just copy the amount of tasks from the search_results.
        - Make sure that the "Task" description contains relevant information from the requirements of the user prompt.
        - Make sure not to use the same Area for every task. Try to distribute the tasks across different Areas.
        - Make sure to use a wide variety of Profiles for the tasks. Don't use the same Profile for every task.
        - Make sure to have different MSCW priorities for the tasks. Make sure to have at least two tasks for each priority.
        - Make sure that the tasks are assigned in order of Must Have then Should Have then Could Have.
        - Make sure that not every task contains "Potential Issues". You may assign them, but only if the possibility of it happening is likely.
        - Temporary: You should ignore the "Offshore" roles.
        - The cost per profile varies: Each Profile has an associated daily rate, which must be used to calculate the EstimatedPrice.
          These rates are as follows: {fetch_roles_and_rates()}

    Description:
        1. **MSCW**: The priority of the task. The options are: "1 Must Have", "2 Should Have", "3 Could Have"
        2. **Area**: The area of the project where the task belongs. The options are: "01 Analyze & Design", "03 Setup", "04 Development"
        3. **Module**: The software engineering domain of the task. The options are: "Overall", "Frontend", "Middleware", "Infra", "IoT", "Security"
        4. **Feature**: What exactly is being done in the task. The options are: "General", "Technical Lead", "Project Manager", "Sprint Artifacts & Meetings", "Technical Analysis", "Functional Analysis", "User Experience (UX)", "User Interface (UI)", "Security Review", "Go-Live support", "Setup Environment + Azure", "Setup Projects", "Authentication & Authorizations", "Monitoring", "Notifications", "Settings" , "Filtering / search"
        5. **Task**: Summarize the task in a detailed sentence or two.
        6. **Profile**: The role of the person who will perform the task. The options are the ones we defined above with their rates.
        7. **MinDays**: The estimated minimum number of days required to complete the task.
        8. **RealDays**: The average or most likely number of days required to complete the task.
        9. **MaxDays**: The estimated maximum number of days required to complete the task.
        10. **Contingency**: For this write "0" for now.
        11. **EstimatedDays**: This is a value between MinDays and MaxDays.
        12. **EstimatedPrice**: this is a formula that calculates the estimated price based on the EstimatedDays and the cost of the Profile. The formula is: EstimatedDays * the cost of the Profile.
        13. **Potential Issues**: List potential risks or issues that might arise, such as “security concerns,” “data compliance requirements,” or “scope changes.”

    Return your response in the following JSON format:
    {{
        "total_price": "The sum of the EstimatedPrice",
        "tasks": [
            {{
                "MSCW": "Must Have / Should Have / Could Have",
                "Area": "Area of work",
                "Module": "Module category",
                "Feature": "Feature of the task",
                "Task": "Task description",
                "Profile": "Profile needed for the task",
                "MinDays": "Minimum estimated days for the task",
                "RealDays": "Actual days taken to complete the task",
                "MaxDays": "Maximum estimated days for the task",
                "% Contingency": "Contingency percentage for the task",
                "EstimatedDays": "Estimated duration for the task",
                "EstimatedPrice": "Estimated price for the task",
                "Potential Issues": "Any potential risks or issues impacting the task"
            }},
            ...
        ]
    }}
    """

def ask_openai_for_estimation(prompt):
    headers = {
        "Content-Type": "application/json",
        "api-key": st.secrets["OPENAI_API_KEY"],
    }

    data = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1500,
        "temperature": 0.1
    }

    try:
        response = requests.post(
            st.secrets["OPENAI_ENDPOINT"], headers=headers, json=data
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            st.error(f"Error in OpenAI estimation request: {response.json()}")
            return None
    except Exception as e:
        st.error(f"An error occurred during OpenAI estimation request: {str(e)}")
        return None

def parse_and_display_estimation(response_json):
    try:
        
        if not response_json:
            st.error("Received empty response for estimation.")
            return
        
        data = json.loads(response_json)
        total_price = data.get("total_price", "N/A")
        tasks = data.get("tasks", [])
          
        if not tasks:
            st.error("No tasks found in the estimation.")
            return


        st.write(f"### Estimated cost of the project: € {total_price}")

        if tasks:
            df = pd.DataFrame(tasks)
            st.dataframe(df)

            st.write(f"## Estimated cost of the project: € {total_price}")

            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Project Estimation")
            excel_buffer.seek(0)

            st.download_button(
                label="Download Estimation as Excel",
                data=excel_buffer,
                file_name="project_estimation.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.error("No tasks found in the estimation.")
    except json.JSONDecodeError as e:
        st.error(f"JSON decoding error: {str(e)}")
    except Exception as e:
        st.error(f"Error while parsing estimation response: {str(e)}")
#endregion

#region Streamlit UI
st.header("AI-Driven Project Estimation Tool")

# Initialize session state for PDF content
if "pdf_content" not in st.session_state:
    st.session_state.pdf_content = None

# File uploader
uploaded_file = st.file_uploader("Upload your project PDF", type=["pdf"])

# Additional requirements input
user_prompt = st.text_area("Additional project requirements (optional):")

if uploaded_file:
    if st.session_state.pdf_content is None:
        with st.spinner("Uploading and analyzing PDF..."):
            pdf_url = upload_pdf_to_azure(uploaded_file)
            if pdf_url:
                st.session_state.pdf_content = analyze_pdf(pdf_url, is_url=True)

    if st.session_state.pdf_content and st.button("Generate Project Estimation"):
        with st.spinner("Generating query..."):
            search_query = generate_search_query(st.session_state.pdf_content, user_prompt)

        if search_query:
            with st.spinner("Querying Azure AI Search..."):
                search_results = query_azure_ai_search(search_query)

            if search_results:
                with st.spinner("Generating project estimation..."):
                    estimation_prompt = construct_estimation_prompt(
                        search_results,
                        st.session_state.pdf_content,
                        user_prompt
                    )
                    ai_response = ask_openai_for_estimation(estimation_prompt)

                if ai_response:
                    parse_and_display_estimation(ai_response)
                else:
                    st.error("No response from OpenAI for estimation.")

#endregion