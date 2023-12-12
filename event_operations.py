# Function to add an event to the database
def add_event(db, event_name, event_date, event_location, event_club, sao_admin_id):
    try:
        query = '''
            INSERT INTO events (event_name, event_date, event_location, event_club, sao_admin_id) 
            VALUES (%s, %s, %s, %s, %s);
        '''
        params = (event_name, event_date, event_location, event_club, sao_admin_id)
        success, _ = db.execute_query(query, params)
        if success:
            return True, "Event added successfully."
        else:
            return False, "Failed to add event."
    except Exception as e:
        return False, str(e)

# Function to view all events from the database
def view_events(db):
    try:
        query = "SELECT * FROM events"
        success, rows = db.execute_query(query)
        if success:
            return True, rows
        else:
            return False, "Failed to retrieve events."
    except Exception as e:
        return False, str(e)

# Function to filter events by date
def filter_events_by_date(db, date):
    try:
        query = "SELECT * FROM events WHERE event_date = %s;"
        success, rows = db.execute_query(query, (date,))
        if success:
            return True, rows
        else:
            return False, "No events found for the specified date."
    except Exception as e:
        return False, str(e)

# Function to filter events by club
def filter_events_by_club(db, club_name):
    try:
        query = "SELECT * FROM events WHERE event_club = %s;"
        success, rows = db.execute_query(query, (club_name,))
        if success:
            return True, rows
        else:
            return False, "No events found for the specified club."
    except Exception as e:
        return False, str(e)

# Function to search for events
def search_events(db, search_text):
    try:
        query = '''
            SELECT * FROM events 
            WHERE event_name ILIKE %s OR event_club ILIKE %s;
        '''
        success, rows = db.execute_query(query, (f'%{search_text}%', f'%{search_text}%'))
        if success:
            return True, rows
        else:
            return False, "No matching events found."
    except Exception as e:
        return False, str(e)
