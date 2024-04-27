from snowflake.connector import connect
from flask import current_app


class User:
    def __init__(self,ID, username, email, ph_number, password, city=None):
        self.ID=ID
        self.username = username
        self.email = email
        self.ph_number = ph_number
        self.password = password
        self.city = city

    @staticmethod
    def create_user(username, email, ph_number, password, city):
        try:
            conn_params = get_snowflake_connection_params(current_app.config['SNOWFLAKE'])
            conn = connect(**conn_params)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ESKO.PUBLIC.USERS (username, email, ph_number, password, city)
                VALUES (%s, %s, CAST(%s AS NUMBER), %s, %s)
            """, (username, email, ph_number, password, city))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            # Consider raising a specific exception or logging the error more robustly
            print(f'Error creating user: {str(e)}')
            return False

    @classmethod
    def get_by_email(cls, email):
        conn_params = get_snowflake_connection_params(current_app.config['SNOWFLAKE'])
        conn = connect(**conn_params)
        cursor = conn.cursor()

        # Replace with your specific query to fetch user by email
        cursor.execute("SELECT * FROM ESKO.PUBLIC.USERS WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        return User(*user) if user else None




def get_snowflake_connection_params(snowflake_config):
    return {
        'account': snowflake_config['account'],
        'user': snowflake_config['user'],
        'password': snowflake_config['password'],
        'warehouse': snowflake_config.get('warehouse', None),
        'database': snowflake_config.get('database', None),
    }
