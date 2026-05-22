from flask import Blueprint, render_template, redirect, url_for

from services.api_service import ApiService
from config import VERIFY_SSL

# requests: para hacer la llamada al endpoint de diagnostico de la API
import requests

bp = Blueprint('home', __name__)

api = ApiService()

# Ruta raíz
@bp.route('/')
def index():
    return redirect(url_for('autenticacion.login'))

# Home real del sistema
@bp.route('/home')
def home():

    diagnostico = None

    try:
        url = f"{api.base_url}/api/diagnostico/conexion"
        respuesta = requests.get(url, timeout=3, verify=VERIFY_SSL)
        if respuesta.ok:
            diagnostico = respuesta.json()

    except Exception:
        pass

    return render_template('pages/home.html', diagnostico=diagnostico)