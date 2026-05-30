from entity.task import Task


class TaskRepository:
    def __init__(self, db_connection):
        self.__db_connection = db_connection

    def add_task(self, task):
        connection = self.__db_connection.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO tasks (
                user_id, title, description, deadline, priority, category, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            task.get_user_id(),
            task.get_title(),
            task.get_description(),
            task.get_deadline(),
            task.get_priority(),
            task.get_category(),
            int(task.get_status())
        ))

        connection.commit()
        connection.close()

    def get_tasks_by_user_id(self, user_id):
        connection = self.__db_connection.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, user_id, title, description, deadline, priority, category, status
            FROM tasks
            WHERE user_id = ?
        """, (user_id,))

        rows = cursor.fetchall()
        connection.close()

        tasks = []

        for row in rows:
            task_id, user_id, title, description, deadline, priority, category, status = row

            tasks.append(Task(
                task_id,
                user_id,
                title,
                description,
                deadline,
                priority,
                category,
                bool(status)
            ))

        return tasks

    def update_task(self, task):
        connection = self.__db_connection.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE tasks
            SET title = ?,
                description = ?,
                deadline = ?,
                priority = ?,
                category = ?,
                status = ?
            WHERE id = ?
        """, (
            task.get_title(),
            task.get_description(),
            task.get_deadline(),
            task.get_priority(),
            task.get_category(),
            int(task.get_status()),
            task.get_id()
        ))

        connection.commit()
        connection.close()

    def delete_task(self, task_id):
        connection = self.__db_connection.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM tasks
            WHERE id = ?
        """, (task_id,))

        connection.commit()
        connection.close()

    def find_by_id(self, task_id):
        connection = self.__db_connection.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, user_id, title, description, deadline, priority, category, status
            FROM tasks
            WHERE id = ?
        """, (task_id,))

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        task_id, user_id, title, description, deadline, priority, category, status = row

        return Task(
            task_id,
            user_id,
            title,
            description,
            deadline,
            priority,
            category,
            bool(status)
        )