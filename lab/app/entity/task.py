class Task:
    def __init__(self, task_id, user_id, title, description, deadline, priority, category, status=False):
        self.__id = task_id
        self.__user_id = user_id
        self.__title = title
        self.__description = description
        self.__deadline = deadline
        self.__priority = priority
        self.__category = category
        self.__status = status

    def get_id(self):
        return self.__id

    def get_user_id(self):
        return self.__user_id

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_deadline(self):
        return self.__deadline

    def get_priority(self):
        return self.__priority

    def get_category(self):
        return self.__category

    def get_status(self):
        return self.__status

    def set_title(self, title):
        self.__title = title

    def set_description(self, description):
        self.__description = description

    def set_deadline(self, deadline):
        self.__deadline = deadline

    def set_priority(self, priority):
        self.__priority = priority

    def set_category(self, category):
        self.__category = category

    def set_status(self, status):
        self.__status = status

    def __str__(self):
        status_text = "finalizata" if self.__status else "nefinalizata"
        return f"{self.__id}. {self.__title} - {self.__priority} - {self.__category} - {status_text}"