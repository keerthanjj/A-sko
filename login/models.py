from snowflake.connector import connect
from flask import current_app


class User:
    def __init__(self, user_id, username, email, ph_number, password, city=None,is_active=True):
        self.user_id= user_id
        self.username = username
        self.email = email
        self.ph_number = ph_number
        self.password = password
        self.city = city
        self.is_active=is_active

    def get_id(self):
        return self.user_id

    @staticmethod
    def create_user(username, email, ph_number, password, city):
        try:
            conn_params = get_snowflake_connection_params(current_app.config['SNOWFLAKE'])
            conn = connect(**conn_params)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ESKO.PUBLIC.USERS (username, email, ph_number, password, city)
                VALUES (%s, %s, %s, %s, %s)
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

        # Cast the email parameter to a string before passing it to the query
        email = str(email)

        # Use a parameterized query to avoid SQL injection and type conversion issues
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
