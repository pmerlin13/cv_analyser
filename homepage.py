import streamlit as st
import psycopg2
from werkzeug.security import check_password_hash

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

    # Buscar el usuario por correo o nombre de usuario
    cursor.execute("SELECT nombre, correo, password FROM users WHERE correo = %s", (correo,))
    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user[2], contrasena):
        return user[0]  # Retornar el nombre del usuario si la contraseña es correcta
    else:
        return None

# Página de inicio de sesión
def pagina_inicio_sesion():
    st.title('Inicio de Sesión')
    st.write('Por favor, ingresa tus credenciales para iniciar sesión.')

    # Obtener los datos del usuario
    correo = st.text_input('Correo o usuario')
    contrasena = st.text_input('Contraseña', type='password')

    # Botón de inicio de sesión
    if st.button('Iniciar sesión'):
        user_name = verificar_credenciales(correo, contrasena)
        if user_name:
            st.success(f'Inicio de sesión exitoso. Bienvenido, {user_name}!')
        else:
            st.error('Usuario o contraseña inválidos.')

    # Enlace para restablecer contraseña
    st.write('¿Olvidaste tu contraseña?')
    if st.button('Restablecer contraseña'):
        # Implementar la lógica para enviar un código de restablecimiento de contraseña al correo del usuario
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
        conn = conectar_bd()
        cursor = conn.cursor()
        # Hashear la contraseña antes de guardarla
        hashed_password = generate_password_hash(contrasena)

        # Insertar el nuevo usuario en la base de datos
        cursor.execute("INSERT INTO users (nombre, correo, password) VALUES (%s, %s, %s)",
                       (nombre, correo, hashed_password))
        conn.commit()
        conn.close()

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


