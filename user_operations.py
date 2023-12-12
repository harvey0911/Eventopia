from tkinter import messagebox

# Function to register a new user
def register_user(db, user_type, first_name, last_name, date_of_birth, email, contact_number, country, username, password):
    try:
        if user_type == "student":
            query = '''
                INSERT INTO students (first_name, last_name, date_of_birth, email, contact_number, country, username, password) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
            params = (first_name, last_name, date_of_birth, email, contact_number, country, username, password)
        elif user_type == "staff":
            query = '''
                INSERT INTO staff (first_name, last_name, date_of_birth, email, contact_number, country, username, password) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
            params = (first_name, last_name, date_of_birth, email, contact_number, country, username, password)
        elif user_type == "faculty":
            query = '''
                INSERT INTO faculty (first_name, last_name, date_of_birth, email, contact_number, country, username, password) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
            params = (first_name, last_name, date_of_birth, email, contact_number, country, username, password)
        elif user_type == "SAOadmin":
            query = '''
                INSERT INTO sao_admins (username, password) VALUES (%s, %s);
            '''
            params = (username, password)
        else:
            raise ValueError("Invalid user type")

        success, _ = db.execute_query(query, params)
        if success:
            return True, "User registered successfully."
        else:
            return False, "Failed to register user."
    except Exception as e:
        return False, str(e)

# Function to log in to the application
def login_user(db, username, password):
    query = '''
        SELECT * FROM sao_admins WHERE username = %s AND password = %s;
    '''
    success, result = db.execute_query(query, (username, password))
    if success and result:
        return True, "Logged in as SAO admin."
    else:
        return False, "Invalid username or password."
