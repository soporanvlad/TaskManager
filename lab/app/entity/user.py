class User:
    def __init__(self, user_id, username, password):
        self.__id = user_id
        self.__username = username
        self.__password = password

    def get_id(self):
        return self.__id

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def __str__(self):
        return f"User(id={self.__id}, username={self.__username})"