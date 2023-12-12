import tkinter as tk
from tkinter import messagebox
import psycopg2

# Database connection setup
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'
DB_HOST = 'localhost'
DB_PORT = '5432'

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

# Create the "SAOadmin" table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS sao_admins (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL
    );
''')

# Create the "events" table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        event_name VARCHAR(100) NOT NULL,
        event_date DATE,
        event_location VARCHAR(100),
        event_club VARCHAR(100),   
        sao_admin_id INTEGER REFERENCES sao_admins(id)
    );
''')

# Create the "students" table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        date_of_birth DATE,
        email VARCHAR(100),
        contact_number VARCHAR(20),
        country VARCHAR(100),
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL
    );
''')

# Create the "staff" table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        date_of_birth DATE,
        email VARCHAR(100),
        contact_number VARCHAR(20),
        country VARCHAR(100),
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL
    );
''')

# Create the "faculty" table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS faculty (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        date_of_birth DATE,
        email VARCHAR(100),
        contact_number VARCHAR(20),
        country VARCHAR(100),
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL
    );
''')

# Create the "attendance" table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        p_id INTEGER REFERENCES students(id),
        event_id INTEGER REFERENCES events(id),
        n_of_attendee INTEGER,
        PRIMARY KEY (p_id, event_id)
    );
''')

conn.commit()

# Rest of your code...

# Function to register a new user
def register_user(user_type):
    def register():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        date_of_birth = entry_date_of_birth.get()
        email = entry_email.get()
        contact_number = entry_contact_number.get()
        country = entry_country.get()
        username = entry_username.get()
        password = entry_password.get()

        if not first_name or not last_name or not date_of_birth or not username or not password:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        try:
            if user_type == "student":
                cur.execute(
                    "INSERT INTO students (first_name, last_name, date_of_birth, email, contact_number, country, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                    (first_name, last_name, date_of_birth, email, contact_number, country, username, password)
                )
            elif user_type == "staff":
                cur.execute(
                    "INSERT INTO staff (first_name, last_name, date_of_birth, email, contact_number, country, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                    (first_name, last_name, date_of_birth, email, contact_number, country, username, password)
                )
            elif user_type == "faculty":
                cur.execute(
                    "INSERT INTO faculty (first_name, last_name, date_of_birth, email, contact_number, country, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                    (first_name, last_name, date_of_birth, email, contact_number, country, username, password)
            
                )
            elif user_type == "SAOadmin":
                cur.execute(
                    "INSERT INTO sao_admins (username, password) VALUES (%s, %s);",
                    (username, password)
            
                )

            conn.commit()
            messagebox.showinfo("Success", "User registered successfully.")
            top.destroy()
        except psycopg2.Error as e:
            messagebox.showerror("Database Error", str(e))

    top = tk.Toplevel()
    top.title(f"Register {user_type.capitalize()}")
    top.geometry("400x400")

    label_first_name = tk.Label(top, text="First Name:", font=label_font)
    label_first_name.pack()
    entry_first_name = tk.Entry(top, font=entry_font)
    entry_first_name.pack()

    label_last_name = tk.Label(top, text="Last Name:", font=label_font)
    label_last_name.pack()
    entry_last_name = tk.Entry(top, font=entry_font)
    entry_last_name.pack()

    label_date_of_birth = tk.Label(top, text="Date of Birth (YYYY-MM-DD):", font=label_font)
    label_date_of_birth.pack()
    entry_date_of_birth = tk.Entry(top, font=entry_font)
    entry_date_of_birth.pack()

    label_email = tk.Label(top, text="Email:", font=label_font)
    label_email.pack()
    entry_email = tk.Entry(top, font=entry_font)
    entry_email.pack()

    label_contact_number = tk.Label(top, text="Contact Number:", font=label_font)
    label_contact_number.pack()
    entry_contact_number = tk.Entry(top, font=entry_font)
    entry_contact_number.pack()

    label_country = tk.Label(top, text="Country:", font=label_font)
    label_country.pack()
    entry_country = tk.Entry(top, font=entry_font)
    entry_country.pack()

    label_username = tk.Label(top, text="Username:", font=label_font)
    label_username.pack()
    entry_username = tk.Entry(top, font=entry_font)
    entry_username.pack()

    label_password = tk.Label(top, text="Password:", font=label_font)
    label_password.pack()
    entry_password = tk.Entry(top, show="*", font=entry_font)
    entry_password.pack()

    btn_register = tk.Button(top, text="Register", command=register, font=button_font, bg=button_color, fg="white")
    btn_register.pack(pady=10)


# Function to log in to the application
def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    # Check if the user is an SAO admin
    cur.execute("SELECT * FROM sao_admins WHERE username = %s AND password = %s;", (username, password))
    sao_admin = cur.fetchone()

    if sao_admin:
        messagebox.showinfo("Success", "Logged in as SAO admin.")
        enable_sao_admin_functionality()
    else:
        messagebox.showinfo("Success", "Logged in as normal user.")
        enable_normal_user_functionality()


def enable_sao_admin_functionality():
    login_frame.pack_forget()
    sao_admin_frame.pack()


