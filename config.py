"""
config.py - Configuracion centralizada de la aplicacion Flask.

Contiene las constantes que se usan en toda la aplicacion:
la URL de la API y la clave secreta para sesiones/flash.
"""

import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7231")
VERIFY_SSL = os.getenv("VERIFY_SSL", "False").lower() in ("true", "1", "t")
SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta-flask-frontend-2024")

if not VERIFY_SSL:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)