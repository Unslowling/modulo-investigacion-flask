from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('grupo_linea', __name__)
api = ApiService()

TABLA = 'grupo_linea'
CLAVE = 'grupo_investigacion'


@bp.route('/grupo-linea')
def index():
    registros = api.listar(TABLA)
    return render_template('pages/grupo_linea/lista.html', registros=registros)


@bp.route('/grupo-linea/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        datos = {
            'grupo_investigacion': request.form.get('grupo_investigacion'),
            'linea_investigacion': request.form.get('linea_investigacion')
        }

        exito, mensaje = api.crear(TABLA, datos)

        if exito:
            flash("Relación creada correctamente", "success")
            return redirect(url_for('grupo_linea.index'))
        else:
            flash(mensaje, "danger")

    return render_template('pages/grupo_linea/crear.html')


@bp.route('/grupo-linea/editar/<grupo>', methods=['GET', 'POST'])
def editar(grupo):
    if request.method == 'POST':
        datos = {
            'linea_investigacion': request.form.get('linea_investigacion')
        }

        exito, mensaje = api.actualizar(TABLA, CLAVE, grupo, datos)

        if exito:
            flash("Relación actualizada", "success")
            return redirect(url_for('grupo_linea.index'))
        else:
            flash(mensaje, "danger")

    registros = api.listar(TABLA)
    registro = next((r for r in registros if str(r.get('grupo_investigacion')) == str(grupo)), None)

    return render_template('pages/grupo_linea/editar.html', registro=registro)


@bp.route('/grupo-linea/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('grupo_investigacion')

    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)

    if exito:
        flash("Relación eliminada", "success")
    else:
        flash(mensaje, "danger")

    return redirect(url_for('grupo_linea.index'))