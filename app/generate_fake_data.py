import os
import pandas as pd
import streamlit as st
import random as rnd
from datetime import datetime
import json

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
POTENTIAL_ISSUES = [
    "Scope creep", "Integration issues with Azure", "Cross-browser compatibility issues", 
    "Usability challenges", "API security vulnerabilities", "Performance issues", 
    "Security vulnerabilities", "Calendar integration errors"
]
# Define a cost per role
ROLE_COSTS = {
    "Consultant Technical": 250,
    "Senior Consultant Technical": 300,
    "Blended FE dev": 200,
    "Blended MW dev": 220,
    "Fullstack Developer": 240,
    "UI Designer": 180,
    "Project Manager": 400,
    "Quality Assurance Engineer": 220,
    "Lead Expert": 500
}

# Initialize the global issue counter
issue_counter = 0

# Generate a single random task
def generate_fake_task():
    global issue_counter  # Declare global to update the issue counter

    mscw = rnd.choice(MSCW_OPTIONS)
    area = rnd.choice(AREAS)
    module = rnd.choice(MODULES)
    feature = rnd.choice(FEATURES)
    task = f"Task: {feature} for {module}"  # Example task description
    role = rnd.choice(list(ROLE_COSTS.keys()))  # Randomly choose a role

    # Time estimates
    min_days = rnd.randint(1, 4)
    most_likely_days = rnd.randint(min_days + 1, min_days + 3)
    max_days = rnd.randint(most_likely_days + 1, most_likely_days + 4)
    estimated_days = rnd.randint(min_days, max_days)  # Random value between min and max days

    # Calculate cost for the random role
    daily_cost = ROLE_COSTS.get(role)
    estimated_price = estimated_days * daily_cost  # Cost for the role

    contingency = "0%"  # Placeholder: This is currently low priority

    # Add an issue once every 20th task
    potential_issue = ""
    issue_counter += 1
    if issue_counter % 20 == 0:
        potential_issue = rnd.sample(POTENTIAL_ISSUES, 1)  # Pick 1 random issue

    # Return a dictionary representing the task
    return {
        "MSCW": mscw,
        "Area": area,
        "Module": module,
        "Feature": feature,
        "Task": task,
        "Profile": role,
        "MinDays": min_days,
        "RealDays": most_likely_days,
        "MaxDays": max_days,
        "Contingency": contingency,
        "EstimatedDays": estimated_days,
        "EstimatedPrice": estimated_price,
        "potential_issues": potential_issue,
    }

# Generate a dataset with multiple projects, each with a random number of tasks
def generate_dataset(num_projects):
    dataset = []
    for _ in range(num_projects):
        num_tasks = rnd.randint(5, 22)  # Random number of tasks per project (between 5 and 22)
        project_tasks = [generate_fake_task() for _ in range(num_tasks)]  # Generate the tasks
        dataset.append(project_tasks)  # Add tasks to the dataset as a list of tasks
    return dataset

# Save the dataset to Excel and JSON files, separated into their respective folders
def save_data_to_excel_and_json(fake_data, output_dir="export", file_prefix="fake_project_"):
    # Create separate directories for Excel and JSON files
    excel_dir = os.path.join(output_dir, "fake_data_excel")
    json_dir = os.path.join(output_dir, "fake_data_json")
    os.makedirs(excel_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)

    # Initialize a list to hold the file paths of the generated files
    saved_file_paths = []

    # Loop through and generate a file for each project batch
    for i, project in enumerate(fake_data):
        # Generate a unique filename based on the current timestamp + index
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name_prefix = f"{file_prefix}{timestamp}_{i + 1}"

        # Save to Excel
        excel_file_name = f"{file_name_prefix}.xlsx"
        excel_output_path = os.path.join(excel_dir, excel_file_name)
        df = pd.DataFrame(project)  # Each element in fake_data is a list of project data
        df.to_excel(excel_output_path, index=False)
        saved_file_paths.append(excel_output_path)
        print(f"Fake data project saved to Excel at: {excel_output_path}")

        # Save to JSON
        json_file_name = f"{file_name_prefix}.json"
        json_output_path = os.path.join(json_dir, json_file_name)
        with open(json_output_path, "w") as json_file:
            json.dump(project, json_file, indent=4)  # Write the project data as JSON
        saved_file_paths.append(json_output_path)
        print(f"Fake data project saved to JSON at: {json_output_path}")

    return saved_file_paths  # Return the paths of all saved files

#endregion

# Streamlit interface
st.header("Generate Fake Projects")

num_generate_files = st.number_input("Enter the number of projects to generate:", min_value=1, max_value=50, step=1)

with st.spinner("Generating files..."):
    if st.button("Generate fake projects"):
        fake_projects = generate_dataset(num_generate_files)

        if fake_projects:
            st.success(f"Fake project(s) successfully generated! ({num_generate_files} projects)")

            with st.spinner("Saving files..."):
                # Save files, now generating both Excel and JSON files for each project
                output_paths = save_data_to_excel_and_json(fake_projects)  # Generate separate files for each project

                if output_paths:
                    st.success(f"Generated {num_generate_files} fake project file(s)!")

                    # Show a list of saved files
                    st.write(f"Generated files: {output_paths}")

                    # Optionally preview the first dataset
                    st.write("Generated Data preview:")
                    st.dataframe(pd.DataFrame(fake_projects[0]))  # Preview the first project
