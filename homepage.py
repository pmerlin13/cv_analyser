import streamlit as st
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

# Cargar secretos desde Streamlit Secrets
db_user = st.secrets["database"]["user"]
db_password = st.secrets["database"]["password"]
db_host = st.secrets["database"]["host"]
db_port = st.secrets["database"]["port"]
db_name = st.secrets["database"]["name"]

# Función para conectar a la base de datos
def conectar_bd():
    conn = psycopg2.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name
    )
    return conn

# Función para verificar las credenciales del usuario
def verificar_credenciales(correo, contrasena):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, correo, password FROM users WHERE correo = %s", (correo,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[2], contrasena):
        return user[0]
    else:
        return None

# Página de inicio de sesión
def pagina_inicio_sesion():
    with st.container():
        st.title('Inicio de Sesión')
        st.write('Por favor, ingresa tus credenciales para iniciar sesión.')
        correo = st.text_input('Correo o usuario')
        contrasena = st.text_input('Contraseña', type='password')
        if st.button('Iniciar sesión'):
            user_name = verificar_credenciales(correo, contrasena)
            if user_name:
                st.success(f'Inicio de sesión exitoso. Bienvenido, {user_name}!')
            else:
                st.error('Usuario o contraseña inválidos.')
        st.write('¿Olvidaste tu contraseña?')
        if st.button('Restablecer contraseña'):
            st.info('Se ha enviado un código de restablecimiento de contraseña a tu correo electrónico.')

# Página de registro
def pagina_registro():
    with st.container():
        st.title('Registro')
        st.write('Por favor, completa los siguientes campos para crear una cuenta.')
        nombre = st.text_input('Nombre')
        correo = st.text_input('Correo electrónico')
        contrasena = st.text_input('Contraseña', type='password')
        if st.button('Crear cuenta'):
            conn = conectar_bd()
            cursor = conn.cursor()
            hashed_password = generate_password_hash(contrasena)
            cursor.execute("INSERT INTO users (nombre, correo, password) VALUES (%s, %s, %s)",
                           (nombre, correo, hashed_password))
            conn.commit()
            conn.close()
            st.success('Cuenta creada exitosamente.')

# Página principal
def pagina_principal():
    st.title('Sistema de Registro y Gestión')
    opcion = st.radio('Opción', ['Inicio de Sesión', 'Registro'])
    if opcion == 'Inicio de Sesión':
        pagina_inicio_sesion()
    elif opcion == 'Registro':
        pagina_registro()

# Ejecutar la aplicación
if __name__ == '__main__':
    pagina_principal()

