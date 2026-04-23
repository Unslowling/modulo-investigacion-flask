from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('participa_semillero', __name__)
api = ApiService()

TABLA = 'participa_semillero'
CLAVE = 'semillero'  # ⚠️ simplificación (PK compuesta en realidad)


@bp.route('/participa-semillero')
def index():
    registros = api.listar(TABLA)
    return render_template('pages/participa_semillero/lista.html', registros=registros)


@bp.route('/participa-semillero/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        datos = {
            'docente': None,  # 👈 SIEMPRE NULL
            'semillero': request.form.get('semillero'),
            'rol': request.form.get('rol'),
            'fecha_inicio': request.form.get('fecha_inicio'),
            'fecha_fin': request.form.get('fecha_fin') or None,
        }

        exito, mensaje = api.crear(TABLA, datos)

        if exito:
            flash("Registro creado correctamente", "success")
            return redirect(url_for('participa_semillero.index'))
        else:
            flash(mensaje, "danger")

    return render_template('pages/participa_semillero/crear.html')


@bp.route('/participa-semillero/editar/<registro_id>', methods=['GET', 'POST'])
def editar(registro_id):
    if request.method == 'POST':
        datos = {
            'semillero': request.form.get('semillero'),
            'rol': request.form.get('rol'),
            'fecha_inicio': request.form.get('fecha_inicio'),
            'fecha_fin': request.form.get('fecha_fin') or None,
        }

        exito, mensaje = api.actualizar(TABLA, CLAVE, registro_id, datos)

        if exito:
            flash("Registro actualizado correctamente", "success")
            return redirect(url_for('participa_semillero.index'))
        else:
            flash(mensaje, "danger")

    registros = api.listar(TABLA)
    registro = next((r for r in registros if str(r.get(CLAVE)) == str(registro_id)), None)

    if not registro:
        flash("Registro no encontrado", "danger")
        return redirect(url_for('participa_semillero.index'))

    return render_template('pages/participa_semillero/editar.html', registro=registro)


@bp.route('/participa-semillero/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('semillero')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)

    if exito:
        flash("Registro eliminado correctamente", "success")
    else:
        flash(mensaje, "danger")

    return redirect(url_for('participa_semillero.index'))