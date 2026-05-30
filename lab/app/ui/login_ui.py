import customtkinter as ctk
from tkinter import messagebox
from ui.task_manager_ui import TaskManagerUI


class LoginUI(ctk.CTk):
    def __init__(self, auth_service, task_service):
        super().__init__()

        self.__auth_service = auth_service
        self.__task_service = task_service

        self.title("Task Manager - Login")
        self.geometry("500x420")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color="#f2f2f2")

        self.__create_widgets()

    def __create_widgets(self):
        title_label = ctk.CTkLabel(
            self,
            text="Task Manager",
            font=("Arial", 30, "bold"),
            text_color="#333333"
        )
        title_label.pack(pady=(35, 10))

        subtitle_label = ctk.CTkLabel(
            self,
            text="Autentificare utilizator",
            font=("Arial", 16),
            text_color="#666666"
        )
        subtitle_label.pack(pady=(0, 20))

        login_frame = ctk.CTkFrame(
            self,
            width=360,
            height=230,
            fg_color="white",
            corner_radius=8
        )
        login_frame.pack(pady=10)
        login_frame.pack_propagate(False)

        self.__username_entry = ctk.CTkEntry(
            login_frame,
            width=280,
            height=40,
            placeholder_text="Username"
        )
        self.__username_entry.pack(pady=(30, 15))

        self.__password_entry = ctk.CTkEntry(
            login_frame,
            width=280,
            height=40,
            placeholder_text="Parola",
            show="*"
        )
        self.__password_entry.pack(pady=(0, 20))

        login_button = ctk.CTkButton(
            login_frame,
            text="Login",
            width=280,
            height=40,
            fg_color="#4a90e2",
            hover_color="#357abd",
            command=self.__login
        )
        login_button.pack()

    def __login(self):
        username = self.__username_entry.get()
        password = self.__password_entry.get()

        user = self.__auth_service.login(username, password)

        if user is None:
            messagebox.showerror("Eroare", "Username sau parola gresita.")
            return

        self.destroy()

        app = TaskManagerUI(
            self.__task_service,
            user
        )
        app.mainloop()

        self.destroy()