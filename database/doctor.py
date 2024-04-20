import sqlite3
class Doctor:
    # i want only the id and username to be mandatory
    def __init__(self, id, username, email, nume = None, prenume = None, data_nasterii = None, cabinet_id = None):
        self.type = 'd'
        self.id = id
        self.username = username
        self.email = email
        self.nume = nume
        self.prenume = prenume
        self.data_nasterii = data_nasterii
        self.cabinet_id = cabinet_id

    def __str__(self):
        return f'Doctor(id={self.id}, username={self.username}, email={self.email}, type={self.type}, nume={self.nume}, prenume={self.prenume}, data_nasterii={self.data_nasterii}, cabinet_id={self.cabinet_id})'
    
    def getDoctor(self):
        conn = sqlite3.connect('database/gliCare_collection1.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM doctor WHERE user_id=?", (self.id,))
        user = cur.fetchone()
        conn.close()
        if user is None:
            # nu exista
            print("User not found")
        else:
            # exista
            # TODO - de completat cu toate datele pacientului preluate din lista user
            self.nume = user[2]
            self.prenume = user[3]
            self.data_nasterii = user[4]
            self.cabinet_id = user[5]
            return self
        
