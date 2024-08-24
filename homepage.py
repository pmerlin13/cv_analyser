import pickle
from pathlib import Path
import streamlit_authenticator as stauth 
import streamlit as st
import psycopg2
  
#---------- USER AUTHENTICATION

#Users
names = ["Merlin Pineda", "Maurelys Jaquez"]
usernames = ["Pineda","Mau"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "sales_dashboard", "abcdef")
authenticator.logout("Logout", "sidebar")
name, authentication_status, username = authenticator.login("Login", "main")

#Verifico authentication
if authentication_status == False:
    st.error("Username/password is incorrect")
if authentication_status == None:
    st.error("please enter your Username andpassword")
if authentication_status:
    # Función para validar el inicio de sesión
    conn = psycopg2.connect(
        user="admin",
        password="admin",
        host="localhost",
        port="5432",  # Replace with the actual port number
        database="medicai"
    )

    cursor = conn.cursor()

    # Ejecutar una consulta SELECT
    query = "SELECT * FROM user"
    cursor.execute(query)

    # Obtener los resultados de la consulta
    results = cursor.fetchall()
    for row in results:
        print(row)

    # Confirmar la transacción y cerrar la conexión
    conn.commit()
    conn.close()

    def iniciar_sesion(correo, contrasena):
        # Aquí puedes implementar tu lógica de validación de inicio de sesión
        # Por simplicidad, este código solo verifica que se ingresen datos en ambos campos
        if correo and contrasena:
            return True
        else:
            return False

    # Página de inicio de sesión
    def pagina_inicio_sesion():
        st.title('Inicio de Sesión')
        st.write('Por favor, ingresa tus credenciales para iniciar sesión.')
        
        # Obtener los datos del usuario
        correo = st.text_input('Correo o usuario')
        contrasena = st.text_input('Contraseña', type='password')
        
        # Botón de inicio de sesión
        if st.button('Iniciar sesión'):
            if iniciar_sesion(correo, contrasena):
                st.success('Inicio de sesión exitoso.')
            else:
                st.error('Usuario o contraseña inválidos.')
        
        # Enlace para restablecer contraseña
        st.write('¿Olvidaste tu contraseña?')
        if st.button('Restablecer contraseña'):
            # Aquí puedes implementar la lógica para enviar un código de restablecimiento de contraseña al correo del usuario
            st.info('Se ha enviado un código de restablecimiento de contraseña a tu correo electrónico.')

    # Página de registro
    def pagina_registro():
        st.title('Registro')
        st.write('Por favor, completa los siguientes campos para crear una cuenta.')
        
        # Obtener los datos del usuario
        nombre = st.text_input('Nombre')
        correo = st.text_input('Correo electrónico')
        contrasena = st.text_input('Contraseña', type='password')
        
        # Botón de registro
        if st.button('Crear cuenta'):
            # Aquí puedes implementar la lógica de registro de usuario
            st.success('Cuenta creada exitosamente.')

    # Página principal
    def pagina_principal():
        st.title('Sistema de Registro y Gestión')
        
        # Opciones del menú
        opcion = st.radio('Opción', ['Inicio de Sesión', 'Registro'])
        
        # Procesar la opción seleccionada
        if opcion == 'Inicio de Sesión':
            pagina_inicio_sesion()
        elif opcion == 'Registro':
            pagina_registro()

    # Ejecutar la aplicación
    if __name__ == '__main__':
        pagina_principal()

