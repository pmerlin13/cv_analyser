#Pagina de Login
#Permite iniciar sesion con correo o usuario y con contraseña, en caso que no sea valido usuario o contraseña debe indicarlo, debe tener un boton de incio sesion
#Permite dar click en olvide contraseña para que se le envie un codigo al correo reestableciendo su contrasena
#Permite dar click en boton de registrarse para crear cuenta con datos personales, correo y contraseña


import streamlit as st

# Función para validar el inicio de sesión
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
