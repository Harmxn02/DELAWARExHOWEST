import streamlit as st
import json
import mysql.connector
import pandas as pd

st.set_page_config(layout="wide", page_title="Find available employees")


st.title("Find available employees")
st.write("When you made the estimations, you were told which roles are needed for the project. Now you can find out which employees are available for these roles.")

uploaded_file = st.file_uploader("Choose a JSON file", type="json")



def get_db_connection():
    return mysql.connector.connect(
        host=str(st.secrets["AE_db_host"]),
        user=str(st.secrets["AE_db_user"]),
        password=str(st.secrets["AE_db_password"]),
        database=str(st.secrets["AE_db_name"])
    )



if uploaded_file is not None:
    # Load JSON file
    data = json.load(uploaded_file)
    
    # Extract roles from the JSON data
    needed_roles_obj = {value for value in data.values()}
    needed_roles_str = ", ".join(sorted(needed_roles_obj))
    
    # Display the roles needed
    # st.write(f"Needed roles: {needed_roles_str}")
    
    # Query the database for available employees whose role matches a needed role
    try:
        # Establish a connection to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Create a SQL query to find available employees with needed roles
        query = f"""
        SELECT firstname, lastname, email, role
        FROM employees
        WHERE role IN ({', '.join(['%s'] * len(needed_roles_obj))}) 
        AND isAvailable = TRUE
        """
        
        # Execute the query with the needed roles
        cursor.execute(query, list(needed_roles_obj))
        
        # Fetch all matching records
        employees = cursor.fetchall()
        
        # Display the results
        st.write("#### Available employees with the needed roles:")
        if employees:
            df = pd.DataFrame(employees)
            
            roles_to_filter = st.selectbox("Filter by role:", options=["All roles"] + list(df["role"].unique()))
            
            if roles_to_filter == "All roles":
                st.dataframe(df, height=35*len(df)+38, use_container_width=True)
            else:
                filtered_df = df[df["role"] == roles_to_filter]
                st.dataframe(filtered_df, height=35*len(filtered_df)+38, use_container_width=True)  # prints all rows
        
        else:
            st.write("No available employees found for the needed roles.")
        
        # Close the database connection
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")