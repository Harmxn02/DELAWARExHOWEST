from create_connection_to_db import create_connection

import pandas as pd
import json
from decimal import Decimal


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