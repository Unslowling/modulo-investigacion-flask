from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('semillero_linea', __name__)
api = ApiService()

TABLA = 'semillero_linea'
CLAVE = 'semillero'


@bp.route('/semillero-linea')
def index():
    registros = api.listar(TABLA)
    return render_template('pages/semillero_linea/lista.html', registros=registros)


@bp.route('/semillero-linea/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        datos = {
            'semillero': request.form.get('semillero'),
            'linea_investigacion': request.form.get('linea_investigacion')
        }

        exito, mensaje = api.crear(TABLA, datos)

        if exito:
            flash("Relación creada correctamente", "success")
            return redirect(url_for('semillero_linea.index'))
        else:
            flash(mensaje, "danger")

    return render_template('pages/semillero_linea/crear.html')


@bp.route('/semillero-linea/editar/<semillero>', methods=['GET', 'POST'])
def editar(semillero):
    if request.method == 'POST':
        datos = {
            'linea_investigacion': request.form.get('linea_investigacion')
        }

        exito, mensaje = api.actualizar(TABLA, CLAVE, semillero, datos)

        if exito:
            flash("Relación actualizada", "success")
            return redirect(url_for('semillero_linea.index'))
        else:
            flash(mensaje, "danger")

    registros = api.listar(TABLA)
    registro = next((r for r in registros if str(r.get('semillero')) == str(semillero)), None)

    return render_template('pages/semillero_linea/editar.html', registro=registro)


@bp.route('/semillero-linea/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('semillero')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)

    if exito:
        flash("Relación eliminada", "success")
    else:
        flash(mensaje, "danger")

    return redirect(url_for('semillero_linea.index'))