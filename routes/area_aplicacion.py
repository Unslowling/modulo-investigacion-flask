from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('area_aplicacion', __name__)
api = ApiService()

TABLA = 'area_aplicacion'
CLAVE = 'id'

@bp.route('/area_aplicacion')
def index():
    """Muestra la tabla de áreas de aplicación."""
    registros = api.listar(TABLA)
    return render_template('pages/area_aplicacion/lista.html', registros=registros)

@bp.route('/area_aplicacion/crear', methods=['GET', 'POST'])
def crear():
    """Muestra el formulario y crea una nueva área de aplicación."""
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre', '').strip()
        }
        
        exito, mensaje = api.crear(TABLA, datos)
        if exito:
            flash("Registro creado correctamente", "success")
            return redirect(url_for('area_aplicacion.index'))
        else:
            flash(mensaje, "danger")
            
    return render_template('pages/area_aplicacion/crear.html')

@bp.route('/area_aplicacion/editar/<registro_id>', methods=['GET', 'POST'])
def editar(registro_id):
    """Muestra el formulario precargado y actualiza una área de aplicación."""
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre', '').strip()
        }
        
        exito, mensaje = api.actualizar(TABLA, CLAVE, registro_id, datos)
        if exito:
            flash("Registro actualizado correctamente", "success")
            return redirect(url_for('area_aplicacion.index'))
        else:
            flash(mensaje, "danger")
            
    registros = api.listar(TABLA)
    registro = next((r for r in registros if str(r.get(CLAVE)) == str(registro_id)), None)
    
    if not registro:
        flash("Área de aplicación no encontrada", "danger")
        return redirect(url_for('area_aplicacion.index'))

    return render_template('pages/area_aplicacion/editar.html', registro=registro)

@bp.route('/area_aplicacion/eliminar', methods=['POST'])
def eliminar():
    """Elimina una área de aplicación."""
    valor = request.form.get('id', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    
    if exito:
        flash("Registro eliminado correctamente", "success")
    else:
        flash(mensaje, "danger")
        
    return redirect(url_for('area_aplicacion.index'))
