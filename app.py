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
from routes.linea_investigacion import bp as linea_investigacion_bp
from routes.area_conocimiento import bp as area_conocimiento_bp
from routes.area_aplicacion import bp as area_aplicacion_bp
from routes.objetivo_desarrollo_sostenible import bp as ods_bp

app.register_blueprint(home_bp)
app.register_blueprint(autenticacion_bp)
app.register_blueprint(linea_investigacion_bp)
app.register_blueprint(area_conocimiento_bp)
app.register_blueprint(area_aplicacion_bp)
app.register_blueprint(ods_bp)

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