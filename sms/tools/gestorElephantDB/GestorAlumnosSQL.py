import os
import psycopg2
import urlparse
import clavesElephantSQL

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(clavesElephantSQL.DATABASE_URL)
conn = psycopg2.connect(database=url.path[1:],
  user=url.username,
  password=url.password,
  host=url.hostname,
  port=url.port
)

cursor = conn.cursor()
cursor.execute(open("DBCreator_v01.sql", "r").read())


# -*- coding: utf-8 -*-
#import MySQLdb
from Alumno import *
from Profesor import *
from Asignatura import *

'''Clase controladora de alumnos. Que usando la clase que define el modelo de Alumno (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorAlumnos:

    @classmethod
    def nuevoAlumno(self, nombre, dni):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        query="INSERT INTO Alumno values("+"'"+nombre+"', "+"'"+dni+"');"
        cursor = db.cursor()
        cursor.execute(query);
        db.commit()
        cursor.close()
        db.close()


    @classmethod
    def getAsignaturasMatriculadas(self, dniAlumno):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        query="select Asignatura.*  from Alumno, Cursa, Asignatura where Alumno.dni=Cursa.dniAlumno and Cursa.idAsignatura=Asignatura.id and Alumno.dni='"+dniAlumno+"';"

        cursor = db.cursor()
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            asg = Asignatura()
            asg.nombre=row[0]
            lista.append(asg)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista


    @classmethod
    def getProfesoresAlumno(self, dniAlumno):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm");
        query="select Profesor.*  from Profesor, Imparte, Cursa, Alumno where Profesor.dni=Imparte.dniProfesor and Imparte.idAsignatura=Cursa.idAsignatura and Cursa.dniAlumno=Alumno.dni and Alumno.dni='"+dniAlumno+"';"
        cursor = db.cursor()
        cursor.execute(query);
        row = cursor.fetchone()

        lista = []

        while row is not None:
            prf = Profesor()
            prf.nombre=row[0]
            prf.apellidos=row[1]
            lista.append(prf)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista


    @classmethod
    def getAlumnos(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm");
        cursor = db.cursor()
        query="select * from Alumno";
        cursor.execute(query);
        row = cursor.fetchone()

        lista = []

        while row is not None:
            alumno = Alumno()
            alumno.nombre=row[0]
            alumno.dni=row[1]
            lista.append(alumno)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

        #Una de las opciones es convertirlo en un objeto y devolverlo

    @classmethod
    def getAlumno(self, dniAlumno):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        cursor = db.cursor()
        query="select * from Alumno where dni='"+dniAlumno+"';"

        cursor.execute(query)
        row = cursor.fetchone()

        alm = Alumno()
        alm.nombre=row[0]
        alm.dni=row[1]

        cursor.close()
        db.close()

        return alm

    '''Registro masivo de usuarios a partir de fichero CSV.
    Como opción para el Admin del Sistema se ofrece la subida masiva de usuarios al sistema mediante
    fichero CSV. Así podrá cargar todos los usuarios que el sistema de la Junta de Andalucía le ofrece para no
    tener que subirlos uno a uno.
    '''
    @classmethod
    def nuevosAlumnos(self):
        import csv
        import sys

        f = open('RegTutores.csv', 'r')

        csv.register_dialect('prueba', delimiter=',')


        reader = csv.reader(f, dialect='prueba')

        #Habilitar para el procesamiento del fichero completo.
        #for row in reader:
        for i in range(10):
                row = reader.next()
                nombre = row[0]
                nombreDividido = nombre.split(',')
                if len(nombreDividido)==2:
                        #print nombreDividido[1],nombreDividido[0]
                        nombre=unicode(nombreDividido[1], errors='replace')
                        apellidos=unicode(nombreDividido[0], errors='replace')

                    #    GestorAlumnos.nuevoAlumno(nombre, apellidos)

                else:
                        print nombreDividido[0]

    @classmethod
    def getNumeroAlumnos(self):
        pass # place magic here


    @classmethod
    def loadAlumnosFromCSVFile(self, file):
        pass #place magic here



    def all_unique(word):

        #Toda la palabra se pasa a mayúsculas
        word=word.upper()

        #Se recorren todas las letras de la palabra:
        for letter in range(len(word)):
            #Se extrae la letra de la palabra
            sectionWord=word[:letter]+word[letter+1:]
            #Se busca en el resto de la palabra si aparece la extraida.
            if sectionWord.find(word[letter]) != -1 :
                #Si se encuentra otra ocurrencia find devuelve la pos (-1 si no la encuentra) y
                #la función devuelve False porque no es una palabra sin elementos repetidos.
                return False
        #Si no se encuentran elementos repetidos se devuelve True.
        return True
