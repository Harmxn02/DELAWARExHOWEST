import pandas as pd
from util.create_connection_to_db import create_connection

def fetch_employees():
    """
    Fetches a list of available employees from the database.

    Returns:
        pd.DataFrame: A DataFrame containing the list of available employees, ordered by role and last name. 
                      If an error occurs, an empty DataFrame is returned.
    """
    connection = create_connection()
    if connection:
        try:
            query = "SELECT * FROM employees WHERE isAvailable = True ORDER BY role, lastname ASC"
            df = pd.read_sql(query, connection)
            connection.close()
            return df
        except Exception as e:
            print(f"Failed to fetch employees: {e}")
    return pd.DataFrame()
