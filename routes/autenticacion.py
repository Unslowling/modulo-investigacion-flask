"""
autenticacion.py - Blueprint para manejar el inicio de sesión con JWT.
"""
import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config import API_BASE_URL

bp = Blueprint('autenticacion', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Muestra el formulario de login y procesa la autenticación contra la API C#."""
    # Si el usuario ya tiene sesión, redirigir al home
    if 'api_token' in session:
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        email = request.form.get('email', '')
        contrasena = request.form.get('contrasena', '')

        try:
            # Enviar credenciales al endpoint de login en C#
            url = f"{API_BASE_URL}/api/autenticacion/login"
            datos = {"email": email, "contrasena": contrasena}
            
            # Petición HTTP directa usando requests
            respuesta = requests.post(url, json=datos)
            
            if respuesta.ok:
                contenido = respuesta.json()
                # Extraer el token de la respuesta JSON
                token = contenido.get("token")
                
                if token:
                    # Guardar el token de seguridad en la sesión local de Flask
                    session['api_token'] = token
                    flash("Has iniciado sesión exitosamente.", "success")
                    return redirect(url_for('home.index'))
                else:
                    flash("Error: El servidor no proporcionó un token válido.", "danger")
            else:
                # Extraer mensaje de error desde C#
                try:
                    mensaje_error = respuesta.json().get("mensaje", "Credenciales inválidas.")
                except:
                    mensaje_error = "Credenciales incorrectas o acceso denegado."
                flash(mensaje_error, "danger")

        except requests.RequestException as ex:
            flash(f"Error de conexión con la API: {ex}", "danger")

    return render_template('pages/login.html')

@bp.route('/logout')
def logout():
    """Cierra la sesión destruyendo el token JWT almacenado localmente."""
    session.pop('api_token', None)
    flash("Has cerrado sesión correctamente.", "success")
    return redirect(url_for('autenticacion.login'))