def enable_normal_user_functionality():
    login_frame.pack_forget()
    normal_user_frame.pack()


# Function to add an event to the database
def add_event():
    event_name = entry_event_name.get()
    event_date = entry_event_date.get()
    event_location = entry_event_location.get()
    event_club = entry_event_club.get()
    

    if not event_name or not event_date:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    try:
        # Get the SAO admin ID to associate the event with the admin
        cur.execute("SELECT id FROM sao_admins WHERE username = %s;", (entry_username.get(),))
        sao_admin_id = cur.fetchone()[0]
        
        cur.execute("INSERT INTO events (event_name, event_date, event_location, event_club, sao_admin_id) VALUES (%s, %s, %s, %s , %s);", (event_name, event_date, event_location, event_club, sao_admin_id) )
        conn.commit()
        messagebox.showinfo("Success", "Event added successfully.")
        entry_event_name.delete(0, tk.END)
        entry_event_date.delete(0, tk.END)
        entry_event_location.delete(0, tk.END)
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))


#Fun

# Function to view all events from the database
def view_events():
    try:
        cur.execute("SELECT * FROM events")
        rows = cur.fetchall()

        if not rows:
            messagebox.showinfo("No Events", "No events found.")
        else:
            result_text = ""
            for row in rows:
                result_text += f"Event ID: {row[0]}, Name: {row[1]}, Date: {row[2]}, Location: {row[3]}\n"
            messagebox.showinfo("Events", result_text)
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))

# Function to filter events by date
def filter_events_by_date():
    date = entry_filter_date.get()
    if not date:
        messagebox.showerror("Error", "Please enter a date.")
        return

    try:
        cur.execute("SELECT * FROM events WHERE event_date = %s;", (date,))
        rows = cur.fetchall()

        if not rows:
            messagebox.showinfo("No Events", "No events found for the specified date.")
        else:
            result_text = ""
            for row in rows:
                result_text += f"Event ID: {row[0]}, Name: {row[1]}, Date: {row[2]}, Location: {row[3]}\n"
            messagebox.showinfo("Events", result_text)
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))



def Register_by_id():
    try:
        event_id = entry_register_event.get()
        username = entry_username.get()

        cur.execute("SELECT id FROM students WHERE username = %s", (username,))  
        student_data = cur.fetchone()

        if not student_data:
            messagebox.showerror("Error", "Student not found.")
            return

        student_id = student_data[0]

        cur.execute("INSERT INTO attendance (p_id, event_id) VALUES (%s, %s);", (student_id, event_id))
        conn.commit()
        messagebox.showinfo("Success", "Successfully registered for the event.")
    except psycopg2.Error as e:
        messagebox.showerror("Error", "Couldn't register you for this event: " + str(e))





def filter_events_by_club():
    club_name = entry_filter_club.get()
    if not club_name:
        messagebox.showerror("Error", "Please enter a club name.")
        return

    try:
        cur.execute("SELECT * FROM events WHERE event_club = %s;", (club_name,))
        rows = cur.fetchall()

        if not rows:
            messagebox.showinfo("No Events", "No events found for the specified club.")
        else:
            result_text = ""
            for row in rows:
                result_text += f"Event ID: {row[0]}, Name: {row[1]}, Date: {row[2]}, Location: {row[3]}\n"
            messagebox.showinfo("Events", result_text)
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))
def search_events():
    search_text = entry_search.get()
    if not search_text:
        messagebox.showerror("Error", "Please enter a search query.")
        return

    try:
        cur.execute("SELECT * FROM events WHERE event_name ILIKE %s OR event_club ILIKE %s;", (f"%{search_text}%", f"%{search_text}%"))
        rows = cur.fetchall()

        if not rows:
            messagebox.showinfo("No Events", "No matching events found.")
        else:
            result_text = ""
            for row in rows:
                result_text += f"Event ID: {row[0]}, Name: {row[1]}, Date: {row[2]}, Location: {row[3]}\n"
            messagebox.showinfo("Search Results", result_text)
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))


root = tk.Tk()
root.title("University Event Management")
root.geometry("400x400")

# GUI elements
background_color = "#F0F0F0"
button_color = "#4CAF50"
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 12)
button_font = ("Helvetica", 12, "bold")

main_frame = tk.Frame(root, bg=background_color)
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = tk.Label(main_frame, text="University Event Management", font=label_font, bg=background_color)
title_label.pack(pady=10)

# Login Section
login_frame = tk.Frame(main_frame, bg=background_color)
login_frame.pack(pady=20)

label_username = tk.Label(login_frame, text="Username:", font=label_font, bg=background_color)
label_username.pack()
entry_username = tk.Entry(login_frame, font=entry_font)
entry_username.pack()

label_password = tk.Label(login_frame, text="Password:", font=label_font, bg=background_color)
label_password.pack()
entry_password = tk.Entry(login_frame, show="*", font=entry_font)
entry_password.pack()

btn_login = tk.Button(login_frame, text="Login", command=login, font=button_font, bg=button_color, fg="white")
btn_login.pack(pady=10)

