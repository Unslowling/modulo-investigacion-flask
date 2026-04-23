from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('grupo_investigacion', __name__)
api = ApiService()

TABLA = 'grupo_investigacion'
CLAVE = 'id'


@bp.route('/grupo-investigacion')
def index():
    registros = api.listar(TABLA)
    return render_template('pages/grupo_investigacion/lista.html', registros=registros)


@bp.route('/grupo-investigacion/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre'),
            'url_gruplac': request.form.get('url_gruplac'),
            'categoria': request.form.get('categoria'),
            'convocatoria': request.form.get('convocatoria'),
            'fecha_fundacion': request.form.get('fecha_fundacion'),
            'universidad_id': request.form.get('universidad_id'),
            'interno': request.form.get('interno'),
            'ambito': request.form.get('ambito'),
        }

        exito, mensaje = api.crear(TABLA, datos)

        if exito:
            flash("Grupo creado correctamente", "success")
            return redirect(url_for('grupo_investigacion.index'))
        else:
            flash(mensaje, "danger")

    return render_template('pages/grupo_investigacion/crear.html')


@bp.route('/grupo-investigacion/editar/<registro_id>', methods=['GET', 'POST'])
def editar(registro_id):
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre'),
            'url_gruplac': request.form.get('url_gruplac'),
            'categoria': request.form.get('categoria'),
            'convocatoria': request.form.get('convocatoria'),
            'fecha_fundacion': request.form.get('fecha_fundacion'),
            'universidad_id': request.form.get('universidad_id'),
            'interno': request.form.get('interno'),
            'ambito': request.form.get('ambito'),
        }

        exito, mensaje = api.actualizar(TABLA, CLAVE, registro_id, datos)

        if exito:
            flash("Grupo actualizado correctamente", "success")
            return redirect(url_for('grupo_investigacion.index'))
        else:
            flash(mensaje, "danger")

    registros = api.listar(TABLA)
    registro = next((r for r in registros if str(r.get(CLAVE)) == str(registro_id)), None)

    if not registro:
        flash("Grupo no encontrado", "danger")
        return redirect(url_for('grupo_investigacion.index'))

    return render_template('pages/grupo_investigacion/editar.html', registro=registro)


@bp.route('/grupo-investigacion/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('id')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)

    if exito:
        flash("Grupo eliminado correctamente", "success")
    else:
        flash(mensaje, "danger")

    return redirect(url_for('grupo_investigacion.index'))