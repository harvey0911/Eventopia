import psycopg2

class Database:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        self.cur = self.conn.cursor()
    
    def execute_query(self, query, params=None):
        try:
            self.cur.execute(query, params or ())
            self.conn.commit()
            return True, self.cur.fetchall()
        except psycopg2.Error as e:
            return False, str(e)
    
    def close(self):
        self.cur.close()
        self.conn.close()