# Registration Button
btn_register_student = tk.Button(login_frame, text="Register as Student", command=lambda: register_user("student"), font=button_font, bg=button_color, fg="white")
btn_register_student.pack(pady=5)

btn_register_staff = tk.Button(login_frame, text="Register as Staff", command=lambda: register_user("staff"), font=button_font, bg=button_color, fg="white")
btn_register_staff.pack(pady=5)

btn_register_faculty = tk.Button(login_frame, text="Register as Faculty", command=lambda: register_user("faculty"), font=button_font, bg=button_color, fg="white")
btn_register_faculty.pack(pady=5)

btn_register_faculty = tk.Button(login_frame, text="Register as SAO ADMIN", command=lambda: register_user("SAOadmin"), font=button_font, bg=button_color, fg="white")
btn_register_faculty.pack(pady=5)


# SAO Admin Functionality
sao_admin_frame = tk.Frame(main_frame, bg=background_color)

label_event_name = tk.Label(sao_admin_frame, text="Event Name:", font=label_font, bg=background_color)
label_event_name.pack()
entry_event_name = tk.Entry(sao_admin_frame, font=entry_font)
entry_event_name.pack()

label_event_date = tk.Label(sao_admin_frame, text="Event Date (YYYY-MM-DD):", font=label_font, bg=background_color)
label_event_date.pack()
entry_event_date = tk.Entry(sao_admin_frame, font=entry_font)
entry_event_date.pack()

label_event_location = tk.Label(sao_admin_frame, text="Event Location:", font=label_font, bg=background_color)
label_event_location.pack()
entry_event_location = tk.Entry(sao_admin_frame, font=entry_font)
entry_event_location.pack()

label_event_club = tk.Label(sao_admin_frame, text="Event Club:", font=label_font, bg=background_color)
label_event_club.pack()
entry_event_club = tk.Entry(sao_admin_frame, font=entry_font)
entry_event_club.pack()

btn_add_event = tk.Button(sao_admin_frame, text="Add Event", command=add_event, font=button_font, bg=button_color, fg="white")
btn_add_event.pack(pady=10)

# Entry and button to search events by event name or club name
label_search = tk.Label(sao_admin_frame, text="Search Events by Event Name or Club Name:", font=label_font, bg=background_color)
label_search.pack()
entry_search = tk.Entry(sao_admin_frame, font=entry_font)
entry_search.pack()
btn_search = tk.Button(sao_admin_frame, text="Search", command=search_events, font=button_font, bg=button_color, fg="white")
btn_search.pack(pady=5)

# Button to view all events
btn_view_events = tk.Button(sao_admin_frame, text="View All Events", command=view_events, font=button_font, bg=button_color, fg="white")
btn_view_events.pack(pady=5)

sao_admin_frame.pack_forget()



# Normal User Functionality


normal_user_frame = tk.Frame(main_frame, bg=background_color)

# Button to view all events
btn_view_events = tk.Button(normal_user_frame, text="View All Events", command=view_events, font=button_font, bg=button_color, fg="white")
btn_view_events.pack(pady=5)


# Entry and button to Register to an  events by id

label_register_event= tk.Label(normal_user_frame, text="Enter the id of the event you want to register to ", font=label_font, bg=background_color)
label_register_event.pack()
entry_register_event = tk.Entry(normal_user_frame, font=entry_font)
entry_register_event.pack()
btn_register_by_event_id = tk.Button(normal_user_frame, text="Register", command=Register_by_id, font=button_font, bg=button_color, fg="white")
btn_register_by_event_id.pack(pady=5)




# Entry and button to filter events by date
label_filter_date = tk.Label(normal_user_frame, text="Filter Events by Date (YYYY-MM-DD):", font=label_font, bg=background_color)
label_filter_date.pack()
entry_filter_date = tk.Entry(normal_user_frame, font=entry_font)
entry_filter_date.pack()
btn_filter_by_date = tk.Button(normal_user_frame, text="Filter", command=filter_events_by_date, font=button_font, bg=button_color, fg="white")
btn_filter_by_date.pack(pady=5)

# Entry and button to filter events by club
label_filter_club = tk.Label(normal_user_frame, text="Filter Events by Club:", font=label_font, bg=background_color)
label_filter_club.pack()
entry_filter_club = tk.Entry(normal_user_frame, font=entry_font)
entry_filter_club.pack()
btn_filter_by_club = tk.Button(normal_user_frame, text="Filter", command=filter_events_by_club, font=button_font, bg=button_color, fg="white")
btn_filter_by_club.pack(pady=5)

# Entry and button to search events by event name or club name
label_search = tk.Label(normal_user_frame, text="Search Events by Event Name", font=label_font, bg=background_color)
label_search.pack()
entry_search = tk.Entry(normal_user_frame, font=entry_font)
entry_search.pack()
btn_search = tk.Button(normal_user_frame, text="Search", command=search_events, font=button_font, bg=button_color, fg="white")
btn_search.pack(pady=5)

normal_user_frame.pack_forget()

root.mainloop()

cur.close()
conn.close()