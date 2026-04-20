"""
app.py - Punto de entrada de la aplicacion Flask.

Crea la aplicacion, registra los Blueprints base
e inicia el servidor de desarrollo en el puerto 5100.
"""

from flask import Flask

from config import SECRET_KEY


# ══════════════════════════════════════════════
# CREAR LA APLICACION FLASK
# ══════════════════════════════════════════════

app = Flask(__name__)

app.secret_key = SECRET_KEY


# ══════════════════════════════════════════════
# REGISTRAR BLUEPRINTS BASE
# ══════════════════════════════════════════════

from routes.home import bp as home_bp
from routes.autenticacion import bp as autenticacion_bp

app.register_blueprint(home_bp)
app.register_blueprint(autenticacion_bp)


# ══════════════════════════════════════════════
# SEGURIDAD GLOBAL DE SESIONES
# ══════════════════════════════════════════════

@app.before_request
def proteger_rutas():
    return None


# ══════════════════════════════════════════════
# INICIAR EL SERVIDOR
# ══════════════════════════════════════════════

if __name__ == '__main__':
    app.run(debug=True, port=5100)