from database import Database
from gui import GUI

def main():
    db = Database('postgres', 'postgres', 'admin', 'localhost', '5432')
    app = GUI(db)
    app.run()
    db.close()

if __name__ == "__main__":
    main()
