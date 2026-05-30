from entity.task import Task


class TaskService:
    def __init__(self, task_repository):
        self.__task_repository = task_repository

    def create_task(self, user_id, title, description, deadline, priority, category):
        if title == "":
            raise ValueError("Titlul nu poate fi gol.")

        task = Task(
            None,
            user_id,
            title,
            description,
            deadline,
            priority,
            category,
            False
        )

        self.__task_repository.add_task(task)

    def get_user_tasks(self, user_id):
        return self.__task_repository.get_tasks_by_user_id(user_id)

    def update_task(self, task_id, user_id, title, description, deadline, priority, category, status):
        if title == "":
            raise ValueError("Titlul nu poate fi gol.")

        task = Task(
            task_id,
            user_id,
            title,
            description,
            deadline,
            priority,
            category,
            status
        )

        self.__task_repository.update_task(task)

    def delete_task(self, task_id):
        task = self.__task_repository.find_by_id(task_id)

        if task is None:
            raise ValueError("Task-ul nu exista.")

        self.__task_repository.delete_task(task_id)

    def toggle_status(self, task_id):
        task = self.__task_repository.find_by_id(task_id)

        if task is None:
            raise ValueError("Task-ul nu exista.")

        task.set_status(not task.get_status())
        self.__task_repository.update_task(task)

    def filter_tasks(self, user_id, category=None, status=None, priority=None):
        tasks = self.__task_repository.get_tasks_by_user_id(user_id)
        filtered_tasks = []

        for task in tasks:
            matches_category = True
            matches_status = True
            matches_priority = True

            if category is not None and category != "Toate":
                matches_category = task.get_category() == category

            if status is not None and status != "Toate":
                if status == "Finalizate":
                    matches_status = task.get_status() is True
                elif status == "Nefinalizate":
                    matches_status = task.get_status() is False

            if priority is not None and priority != "Toate":
                matches_priority = task.get_priority() == priority

            if matches_category and matches_status and matches_priority:
                filtered_tasks.append(task)

        return filtered_tasks