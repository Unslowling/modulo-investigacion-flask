from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('participa_grupo', __name__)
api = ApiService()

TABLA = 'participa_grupo'
CLAVE = 'docente_cedula'  # clave principal (ajústalo si tu PK es compuesta)


@bp.route('/participa-grupo')
def index():
    registros = api.listar(TABLA)
    return render_template('pages/participa_grupo/lista.html', registros=registros)


@bp.route('/participa-grupo/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        datos = {
            'docente_cedula': request.form.get('docente_cedula'),
            'grupo_investigacion_id': request.form.get('grupo_investigacion_id'),
            'rol': request.form.get('rol'),
            'fecha_inicio': request.form.get('fecha_inicio'),
            'fecha_fin': request.form.get('fecha_fin') or None,
        }

        exito, mensaje = api.crear(TABLA, datos)

        if exito:
            flash("Registro creado correctamente", "success")
            return redirect(url_for('participa_grupo.index'))
        else:
            flash(mensaje, "danger")

    return render_template('pages/participa_grupo/crear.html')


@bp.route('/participa-grupo/editar/<registro_id>', methods=['GET', 'POST'])
def editar(registro_id):
    if request.method == 'POST':
        datos = {
            'grupo_investigacion_id': request.form.get('grupo_investigacion_id'),
            'rol': request.form.get('rol'),
            'fecha_inicio': request.form.get('fecha_inicio'),
            'fecha_fin': request.form.get('fecha_fin') or None,
        }

        exito, mensaje = api.actualizar(TABLA, CLAVE, registro_id, datos)

        if exito:
            flash("Registro actualizado correctamente", "success")
            return redirect(url_for('participa_grupo.index'))
        else:
            flash(mensaje, "danger")

    registros = api.listar(TABLA)
    registro = next((r for r in registros if str(r.get(CLAVE)) == str(registro_id)), None)

    if not registro:
        flash("Registro no encontrado", "danger")
        return redirect(url_for('participa_grupo.index'))

    return render_template('pages/participa_grupo/editar.html', registro=registro)


@bp.route('/participa-grupo/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('docente_cedula')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)

    if exito:
        flash("Registro eliminado correctamente", "success")
    else:
        flash(mensaje, "danger")

    return redirect(url_for('participa_grupo.index'))