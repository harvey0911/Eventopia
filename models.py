

TABLES = {
    'sao_admins': '''
        CREATE TABLE IF NOT EXISTS sao_admins (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL
        );
    ''',
    'events': '''
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            event_name VARCHAR(100) NOT NULL,
            event_date DATE,
            event_location VARCHAR(100),
            event_club VARCHAR(100),
            sao_admin_id INTEGER REFERENCES sao_admins(id)
        );
    ''',
    'students': '''
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
    ''',
    'staff': '''
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
    ''',
    'faculty': '''
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
    ''',
    'attendance': '''
        CREATE TABLE IF NOT EXISTS attendance (
            p_id INTEGER REFERENCES students(id),
            event_id INTEGER REFERENCES events(id),
            n_of_attendee INTEGER,
            PRIMARY KEY (p_id, event_id)
        );
    '''
}

def create_tables(db):
    for table_name, table_query in TABLES.items():
        db.execute_query(table_query)
