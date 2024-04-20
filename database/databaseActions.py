import sqlite3
from database.pacient import Pacient
from database.doctor import Doctor
import datetime
from PIL import Image
from pdf2image import convert_from_path
import os
import io

# functie de adaugare utilizator in bd
def addUser(username, password, email, tip, CABINET_ID):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO utilizator (user_id, password, email, type) VALUES (?,?,?,?)", (username, password, email, tip,))
    conn.commit()  # commit after inserting into utilizator
    if tip == 'p':
        cur.execute("INSERT INTO pacient (user_id) SELECT id FROM utilizator WHERE user_id=?", (username,))
    elif tip == 'd':
        cur.execute("SELECT id FROM utilizator WHERE user_id=?", (username,))
        doctor_id = cur.fetchone()
        cur.execute("INSERT INTO doctor (user_id, cabinet_id) VALUES(?,?)", (doctor_id[0], CABINET_ID,))
    conn.commit()
    conn.close()

# functie de returnare a datelor unui utilizator
def getUser(id):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM utilizator WHERE id=?", (id,))
    user = cur.fetchone()
    conn.close()
    # preia obiectul utilizator
    if(user[4] == 'p'):
        pacient = Pacient(id = user[0], username = user[1], email = user[3])
        pacient.getPacient()
        return pacient
    elif(user[4] == 'd'):
        doctor = Doctor(id = user[0], username = user[1], email = user[3])
        doctor.getDoctor()
        return doctor
    else:
        return user

def getUserType(id):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM utilizator WHERE id=?", (id,))
    user = cur.fetchone()
    conn.close()
    return user
#  functie de actualizare a datelor unui utilizator
def updateUser(user):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    if user.type == 'p':
        cur.execute("""
            UPDATE pacient
            SET nume = ?, prenume = ?, data_nasterii = ?, doctor_id = ?, sex = ?, weight = ?, height = ?
            WHERE user_id = ?
        """, (user.nume, user.prenume, user.data_nasterii, user.doctor_id ,user.sex, user.weight, user.height, user.id))
    elif user.type == 'd':
        cur.execute("""
            UPDATE doctor
            SET nume = ?, prenume = ?, data_nasterii = ?
            WHERE user_id = ?
        """, (user.nume, user.prenume, user.data_nasterii, user.id))
    conn.commit()
    conn.close()

# FUNCTII PENTRU PRELUCRAREA ADEVERINTELOR MEDICALE
def getAdeverinte(user):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    if user.type == 'p':
        cur.execute("SELECT id_adv, adeverinta FROM adeverinta WHERE id_pacient=?", (user.id,))
    elif user.type == 'd':
        cur.execute("SELECT id_adv, adeverinta FROM adeverinta WHERE id_doctor=? AND stare=0", (user.id,))
    rows = cur.fetchall()
    conn.close()

    images = {}
    for row in rows:
        id = row[0]
        adeverinta_blob = row[1]
        image_data = io.BytesIO(adeverinta_blob)
        image = Image.open(image_data)
        images[id] = image

    return images

def addAdeverinta(user, doctor_id, adeverinta):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    data = datetime.datetime.now().strftime("%Y-%m-%d")
    cur.execute("INSERT INTO adeverinta (id_pacient, id_doctor, adeverinta, date, stare) VALUES (?,?,?,?,?)", (user, doctor_id,adeverinta,data,0,))
    conn.commit()
    conn.close()

def updateAdeverinta(id_adeverinta,adeverinta):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    # store the binary data in the database
    cur.execute("UPDATE adeverinta SET adeverinta = ?, stare = 1 WHERE id_adv = ?", (adeverinta, id_adeverinta))
    conn.commit()
    conn.close()

# FUNCTII PENTRU FORUM
def getPostari():
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM postareForum")
    rows = cur.fetchall()
    conn.close()
    return rows

def addPostare(user_id, titlu, text, tip_postare, poza=None):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    data = datetime.datetime.now().strftime("%d-%m-%Y")
    cur.execute("INSERT INTO postareForum (id_utilizator, titlu, text, data_postarii, tip_postare, poza) VALUES (?,?,?,?,?,?)", (user_id, titlu, text, data, tip_postare, poza,))
    conn.commit()
    conn.close()

def getRaspunsPostare(id_post):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM raspunsForum WHERE id_postare=?", (id_post,))
    rows = cur.fetchall()
    conn.close()
    return rows

def addRaspunsPostare(user_id, id_postare, text, tip_postare):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO raspunsForum (id_postare, id_utilizator, text, tip_postare) VALUES (?,?,?,?)", (id_postare, user_id, text, tip_postare,))
    conn.commit()
    conn.close()

# FUNCTII PENTRU BLOG
def getPostariBlog():
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM blog ORDER BY id_blog DESC LIMIT 5")
    rows = cur.fetchall()
    conn.close()
    return rows

def addPostareBlog(titlu, text, poza=None):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    data = datetime.datetime.now().strftime("%d-%m-%Y")
    cur.execute("INSERT INTO blog (titlu, text, data_postarii, poza) VALUES (?,?,?,?)", (titlu, text, data, poza,))
    conn.commit()
    conn.close()

def getBlog(id_blog):
    conn = sqlite3.connect('database/gliCare_collection1.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM blog WHERE id_blog=?", (id_blog,))
    blog = cur.fetchone()
    conn.close()
    return blog