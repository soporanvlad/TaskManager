from entity.user import User


class Admin(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)

    def __str__(self):
        return f"Admin(id={self.get_id()}, username={self.get_username()})"