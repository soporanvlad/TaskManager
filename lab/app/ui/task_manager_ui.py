import customtkinter as ctk
from tkinter import ttk, messagebox


class TaskManagerUI(ctk.CTk):
    def __init__(self, task_service, user):
        super().__init__()

        self.__task_service = task_service
        self.__user = user
        self.__selected_task_id = None

        self.title("Task Manager")
        self.geometry("1250x760")
        self.configure(fg_color="#f2f2f2")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.__create_layout()
        self.__load_tasks()

    def __create_layout(self):
        self.__sidebar = ctk.CTkFrame(self, width=300, fg_color="#f7f7f7", corner_radius=0)
        self.__sidebar.pack(side="left", fill="y", padx=(15, 5), pady=15)
        self.__sidebar.pack_propagate(False)

        self.__content = ctk.CTkFrame(self, fg_color="white", corner_radius=3)
        self.__content.pack(side="right", fill="both", expand=True, padx=(5, 15), pady=15)

        self.__create_sidebar()
        self.__create_content()

    def __create_sidebar(self):
        title = ctk.CTkLabel(
            self.__sidebar,
            text=f"Bun venit, {self.__user.get_username()}",
            font=("Arial", 20, "bold"),
            text_color="#333333"
        )
        title.pack(pady=(20, 25))

        btn_all = ctk.CTkButton(
            self.__sidebar,
            text="Toate Sarcinile",
            height=45,
            fg_color="#4a90e2",
            hover_color="#357abd",
            command=self.__load_tasks
        )
        btn_all.pack(fill="x", padx=20, pady=8)

        btn_work = ctk.CTkButton(
            self.__sidebar,
            text="Sarcini de Muncă",
            height=45,
            fg_color="transparent",
            text_color="#555555",
            hover_color="#e6e6e6",
            command=lambda: self.__apply_filter(category="Muncă")
        )
        btn_work.pack(fill="x", padx=20, pady=8)

        btn_school = ctk.CTkButton(
            self.__sidebar,
            text="Sarcini de Școală",
            height=45,
            fg_color="transparent",
            text_color="#555555",
            hover_color="#e6e6e6",
            command=lambda: self.__apply_filter(category="Școală")
        )
        btn_school.pack(fill="x", padx=20, pady=8)

        btn_personal = ctk.CTkButton(
            self.__sidebar,
            text="Sarcini Personale",
            height=45,
            fg_color="transparent",
            text_color="#555555",
            hover_color="#e6e6e6",
            command=lambda: self.__apply_filter(category="Personal")
        )
        btn_personal.pack(fill="x", padx=20, pady=8)

        btn_done = ctk.CTkButton(
            self.__sidebar,
            text="Sarcini Finalizate",
            height=45,
            fg_color="transparent",
            text_color="#555555",
            hover_color="#e6e6e6",
            command=lambda: self.__apply_filter(status="Finalizate")
        )
        btn_done.pack(fill="x", padx=20, pady=8)

        separator = ctk.CTkFrame(self.__sidebar, height=2, fg_color="#dddddd")
        separator.pack(fill="x", padx=20, pady=(25, 15))

        filter_title = ctk.CTkLabel(
            self.__sidebar,
            text="Filtrare",
            font=("Arial", 18, "bold"),
            text_color="#333333"
        )
        filter_title.pack(anchor="w", padx=25, pady=(0, 15))

        self.__category_filter = ctk.CTkOptionMenu(
            self.__sidebar,
            values=["Toate", "Școală", "Muncă", "Personal", "Cumpărături"],
            width=240
        )
        self.__category_filter.set("Toate")
        self.__category_filter.pack(padx=20, pady=8)

        self.__priority_filter = ctk.CTkOptionMenu(
            self.__sidebar,
            values=["Toate", "Scăzută", "Medie", "Ridicată"],
            width=240
        )
        self.__priority_filter.set("Toate")
        self.__priority_filter.pack(padx=20, pady=8)

        self.__status_filter = ctk.CTkOptionMenu(
            self.__sidebar,
            values=["Toate", "Finalizate", "Nefinalizate"],
            width=240
        )
        self.__status_filter.set("Toate")
        self.__status_filter.pack(padx=20, pady=8)

        filter_button = ctk.CTkButton(
            self.__sidebar,
            text="Aplică Filtre",
            height=40,
            fg_color="#4a90e2",
            hover_color="#357abd",
            command=self.__filter_from_sidebar
        )
        filter_button.pack(fill="x", padx=20, pady=(15, 8))

    def __create_content(self):
        top_frame = ctk.CTkFrame(self.__content, fg_color="white")
        top_frame.pack(fill="x", padx=20, pady=(20, 10))

        add_button = ctk.CTkButton(
            top_frame,
            text="+ Adaugă Sarcină",
            width=220,
            height=45,
            fg_color="#4a90e2",
            hover_color="#357abd",
            command=self.__open_add_window
        )
        add_button.pack(side="left")

        columns = ("id", "title", "category", "priority", "deadline", "status")

        self.__tree = ttk.Treeview(
            self.__content,
            columns=columns,
            show="headings",
            height=18
        )

        self.__tree.heading("id", text="ID")
        self.__tree.heading("title", text="Titlu")
        self.__tree.heading("category", text="Categorie")
        self.__tree.heading("priority", text="Prioritate")
        self.__tree.heading("deadline", text="Termen limită")
        self.__tree.heading("status", text="Status")

        self.__tree.column("id", width=50)
        self.__tree.column("title", width=220)
        self.__tree.column("category", width=140)
        self.__tree.column("priority", width=130)
        self.__tree.column("deadline", width=140)
        self.__tree.column("status", width=150)

        self.__tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.__tree.bind("<<TreeviewSelect>>", self.__select_task)

        bottom_frame = ctk.CTkFrame(self.__content, fg_color="white")
        bottom_frame.pack(fill="x", padx=20, pady=(10, 20))

        edit_button = ctk.CTkButton(
            bottom_frame,
            text="✎ Editează Sarcina",
            width=220,
            height=45,
            fg_color="#4a90e2",
            hover_color="#357abd",
            command=self.__open_edit_window
        )
        edit_button.pack(side="left", padx=10)

        delete_button = ctk.CTkButton(
            bottom_frame,
            text="✕ Șterge Sarcina",
            width=220,
            height=45,
            fg_color="#ffffff",
            text_color="#cc5555",
            border_width=1,
            border_color="#cccccc",
            hover_color="#eeeeee",
            command=self.__delete_task
        )
        delete_button.pack(side="left", padx=10)

        done_button = ctk.CTkButton(
            bottom_frame,
            text="✓ Marchează / Demarchează",
            width=260,
            height=45,
            fg_color="#78c26d",
            hover_color="#5ea855",
            command=self.__toggle_status
        )
        done_button.pack(side="left", padx=10)

    def __load_tasks(self):
        tasks = self.__task_service.get_user_tasks(self.__user.get_id())
        self.__populate_table(tasks)

    def __populate_table(self, tasks):
        for row in self.__tree.get_children():
            self.__tree.delete(row)

        for task in tasks:
            status_text = "Finalizată" if task.get_status() else "Nefinalizată"

            self.__tree.insert(
                "",
                "end",
                values=(
                    task.get_id(),
                    task.get_title(),
                    task.get_category(),
                    task.get_priority(),
                    task.get_deadline(),
                    status_text
                )
            )

    def __select_task(self, event):
        selected = self.__tree.selection()

        if selected:
            values = self.__tree.item(selected[0], "values")
            self.__selected_task_id = int(values[0])

    def __filter_from_sidebar(self):
        category = self.__category_filter.get()
        priority = self.__priority_filter.get()
        status = self.__status_filter.get()

        tasks = self.__task_service.filter_tasks(
            self.__user.get_id(),
            category,
            status,
            priority
        )

        self.__populate_table(tasks)

    def __apply_filter(self, category=None, status=None):
        tasks = self.__task_service.filter_tasks(
            self.__user.get_id(),
            category=category,
            status=status,
            priority=None
        )

        self.__populate_table(tasks)

    def __open_add_window(self):
        self.__open_task_form("Adaugă Sarcină")

    def __open_edit_window(self):
        if self.__selected_task_id is None:
            messagebox.showwarning("Atenție", "Selectează o sarcină.")
            return

        self.__open_task_form("Editează Sarcină", self.__selected_task_id)

    def __open_task_form(self, title, task_id=None):
        form = ctk.CTkToplevel(self)
        form.title(title)
        form.geometry("420x520")
        form.resizable(False, False)
        form.configure(fg_color="#f2f2f2")

        title_entry = ctk.CTkEntry(form, width=320, placeholder_text="Titlu")
        title_entry.pack(pady=(30, 10))

        description_entry = ctk.CTkEntry(form, width=320, placeholder_text="Descriere")
        description_entry.pack(pady=10)

        deadline_entry = ctk.CTkEntry(form, width=320, placeholder_text="Termen limită")
        deadline_entry.pack(pady=10)

        priority_menu = ctk.CTkOptionMenu(
            form,
            values=["Scăzută", "Medie", "Ridicată"],
            width=320
        )
        priority_menu.set("Medie")
        priority_menu.pack(pady=10)

        category_menu = ctk.CTkOptionMenu(
            form,
            values=["Școală", "Muncă", "Personal", "Cumpărături"],
            width=320
        )
        category_menu.set("Personal")
        category_menu.pack(pady=10)

        status_menu = ctk.CTkOptionMenu(
            form,
            values=["Nefinalizată", "Finalizată"],
            width=320
        )
        status_menu.set("Nefinalizată")
        status_menu.pack(pady=10)

        if task_id is not None:
            task = self.__task_service._TaskService__task_repository.find_by_id(task_id)

            if task is not None:
                title_entry.insert(0, task.get_title())
                description_entry.insert(0, task.get_description())
                deadline_entry.insert(0, task.get_deadline())
                priority_menu.set(task.get_priority())
                category_menu.set(task.get_category())
                status_menu.set("Finalizată" if task.get_status() else "Nefinalizată")

        save_button = ctk.CTkButton(
            form,
            text="Salvează",
            width=320,
            height=42,
            fg_color="#4a90e2",
            hover_color="#357abd",
            command=lambda: self.__save_task(
                form,
                task_id,
                title_entry.get(),
                description_entry.get(),
                deadline_entry.get(),
                priority_menu.get(),
                category_menu.get(),
                status_menu.get()
            )
        )
        save_button.pack(pady=25)

    def __save_task(self, form, task_id, title, description, deadline, priority, category, status_text):
        try:
            status = status_text == "Finalizată"

            if task_id is None:
                self.__task_service.create_task(
                    self.__user.get_id(),
                    title,
                    description,
                    deadline,
                    priority,
                    category
                )
            else:
                self.__task_service.update_task(
                    task_id,
                    self.__user.get_id(),
                    title,
                    description,
                    deadline,
                    priority,
                    category,
                    status
                )

            form.destroy()
            self.__load_tasks()

        except ValueError as error:
            messagebox.showerror("Eroare", str(error))

    def __delete_task(self):
        if self.__selected_task_id is None:
            messagebox.showwarning("Atenție", "Selectează o sarcină.")
            return

        confirm = messagebox.askyesno("Confirmare", "Sigur vrei să ștergi sarcina?")

        if confirm:
            self.__task_service.delete_task(self.__selected_task_id)
            self.__selected_task_id = None
            self.__load_tasks()

    def __toggle_status(self):
        if self.__selected_task_id is None:
            messagebox.showwarning("Atenție", "Selectează o sarcină.")
            return

        self.__task_service.toggle_status(self.__selected_task_id)
        self.__load_tasks()