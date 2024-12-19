import pandas as pd
import pymysql
import json
from decimal import Decimal

from dotenv import load_dotenv
import os


load_dotenv()


def create_connection():
    """
    Establishes a connection to the MySQL database using credentials stored in Streamlit secrets.

    Returns:
        pymysql.connections.Connection: A connection object to the MySQL database if successful.
        None: If the connection attempt fails.

    Raises:
        pymysql.MySQLError: If there is an error connecting to the MySQL database.
    """
    try:
        connection = pymysql.connect(
            host=os.getenv("AZ_db_host"),
            user=os.getenv("AZ_db_user"),
            password=os.getenv("AZ_db_password"),
            database=os.getenv("AZ_db_name"),
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Failed to connect to the database: {e}")
        return None


def decimal_default(obj):
    """
    Converts Decimal objects to float for JSON serialization.
    """
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def fetch_roles_and_rates():
    """
    Fetches roles and daily rates from the database.
    
    Returns:
        json: A JSON object containing roles as keys and daily rates as values.
    """
    
    connection = create_connection()
    if connection:
        try:
            query = "SELECT role, rate FROM roles_rates"
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            
            roles_rates = {role: rate for role, rate in data}
            return json.dumps(roles_rates, default=decimal_default)
        except Exception as e:
            print(f"Failed to fetch roles and rates: {e}")
    return json.dumps({})

if __name__ == "__main__":
    results = fetch_roles_and_rates()
    
    print(results)
    
    with open("roles_rates.json", "w") as file:
        file.write(results)   
    
