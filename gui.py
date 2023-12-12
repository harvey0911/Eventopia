import tkinter as tk
from tkinter import messagebox
from user_operations import register_user, login_user
from event_operations import add_event, view_events, filter_events_by_date, filter_events_by_club, search_events

class GUI:
    def __init__(self, db):
        self.db = db
        self.root = tk.Tk()
        self.root.title("University Event Management System")
        self.root.geometry("800x600")

        self.setup_menu()
        self.initialize_frames()
        self.show_login_frame()

    def setup_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Login", command=self.show_login_frame)
        file_menu.add_command(label="Register", command=self.show_register_frame)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

    def initialize_frames(self):
        self.setup_login_frame()
        self.setup_register_frame()
        self.setup_sao_admin_frame()

    def show_login_frame(self):
        self.hide_all_frames()
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def show_register_frame(self):
        self.hide_all_frames()
        self.register_frame.pack(fill=tk.BOTH, expand=True)

    def setup_login_frame(self):
        self.login_frame = tk.Frame(self.root)
        tk.Label(self.login_frame, text="Username:").pack()
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_username.pack()
        tk.Label(self.login_frame, text="Password:").pack()
        self.entry_password = tk.Entry(self.login_frame, show="*")
        self.entry_password.pack()
        tk.Button(self.login_frame, text="Login", command=self.on_login).pack()

    def setup_register_frame(self):
        self.register_frame = tk.Frame(self.root)
        tk.Label(self.register_frame, text="First Name:").pack()
        self.entry_first_name = tk.Entry(self.register_frame)
        self.entry_first_name.pack()
        # ... add other registration fields in a similar manner
        tk.Button(self.register_frame, text="Register", command=self.on_register).pack()

    def setup_sao_admin_frame(self):
        self.sao_admin_frame = tk.Frame(self.root)
        tk.Label(self.sao_admin_frame, text="SAO Admin Panel").pack()
        # ... add SAO admin-specific fields and buttons
        # Example: Add Event button
        tk.Button(self.sao_admin_frame, text="Add Event", command=self.on_add_event).pack()

    def on_login(self):
        # ... login logic
        self.show_sao_admin_frame()

    def on_register(self):
        # ... registration logic
        pass

    def on_add_event(self):
        # ... add event logic
        pass

    def hide_all_frames(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.pack_forget()

    def run(self):
        self.root.mainloop()

# Example usage
# db = Database(...)
# app = GUI(db)
# app.run()
