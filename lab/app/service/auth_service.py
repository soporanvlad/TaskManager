class AuthService:
    def __init__(self, user_repository):
        self.__user_repository = user_repository

    def login(self, username, password):
        user = self.__user_repository.find_by_username(username)

        if user is None:
            return None

        if user.get_password() != password:
            return None

        return user

    def register_user(self, username, password, role="user"):
        if username == "" or password == "":
            raise ValueError("Username si parola nu pot fi goale.")

        existing_user = self.__user_repository.find_by_username(username)

        if existing_user is not None:
            raise ValueError("Exista deja un utilizator cu acest username.")

        self.__user_repository.add_user(username, password, role)