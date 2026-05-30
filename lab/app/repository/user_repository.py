from entity.user import User
from entity.admin import Admin


class UserRepository:
    def __init__(self, db_connection):
        self.__db_connection = db_connection

    def add_user(self, username, password, role="user"):
        connection = self.__db_connection.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, role))

        connection.commit()
        connection.close()

    def find_by_username(self, username):
        connection = self.__db_connection.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, username, password, role
            FROM users
            WHERE username = ?
        """, (username,))

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        user_id, username, password, role = row

        if role == "admin":
            return Admin(user_id, username, password)

        return User(user_id, username, password)

    def get_all_users(self):
        connection = self.__db_connection.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, username, password, role
            FROM users
        """)

        rows = cursor.fetchall()
        connection.close()

        users = []

        for row in rows:
            user_id, username, password, role = row

            if role == "admin":
                users.append(Admin(user_id, username, password))
            else:
                users.append(User(user_id, username, password))

        return users