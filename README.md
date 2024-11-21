# DELAWARExHOWEST - AI-driven Project Estimations Application

## Overview

The **AI-Driven Project Estimation Application** is designed to help software engineering teams estimate the development effort required for a project based on detailed project descriptions provided in PDF format. The applications reads in a PDF-file describing a project (including tasks, tools, frameworks, etc.) and generates estimations for each task in terms of:

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

These estimations are returned in a structured JSON format, which is read into the Web App.

## Example JSON output

The script returns a structured JSON output with estimated details for each task in the project, similar to the example below:

```json
{
    "list_of_all_tasks": [
        {
            "MSCW": "1 Must Have",
            "Area": "01 Analyze & Design",
            "Module": "Overall",
            "Feature": "Technical Analysis",
            "Task": "Gather requirements from RealEstateCo stakeholders and develop project scope document",
            "Profile": "1 Analyst",
            "MinDays": 2,
            "RealDays": 4,
            "MaxDays": 6,
            "Contingency": "I don't know what this feature means -HS",
            "EstimatedDays": 5,
            "EstimatedPrice": 1000,
            "potential_issues": [
                "Scope changes",
                "Lack of clarity in requirements"
            ]
        },
        {
            "MSCW": "1 Must Have",
            "Area": "01 Analyze & Design",
            "Module": "Overall",
            "Feature": "Functional Analysis",
            "Task": "Create functional specifications document for the platform",
            "Profile": "2 Consultant Technical",
            "MinDays": 2,
            "RealDays": 3,
            "MaxDays": 4,
            "Contingency": "I don't know what this feature means -HS",
            "EstimatedDays": 4,
            "EstimatedPrice": 800,
            "potential_issues": [
                "Scope changes",
                "Lack of clarity in requirements"
            ]
        },
    ]
}
```

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
