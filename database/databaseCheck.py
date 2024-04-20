import sqlite3
#  This function checks if the username exists in the database
def signInUsernameExists(username):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM utilizator WHERE user_id=?", (username,))
    user = cur.fetchone()
    conn.close()
    if user is None:
        # nu exista
        return False
    else:
        # exista
        return True
    
# This function checks if the email exists in the database
def signInEmailExists(email):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM utilizator WHERE email=?", (email,))
    user = cur.fetchone()
    conn.close()
    if user is None:
        return False
    else:
        return True
    
# This function checks if the clinic exists in the database
def signInClinicExists(id_clinica):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM clinica WHERE id=?", (id_clinica,))
    clinica = cur.fetchone()
    conn.close()
    if clinica is None:
        return False
    else:
        return clinica

# this function checks if the user exists in the database and if the password is correct
def logIn(username, password):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM utilizator WHERE user_id=?", (username,))
    user = cur.fetchone()
    conn.close()
    if user is None:
        return False
    elif user[2] == password:
        return user
    else:
        return False
    
# check if doctor is in the database
def doctorExists(username):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM utilizator WHERE user_id=?", (username,))
    user = cur.fetchone()
    conn.close()
    if user is None:
        return False
    elif user[3] == 'd':
        return True
    else:
        return False
    
def getDoctor(username):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctor WHERE id=?", (username,))
    user = cur.fetchone()
    conn.close()
    return user