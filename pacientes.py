import streamlit as st
import psycopg2
import json
import sys
sys.path.append(r"C:\\Users\\user\\Desktop\\Proyectos\\medic.ai")
import database
#***********************************************************************************************************************Class client
class client:
    def __init__(self,nombres:str,apellidos:str,cedula:str,pasaporte:str,fecha_nacimiento:str,sexo:str,seguro:str,id_seguro:str,telefono:str,celular:str,pariente_cercano:str,numero_pariente:str,profesion_oficio:str):
        self.user_id = 1
        self.id_paciente = self.generar_id_paciente()
        self.name = [nombres]
        self.lastname = [apellidos]
        self.card_id = cedula
        self.passport = pasaporte
        self.birthdate = fecha_nacimiento
        self.sex = sexo
        self.assurance_provider = seguro
        self.assurance_number = id_seguro        
        self.phone_number = telefono
        self.cell_phone = celular
        self.family_member = pariente_cercano
        self.f_member_number = numero_pariente 
        self.occupation = profesion_oficio
    def add(self):
        conn = database.database_connection()
        # Crear un cursor para interactuar con la base de datos
        cursor = conn.cursor()
        # Construir la consulta SQL para actualizar los campos
# Primero, intenta insertar el registro en la tabla
        insert_query = """
            INSERT INTO medicai.client (client_id, user_id, name, lastname, card_id, passport, birthdate, sex, assurance_provider, assurance_number, phone_number, cell_phone, family_member, f_member_number, occupation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Ejecutar la consulta de inserción
        cursor.execute(insert_query, (
            self.id_paciente,
            self.user_id,
            self.name,
            self.lastname,
            self.card_id,
            self.passport,
            self.birthdate,
            self.sex,
            self.assurance_provider,
            self.assurance_number,
            self.phone_number,
            self.cell_phone,
            self.family_member,
            self.f_member_number,
            self.occupation
        ))

        # Confirmar la transacción
        conn.commit()

        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()
    # Función para generar el ID del paciente
    def generar_id_paciente(self):
        # Definir el ID del cliente que deseas actualizar
        conn = database.database_connection()
        # Crear un cursor para interactuar con la base de datos
        cursor = conn.cursor()
        # Ejecutar la consulta SQL para obtener el último ID
        try:
            cursor.execute("SELECT MAX(client_id) FROM medicai.client")
            # Obtener el resultado de la consulta
            ultimo_id = cursor.fetchone()[0]        
            # Cerrar el cursor y la conexión
            cursor.close()
            conn.close()
        except:
            print("No hay paciente registrado")
        if ultimo_id:
            nuevo_id = ultimo_id + 1
        else:
            nuevo_id = 1      

        # Imprimir el último ID obtenido
        print("Último ID:", ultimo_id,"Nuevo ID:",nuevo_id)
        return nuevo_id
    # Función para obtener nuevo numero de paciente a utilizar(id)
        # Función para generar el ID del paciente
def buscar_id_paciente():
    ultimo_id = 0
    # Definir el ID del cliente que deseas actualizar
    conn = database.database_connection()
    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()
    # Ejecutar la consulta SQL para obtener el último ID
    try:
        cursor.execute("SELECT MAX(client_id) FROM medicai.client")
        # Obtener el resultado de la consulta
        ultimo_id = cursor.fetchone()[0]        
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()
    except:
        print("No hay paciente registrado")

    if ultimo_id:
        nuevo_id = ultimo_id + 1
    else:
        nuevo_id = 1      


    # Imprimir el último ID obtenido
    print("Último ID:", ultimo_id,"Nuevo ID:",nuevo_id)
    return nuevo_id
