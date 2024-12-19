import pymysql
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
