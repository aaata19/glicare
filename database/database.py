import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

db = sqlite3.connect("gliCare_collection1.db")
cursor = db.cursor()

class Base(DeclarativeBase):
  pass

# #   CREARE SI POPULARE TABELA UTILIZATOR
# # type pt tip utilizator (a-admin, d-doct, p-pacient)
# cursor.execute("CREATE TABLE utilizator (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id varchar(30) NOT NULL UNIQUE, password varchar(30) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE,type varchar(3) NOT NULL)")
# cursor.execute("INSERT INTO utilizator (user_id, password, email,type) VALUES ('ion_ion', 'abc123', 'ion@test.com','p')")
# cursor.execute("INSERT INTO utilizator (user_id, password, email, type) VALUES ('john_doe', 'abc123', 'johndoe@test.com','a')")
# cursor.execute("INSERT INTO utilizator (user_id, password, email, type) VALUES ('snow_white', 'abc123', 'snowwhite@test.com','p')")
# cursor.execute("INSERT INTO utilizator (user_id, password, email, type) VALUES ('doc_vasile45', 'abc123', 'vasile@test.com','d')")
# cursor.execute("INSERT INTO utilizator (user_id, password, email, type) VALUES ('ana_ionescu', 'abc123', 'ana@test.com','d')")
#
# # CREARE SI POPULARE TABELA CLINICA
# cursor.execute("CREATE TABLE clinica (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), country VARCHAR(20), city VARCHAR(20))")
# cursor.execute("INSERT INTO clinica (name, country, city) VALUES ('SuperMed', 'Romania', 'Bucuresti')")
# cursor.execute("INSERT INTO clinica (name, country, city) VALUES ('DiaMed', 'Romania', 'Galati')")
#
# # CREARE SI POPULARE TABELA DOCTORI
# cursor.execute("CREATE TABLE doctor (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, nume VARCHAR(30), prenume VARCHAR(30), data_nasterii DATE, cabinet_id INTEGER NOT NULL)")
# cursor.execute("INSERT INTO doctor (user_id, nume, prenume, data_nasterii, cabinet_id) VALUES (4, 'Marinescu', 'Vasile', '10-10-1983', 1)")
# cursor.execute("INSERT INTO doctor (user_id, nume, prenume, data_nasterii, cabinet_id) VALUES (5, 'Ionescu', 'Ana', '25-01-1989', 2)")
#
# # CREARE SI POPULARE TABELA PACIENTI
# # greutate = kg, inaltime = cm
# cursor.execute("CREATE TABLE pacient (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id, nume VARCHAR(30), prenume VARCHAR(30), data_nasterii DATE, doctor_id INTEGER, sex VARCHAR(3), weight INTEGER, height INTEGER)")
# cursor.execute("INSERT INTO pacient(user_id, nume, prenume, data_nasterii, doctor_id, sex, weight, height) VALUES (1, 'Popescu', 'Ion', '1999-12-23', 1, 'm', 76, 185)")
# cursor.execute("INSERT INTO pacient(user_id, nume, prenume, data_nasterii, doctor_id, sex, weight, height) VALUES (3, 'White', 'Snow', '2000-02-24', 2, 'f', 55, 167)")
#
# # CREARE SI POPULARE TABELA OBIECTIVE
# cursor.execute("CREATE TABLE obiective (id INTEGER PRIMARY KEY AUTOINCREMENT, pacient_id INTEGER, weight INTEGER, medie_glicemii INTEGER)")
# cursor.execute("INSERT INTO obiective(pacient_id, weight, medie_glicemii) VALUES (1, 85, 155)")
# cursor.execute("INSERT INTO obiective(pacient_id, weight, medie_glicemii) VALUES (2, 57, 120)")
#
# # CREARE TABELA ADEVERINTA
# cursor.execute("CREATE TABLE adeverinta (id_adv INTEGER PRIMARY KEY AUTOINCREMENT,id_pacient INTEGER,id_doctor INTEGER,adeverinta BLOB,date DATE,stare INTEGER CHECK(stare IN (0, 1)))")
#
# cursor.execute("CREATE TABLE postareForum (id_post INTEGER PRIMARY KEY AUTOINCREMENT, id_utilizator INTEGER, titlu VARCHAR(150), text VARCHAR (250), data_postarii DATE, tip_postare VARCHAR(2), poza BLOB)")
# cursor.execute("INSERT INTO postareForum (id_utilizator, titlu, text, data_postarii, tip_postare) VALUES (1, 'Ce mancati seara inainte de culcare sa aveti glicemia stabila toata noaptea?', 'Buna seara! De o perioada am niste probleme cu spike-uri glicemice noaptea, ma trezesc ori cu hipoglicemie ori cu hiperglicemie de mai multe ori pe parcursul unei nopti. Ce as putea consuma inainte de culcare pentru a pastra valorile glicemiilor intr-un anumit interval?', '11-04-2024', 'n')")
# cursor.execute("INSERT INTO postareForum (id_utilizator, titlu, text, data_postarii, tip_postare) VALUES (3, 'Dosar handicap', 'Buna seara ! Am depus si eu dosarul pt certificat de handicap si am primit incadrarea in grad mediu ( mentionez ca am de 3 ani diabet si am mai multe cunostite care au incadrarea in grad accentuat ) .Stiti dupa ce criterii se alege incadrarea ? Ce drepturi ai in  gradul mediu ? Multumesc mult', '10-04-2024', 'n')")
# cursor.execute("INSERT INTO postareForum (id_utilizator, titlu, text, data_postarii, tip_postare) VALUES (7, 'Senzor Guardian3', 'Bună ziua ,cine mă poate ajuta și pe mine cu lista de telefoane compatibile cu Guardian3  ,lista care o găsesc eu zice că nu mai sunt compatibile toate pt că de pe 6 aprilie sa actualizat lista și multe nu mai sunt compatibile', '10-04-2024', 'a')")
#
# cursor.execute("CREATE TABLE raspunsForum (id_raspuns INTEGER PRIMARY KEY AUTOINCREMENT, id_postare INTEGER, id_utilizator INTEGER, text VARCHAR (250),tip_postare VARCHAR(2))")
# cursor.execute("INSERT INTO raspunsForum (id_postare, id_utilizator, text, tip_postare) VALUES (1, 12, 'Depinde ce mancati la cina...Ideal ar fi ceva ușor, fără multe grăsimi ce noaptea se transforma în glucide.. ', 'n')")
# cursor.execute("INSERT INTO raspunsForum (id_postare, id_utilizator, text, tip_postare) VALUES (1, 3, 'La mine merge niste mar cu unt de arahide sau alte unturi de nuci', 'a')")
#

# TABELA BLOG 
cursor.execute("CREATE TABLE blog (id_blog INTEGER PRIMARY KEY AUTOINCREMENT, titlu VARCHAR(150), text VARCHAR (250), data_postarii DATE, poza BLOB)")


db.commit()
db.close()

