import pandas as pd
from util.create_connection_to_db import create_connection

def fetch_projects():
    """
    Fetches active projects from the database.

    Returns:
        pd.DataFrame: A DataFrame containing the active projects, or an empty DataFrame if an error occurs.
    """
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

def assign_project(employee_id, project_id):
    """
    Assigns a project to an employee by inserting a record into the project_assignments table.

    Args:
        employee_id (int): The ID of the employee to whom the project is being assigned.
        project_id (int): The ID of the project being assigned.

    Raises:
        Exception: If there is an error during the database operation, an exception is raised and an error message is displayed.
    """
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

def add_project(project_title):
    """
    Adds a new project to the database with the given project title.

    Args:
        project_title (str): The title of the project to be added.

    Raises:
        Exception: If there is an error while adding the project to the database.
    """
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

def delete_project(project_title):
    """
    Marks a project as inactive in the database.

    Args:
        project_title (str): The title of the project to be marked as inactive.

    Raises:
        Exception: If there is an error while updating the project status in the database.
    """
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