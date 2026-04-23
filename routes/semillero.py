from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('semillero', __name__)
api = ApiService()

TABLA = 'semillero'
CLAVE = 'id'


@bp.route('/semillero')
def index():
    registros = api.listar(TABLA)
    return render_template('pages/semillero/lista.html', registros=registros)


@bp.route('/semillero/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre'),
            'fecha_fundacion': request.form.get('fecha_fundacion'),
            'grupo_investigacion': request.form.get('grupo_investigacion'),
        }

        exito, mensaje = api.crear(TABLA, datos)

        if exito:
            flash("Semillero creado correctamente", "success")
            return redirect(url_for('semillero.index'))
        else:
            flash(mensaje, "danger")

    return render_template('pages/semillero/crear.html')


@bp.route('/semillero/editar/<registro_id>', methods=['GET', 'POST'])
def editar(registro_id):
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre'),
            'fecha_fundacion': request.form.get('fecha_fundacion'),
            'grupo_investigacion': request.form.get('grupo_investigacion'),
        }

        exito, mensaje = api.actualizar(TABLA, CLAVE, registro_id, datos)

        if exito:
            flash("Semillero actualizado correctamente", "success")
            return redirect(url_for('semillero.index'))
        else:
            flash(mensaje, "danger")

    registros = api.listar(TABLA)
    registro = next((r for r in registros if str(r.get(CLAVE)) == str(registro_id)), None)

    if not registro:
        flash("Semillero no encontrado", "danger")
        return redirect(url_for('semillero.index'))

    return render_template('pages/semillero/editar.html', registro=registro)


@bp.route('/semillero/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('id')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)

    if exito:
        flash("Semillero eliminado correctamente", "success")
    else:
        flash(mensaje, "danger")

    return redirect(url_for('semillero.index'))