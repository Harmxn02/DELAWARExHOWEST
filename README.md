# DELAWARExHOWEST - AI-driven Project Estimations and Team Planning Platform

## Overview

The **AI-driven Project Estimations and Team Planning Platform** is designed to help software engineering teams estimate the development effort required for a project based on detailed project descriptions provided in PDF format. The applications reads in a PDF-file describing a project (including tasks, tools, frameworks, etc.) and generates estimations for each task in terms of:

1. **MSCW**: The priority of the task.
1. **Area**: The area of the project where the task belongs.
1. **Module**: The software engineering domain of the task.
1. **Feature**: What exactly is being done in the task.
1. **Task**: Summarize the task in a detailed sentence or two.
1. **Profile**: The role of the person who will perform the task.
1. **MinDays**: The estimated minimum number of days required to complete the task.
1. **RealDays**: The average or most likely number of days required to complete the task.
1. **MaxDays**: The estimated maximum number of days required to complete the task.
1. **Contingency**
1. **EstimatedDays**
1. **EstimatedPrice**
1. **Potential Issues**

## Workflow

1. You will start by uploading a PDF file in the **Project Estimation Tool**. This tool will generate estimations for you, using an outline (a PDF file) of your project.
2. After having generated the estimations you can now press the `Export Profiles to JSON` button, which contains all employee's roles you will need for the project.
3. Moving over to the **Team Planning Platform**, where you can plan your project
    - **Tab 1 - Add Project**: Give your project a name and press `Add Project`
    - **Tab 2 - View Projects**: Refresh the page. If your project was made succesfully you should see your project in the list
    - **Tab 3 - View Employees**: Upload the `project_profiles.json` file you exported on the **Project Estimation Tool** page here. Once you upload it, you will see a list of all roles your project requires according to our estimation tool. Below, you can see all employees and their roles, you can filter by role to find the employees you need.
    - **Tab 4 - Assign Project**: Now you can assign employees to your project by typing the employee's name in the search bar, and selecting the newly made project, and then pressing the `Assign Project` button
    - **Tab 5 - Close Project** (optional): Once your project has finalised, you can close the project. This will set the project to `inactive` in the database, but does not delete it. Closing a project makes all assigned employees available again.

## Technologies used

- Scripting: Python
- Natural langage processing: GPT-3.5 through the Azure OpenAI resource
- PDF parsing: Azure Document Intelligence

- Frontend: Streamlit application
- Hosting: currently hosted on Streamlit itself, but will most likely be Azure Static Web Apps

## Installation and setup

### Requirements

- Python
- API Key for Language Model (e.g., OpenAI API through Azure)

### Steps to install

#### Step 1. Clone the repository

```bash
git clone https://github.com/Harmxn02/DELAWARExHOWEST_AI-driven-project-estimations.git
cd DELAWARExHOWEST_AI-driven-project-estimations

```

#### Step 2. Install necessary libraries

```bash
cd .\app\
pip install -r requirements.txt
```

#### Step 3. Set up environment variables

Inside the `.\app\` directory create a `.streamlit` folder, with inside it a `secrets.toml` file which contain your API keys and configuration settings. Below is an example using placeholder values:

```python
# secrets.toml

# Azure Document Intelligence Variables
DOC_INTEL_ENDPOINT = "placeholder"
DOC_INTEL_API_KEY = "placeholder"

# Azure OpenAI Variables
OPENAI_ENDPOINT = "placeholder"
OPENAI_API_KEY = "placeholder"

# Azure Blob Storage Variables
AZURE_STORAGE_ACCOUNT_NAME = "placeholder"
AZURE_CONTAINER_NAME = "placeholder"
AZURE_STORAGE_CONNECTION_STRING = "placeholder"
```

#### Step 4. Run the streamlit application

Run the following command:

Make sure you are inside the `.\app\` directory and run the following command:

```bash
streamlit run streamlit_main.py
```

If you are not inside the `.\app\` directory, the streamlit application will not find the secrets.toml file because that is stored inside the `.\app\`-directory.
