import sqlite3

class Pacient:
    # i want only the id and username to be mandatory
    def __init__(self, id, username, email, nume = None, prenume = None, data_nasterii = None, doctor_id = None, weight = None, height = None, sex = None):
        self.type = 'p'
        self.id = id
        self.username = username
        self.email = email
        self.nume = nume
        self.prenume = prenume
        self.data_nasterii = data_nasterii
        self.doctor_id = doctor_id
        self.weight = weight
        self.height = height
        self.sex = sex
    
    def __str__(self):
        return f'Pacient(id={self.id}, username={self.username}, email={self.email}, type={self.type}, nume={self.nume}, prenume={self.prenume}, data_nasterii={self.data_nasterii}, doctor_id={self.doctor_id}, weight={self.weight}, height={self.height}, sex={self.sex})'
    
    def getPacient(self):
        conn = sqlite3.connect('database/gliCare_collection1.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM pacient WHERE user_id=?", (self.id,))
        user = cur.fetchone()
        conn.close()
        if user is None:
            print("User not found")
        else:
            # exista
            # TODO - de completat cu toate datele pacientului preluate din lista user
            self.nume = user[2]
            self.prenume = user[3]
            self.data_nasterii = user[4]
            self.doctor_id = user[5]
            self.sex = user[6]
            self.weight = user[7]
            self.height = user[8]
        return self
    