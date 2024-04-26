from snowflake.connector import connect
from flask import current_app

class User:

    from snowflake.connector import connect  # Assuming Snowflake connection

class User:
    # ... other user model attributes (email, password, etc.)

    def __init__(self, username, email, password, city=None, is_active=True):
        self.username = username
        self.email = email
        self.password = password  # Assuming hashed password (implement security!)
        self.city = city
        self.is_active = is_active  # New attribute (if needed)

    @classmethod
    def get_by_email(cls, email):
        conn_params = get_snowflake_connection_params(current_app.config['SNOWFLAKE'])
        conn = connect(**conn_params)
        cursor = conn.cursor()

        # Replace with your specific query to fetch user by email
        cursor.execute("SELECT * FROM ESKO.PUBLIC.USER_TABLE WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        return User(*user) if user else None
    
    def get_id(self):
       return self.id 
        


    @staticmethod
    def create_user(username, email, password, city):
        try:
            conn_params = get_snowflake_connection_params(current_app.config['SNOWFLAKE'])
            conn = connect(**conn_params)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ESKO.PUBLIC.USER_TABLE (username, email, password, city)
                VALUES (%s, %s, %s, %s)
            """, (username, email, password, city))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f'Error creating user: {str(e)}')
            return False





def get_snowflake_connection_params(snowflake_config):
    """
    Retrieves Snowflake connection parameters from the provided dictionary.

    Args:
        snowflake_config (dict): A dictionary containing Snowflake connection details.

    Returns:
        A dictionary containing Snowflake connection parameters.
    """

    return {
        'account': snowflake_config['account'],
        'user': snowflake_config['user'],
        'password': snowflake_config['password'],
        'warehouse': snowflake_config.get('warehouse', None),
        'database': snowflake_config.get('database', None),
    }
