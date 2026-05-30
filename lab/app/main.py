from repository.db_connection import DatabaseConnection
from repository.user_repository import UserRepository
from repository.task_repository import TaskRepository

from service.auth_service import AuthService
from service.task_service import TaskService

from ui.login_ui import LoginUI


def main():
    db_connection = DatabaseConnection()
    db_connection.create_tables()

    user_repository = UserRepository(db_connection)
    task_repository = TaskRepository(db_connection)

    auth_service = AuthService(user_repository)
    task_service = TaskService(task_repository)

    try:
        auth_service.register_user("admin", "admin123", "admin")
    except ValueError:
        pass

    try:
        auth_service.register_user("user", "user123", "user")
    except ValueError:
        pass

    app = LoginUI(auth_service, task_service)
    app.mainloop()


if __name__ == "__main__":
    main()