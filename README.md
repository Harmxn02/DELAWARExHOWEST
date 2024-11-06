# DELAWARExHOWEST - Project Estimation Application

## Overview

The **Project Estimation Application** is designed to help software engineering teams estimate the development effort required for a project based on detailed project descriptions provided in PDF format. The script reads in the PDFs describing a project (including tasks, tools, framewors, etc.) and generates estimations for each task in terms of:

- Estimated man-days (minimum, most likely, maximum)
- Fitting employee roles from a pre-defined list of job titles
- Feature categories for each task

These estimations are returned in a structured JSON format, which is read into the Web App.

## Example JSON output

The script returns a structured JSON output with estimated details for each task in the project, similar to the example below:

``` json
{
    "list_of_all_tasks": {
        "task 1": {
            "description": "Design a responsive UI that provides a seamless experience across devices (desktop, tablet, mobile)",
            "fitting_employees": [
                {
                    "role": "UI Designer",
                    "count": 2
                }
            ],
            "estimated_days": {
                "min": 5,
                "most_likely": 7,
                "max": 10
            },
            "potential_issues": [
                "Cross-browser compatibility issues",
                "UI/UX challenges for mobile devices",
                "Scope changes due to design iterations"
            ]
        },
        "task 2": {
            "description": "Develop a relational database to store property listings, user profiles, and interactions",
            "fitting_employees": [
                {
                    "role": "Database Developer",
                    "count": 2
                }
            ],
            "estimated_days": {
                "min": 10,
                "most_likely": 14,
                "max": 20
            },
            "potential_issues": [
                "Data migration challenges from legacy systems",
                "Data compliance requirements",
                "Data security concerns"
            ]
        },
        "task 3": {
            "description": "Build REST APIs for accessing and updating property listings, user profiles, and appointment details",
            "fitting_employees": [
                {
                    "role": "Backend Developer",
                    "count": 3
                }
            ],
            "estimated_days": {
                "min": 15,
                "most_likely": 20,
                "max": 30
            },
            "potential_issues": [
                "Integration challenges with third-party systems",
                "API security vulnerabilities",
                "Scope changes due to API design iterations"
            ]
        }
    }
}
```

## Technologies used

- Scripting: Python
- Natural langage processing: GPT-3.5 through the Azure OpenAI resource
- PDF parsing: Azure Document Intelligence

- Frontend: to-do
- Database: to-do
- Hosting: to-do, but will most likely be Azure Static Web Apps

## Installation and setup

### Requirements

- Python
- Node.js
- API Key for Language Model (e.g., OpenAI API through Azure)

### Steps to install

1. Clone the repository

``` bash
git clone https://github.com/Harmxn02/DELAWARExHOWEST_Setup.git
cd DELAWARExHOWEST_Setup

```

2. Install necessary libraries

``` bash
pip install -r requirements.txt
```

3. Set up environment variables

Create a `config.py` in the root directory and include your API keys and configuration settings. Below is an example using placeholder values:

``` python
# config.py

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

4. Still in progress

Most likely we will have an executable that will run the script, and afterwards automatically open the web-app.
