import streamlit as st
import pandas as pd
import pymysql
import json

st.set_page_config(layout="wide", page_title="Team Planning Platform")
st.title("Team Planning Platform")

# Function to Create Database Connection
def create_connection():
    try:
        connection = pymysql.connect(
            host=str(st.secrets["AZ_db_host"]),
            user=str(st.secrets["AZ_db_user"]),
            password=str(st.secrets["AZ_db_password"]),
            database=str(st.secrets["AZ_db_name"]),
        )
        return connection
    except pymysql.MySQLError as e:
        st.error(f"Failed to connect to the database: {e}")
        return None

# Function to Fetch Employees
def fetch_employees():
    connection = create_connection()
    if connection:
        try:
            query = "SELECT * FROM employees WHERE isAvailable = True ORDER BY role, lastname ASC"
            df = pd.read_sql(query, connection)
            connection.close()
            return df
        except Exception as e:
            st.error(f"Failed to fetch employees: {e}")
    return pd.DataFrame()

# Function to Fetch Projects
def fetch_projects():
    connection = create_connection()
    if connection:
        try:
            query = "SELECT * FROM projects WHERE isActive = True ORDER BY dateStarted ASC"
            df = pd.read_sql(query, connection)
            connection.close()
            return df
        except Exception as e:
            st.error(f"Failed to fetch projects: {e}")
    return pd.DataFrame()

# Function to Assign Project to Employee
def assign_project(employee_id, project_id):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO project_assignments (employeeId, projectId) VALUES (%s, %s)"
                cursor.execute(query, (employee_id, project_id))
                connection.commit()
            st.success("Project assigned successfully!")
        except Exception as e:
            st.error(f"Failed to assign project: {e}")
        finally:
            connection.close()

# Function to Add New Project
def add_project(project_title):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                formatted_date = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                query = "INSERT INTO projects (projectTitle, dateStarted, isActive) VALUES (%s, %s, True)"
                cursor.execute(query, (project_title, formatted_date))
                connection.commit()
            st.success("Project added successfully!")
        except Exception as e:
            st.error(f"Failed to add project: {e}")
        finally:
            connection.close()

# Function to Delete (Close) Project
def delete_project(project_title):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                query = "UPDATE projects SET isActive = False WHERE projectTitle = %s"
                cursor.execute(query, (project_title,))
                connection.commit()
            st.success("Project closed successfully!")
        except Exception as e:
            st.error(f"Failed to close project: {e}")
        finally:
            connection.close()

# Fetch Employees and Projects
employees = fetch_employees()
projects = fetch_projects()

# Tabbed Interface
tabs = st.tabs(["Add Project", "View Projects", "View Employees", "Assign Project", "Close Project"])

# Tab 1: Add Project
with tabs[0]:
    st.header("Add New Project")
    project_title = st.text_input("Project Title")
    if st.button("Add Project"):
        if project_title:
            add_project(project_title)
        else:
            st.warning("Please enter a project title.")

# Tab 2: View Projects
with tabs[1]:
    st.header("Active Projects")
    if not projects.empty:
        st.dataframe(projects, use_container_width=True)
    else:
        st.warning("No projects available.")

# Tab 3: View Employees
with tabs[2]:
    st.header("Available Employees")
    
    uploaded_file = st.file_uploader("Upload a JSON file to filter based on your project's requirements", type="json")

    if uploaded_file is not None:
        # Load JSON file, and extract roles from the JSON data
        data = json.load(uploaded_file)
        needed_roles_obj = {value for value in data.values()}
        needed_roles_str = ", ".join(sorted(needed_roles_obj))
        st.write(f"#### Your project requires the following roles:")
        for i in needed_roles_obj:
            st.markdown("- " + i)
        

        # Filter employees based on the roles needed
        if not employees.empty:
            df_employee = pd.DataFrame(employees)
            selected_roles = st.selectbox("Filter available employees by role:", options=["All roles"] + list(df_employee["role"].unique()))
            filtered_employees = df_employee[df_employee["role"] == selected_roles]

            if selected_roles == "All roles":
                st.dataframe(df_employee, use_container_width=True)
            else:
                st.dataframe(filtered_employees, use_container_width=True)
        else:
            st.warning("No employees available.")

# Tab 4: Assign Project
with tabs[3]:
    st.header("Assign Project")
    if not employees.empty and not projects.empty:
        employee_id = st.selectbox(
            "Select Employee", 
            options=employees["id"], 
            format_func=lambda x: f"{employees.loc[employees['id'] == x, 'firstname'].values[0]} {employees.loc[employees['id'] == x, 'lastname'].values[0]} [{employees.loc[employees['id'] == x, 'role'].values[0]}]", 
            key="employee_id"
        )
        project_id = st.selectbox(
            "Select Project", 
            options=projects["id"], 
            format_func=lambda x: projects.loc[projects['id'] == x, 'projectTitle'].values[0], 
            key="project_id"
        )

        if st.button("Assign Project"):
            assign_project(employee_id, project_id)
    else:
        st.warning("No employees or projects available.")

# Tab 5: Close Project
with tabs[4]:
    st.header("Close Project")
    if not projects.empty:
        project_title = st.selectbox("Select Project", options=projects["projectTitle"])
        if st.button("Close Project"):
            delete_project(project_title)
    else:
        st.warning("No projects available.")
