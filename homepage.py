import streamlit as st
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import streamlit_authenticator as stauth

# Proceso de encriptación
def get_fernet_key():
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
        st.error("Error de conexión")
        raise

# Función para verificar si un correo ya está registrado
def correo_registrado(correo):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM "user".user_info WHERE email = %s', (correo,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Función para obtener usuarios y contraseñas desde la base de datos
def obtener_usuarios_y_contrasenas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT name, email, password FROM "user".user_info')
    users = cursor.fetchall()
    conn.close()
    names = []
    usernames = []
    hashed_passwords = []
    credentials = {"usernames": {}}
    for user in users:
        name, username, hashed_password = user
        names.append(name)
        usernames.append(username)
        hashed_passwords.append(hashed_password)
        #credentials["usernames"][username] = {"name": name, "password": hashed_password}

    return names,usernames,hashed_passwords

# Página principal
def pagina_principal():
    st.title('Bienvenido al Sistema de Gestión de CVs')
    st.write('Esta es la página principal, solo accesible después de la autenticación.')

# Página de inicio de sesión combinada con streamlit_authenticator
def pagina_inicio_sesion():
    with st.container():
        st.title('Inicio de Sesión')
        st.write('Por favor, ingresa tus credenciales para iniciar sesión.')

        # Obtener los datos del usuario
        correo = st.text_input('Correo o usuario')
        contrasena = st.text_input('Contraseña', type='password')

        # Validar campos y autenticar usuario
        if st.button('Iniciar sesión'):
            if not correo or not contrasena:
                st.error("Todos los campos son obligatorios.")
            else:
                # Obtener las credenciales desde la base de datos
                names, usernames, hashed_passwords = obtener_usuarios_y_contrasenas()

                # Inicializar el autenticador de Streamlit
                authenticator = stauth.Authenticate(
                    names,
                    usernames,
                    hashed_passwords,
                    "sales_dashboard",
                    "abcdef"
                )

                # Usar streamlit_authenticator para autenticar
                name, authentication_status = authenticator.login("Login", "main")

                if authentication_status:
                    st.success(f'Inicio de sesión exitoso. Bienvenido, {name}!')
                    pagina_principal()
                elif authentication_status == False:
                    st.error('Usuario o contraseña inválidos.')
                elif authentication_status == None:
                    st.warning('Por favor, ingrese su usuario y contraseña.')

        st.write('¿Olvidaste tu contraseña?')
        if st.button('Restablecer contraseña'):
            st.info('Se ha enviado un código de restablecimiento de contraseña a tu correo electrónico.')

# Página de registro
def pagina_registro():
    st.title('Registro')
    st.write('Por favor, completa los siguientes campos para crear una cuenta.')

    nombre = st.text_input('Nombre')
    apellido = st.text_input('Apellido')
    correo = st.text_input('Correo electrónico')
    contrasena = st.text_input('Contraseña', type='password')

    if st.button('Crear cuenta'):
        if not nombre or not apellido or not correo or not contrasena:
            st.error("Todos los campos son obligatorios.")
        else:
            # Verificar si el correo ya está registrado
            if correo_registrado(correo):
                st.error('El correo electrónico ya está registrado. Por favor, utiliza otro correo.')
            else:
                conn = conectar_bd()
                cursor = conn.cursor()
                hashed_password = generate_password_hash(contrasena)
                cursor.execute('INSERT INTO "user".user_info (name, lastname, email, password) VALUES (%s, %s, %s, %s)', (nombre, apellido, correo, hashed_password))
                conn.commit()
                conn.close()
                st.success('Cuenta creada exitosamente.')

# Página de selección inicial
def pagina_seleccion():
    st.title("Bienvenido")
    opcion = st.radio('Seleccione una opción', ['Login', 'Registro'])

    if opcion == 'Login':
        pagina_inicio_sesion()
    elif opcion == 'Registro':
        pagina_registro()

# Ejecutar la aplicación
if __name__ == '__main__':
    pagina_seleccion()
