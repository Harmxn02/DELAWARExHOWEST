import os
import pandas as pd
import streamlit as st
import random as rnd
from datetime import datetime


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
    # Define the cost per profile
    PROFILE_COSTS = {
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

    mscw = rnd.choice(MSCW_OPTIONS)
    area = rnd.choice(AREAS)
    module = rnd.choice(MODULES)
    feature = rnd.choice(FEATURES)
    task = f"Task: {feature} for {module}"  # Example task description
    num_profile = rnd.randint(1, 4)  # Needed for adjusting the price and amount of days
    profile = f"{num_profile} {rnd.choice(PROFILES)}"
    min_days = rnd.randint(3, 7) * num_profile
    most_likely_days = rnd.randint(min_days + 1, min_days + 3)
    max_days = rnd.randint(most_likely_days + 1, most_likely_days + 4)
    contingency = "0%"  # Placeholder: This is currently low priority
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
def generate_dataset(num_projects):
    return [generate_fake_project() for _ in range(num_projects)]

# Save the dataset to an Excel file
def save_data_to_excel(fake_data, output_dir="export/fake data", file_prefix="fake_project_"):
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Initialize a list to hold the file paths of the generated files
    saved_file_paths = []

    # Loop through and generate a file for each project batch
    for i in range(len(fake_data)):
        # Generate a unique filename based on the current timestamp + index
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{file_prefix}{timestamp}_{i + 1}.xlsx"
        output_path = os.path.join(output_dir, file_name)

        # Save to Excel
        df = pd.DataFrame(fake_data[i])  # Each element in fake_data is a list of project data
        df.to_excel(output_path, index=False)
        saved_file_paths.append(output_path)
        print(f"Fake data project created at: {output_path}")

    return saved_file_paths  # Return the paths of all saved files

#endregion

st.header("Generate Fake Projects")

num_generate_files = st.number_input("Enter the number of projects to generate:", min_value=1, max_value=50, step=1)

with st.spinner("Generating files..."):

    if st.button("Generate fake projects"):
        fake_projects = generate_dataset(num_generate_files)

        if fake_projects:
            st.success(f"Fake project(s) successfully generated! ({num_generate_files} projects)")

            with st.spinner("Saving files..."):
                # Save files, the new function now supports generating multiple files
                output_paths = save_data_to_excel([fake_projects] * num_generate_files)  # Generate separate files for each project

                if output_paths:
                    st.success(f"Generated {num_generate_files} fake project file(s)!")
                    
                    # Show a list of saved files
                    st.write(f"Generated files: {output_paths}")

                    # Optionally preview the first dataset
                    st.write("Generated Data preview:")
                    st.dataframe(pd.DataFrame(fake_projects))  # Preview the first dataset      