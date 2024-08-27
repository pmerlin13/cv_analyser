import streamlit as st
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

# Proceso de encriptación
def get_fernet_key():
    # Cargar la clave desde un archivo o una configuración segura
    # En este ejemplo, la clave está codificada directamente
    # En un entorno de producción, considera almacenar la clave en una ubicación segura
    key = st.secrets["database"]["encryption_key"]
    return Fernet(key.encode('utf-8'))

def encrypt_pass(password):
    fernet = get_fernet_key()
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_pass(encrypted_password):
    fernet = get_fernet_key()
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Cargar secretos desde Streamlit Secrets
db_user = st.secrets["database"]["user"]
db_password = st.secrets["database"]["password"]
db_host = st.secrets["database"]["host"]
db_port = st.secrets["database"]["port"]
db_name = st.secrets["database"]["name"]

# Función para conectar a la base de datos
def conectar_bd():
    try:
        conn = psycopg2.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name,
            sslmode="require" 
        )
        return conn
    except psycopg2.OperationalError as e:
        st.error(f"Error de conexión:  {e}")
        raise

# Función para verificar las credenciales del usuario
def verificar_credenciales(correo, contrasena):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, password FROM user.user_info WHERE email = %s", (correo,))
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
        
        # Obtener los datos del usuario
        correo = st.text_input('Correo o usuario')
        contrasena = st.text_input('Contraseña', type='password')

        # Validar campos
        if st.button('Iniciar sesión'):
            if not correo or not contrasena:
                st.error("Todos los campos son obligatorios.")
            else:
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

        # Obtener los datos del usuario
        nombre = st.text_input('Nombre')
        correo = st.text_input('Correo electrónico')
        contrasena = st.text_input('Contraseña', type='password')

        # Validar campos
        if st.button('Crear cuenta'):
            if not nombre or not correo or not contrasena:
                st.error("Todos los campos son obligatorios.")
            else:
                conn = conectar_bd()
                cursor = conn.cursor()
                hashed_password = generate_password_hash(contrasena)
                cursor.execute("INSERT INTO user.user_info (name, email, password) VALUES (%s, %s, %s)",
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
