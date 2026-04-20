from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('linea_investigacion', __name__)
api = ApiService()

TABLA = 'linea_investigacion'
CLAVE = 'id'

@bp.route('/linea-investigacion')
def index():
    """Muestra la tabla de líneas de investigación."""
    # Obtener registros de la API
    registros = api.listar(TABLA)
    return render_template('pages/linea_investigacion/lista.html', registros=registros)

@bp.route('/linea-investigacion/crear', methods=['GET', 'POST'])
def crear():
    """Muestra el formulario y crea una nueva línea de investigación."""
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre', ''),
            'descripcion': request.form.get('descripcion', '')
        }
        
        exito, mensaje = api.crear(TABLA, datos)
        if exito:
            flash("Registro creado correctamente", "success")
            return redirect(url_for('linea_investigacion.index'))
        else:
            flash(mensaje, "danger")
            
    return render_template('pages/linea_investigacion/crear.html')

@bp.route('/linea-investigacion/editar/<id>', methods=['GET', 'POST'])
def editar(id):
    """Muestra el formulario precargado y actualiza una línea de investigación."""
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre', ''),
            'descripcion': request.form.get('descripcion', '')
        }
        
        exito, mensaje = api.actualizar(TABLA, CLAVE, id, datos)
        if exito:
            flash("Registro actualizado correctamente", "success")
            return redirect(url_for('linea_investigacion.index'))
        else:
            flash(mensaje, "danger")
            
    # GET: Buscar los datos actuales del registro
    registros = api.listar(TABLA)
    # Extraer el registro que coincide con el ID
    registro = next((r for r in registros if str(r.get(CLAVE)) == str(id)), None)
    
    if not registro:
        flash("Línea de investigación no encontrada", "danger")
        return redirect(url_for('linea_investigacion.index'))

    return render_template('pages/linea_investigacion/editar.html', registro=registro)

@bp.route('/linea-investigacion/eliminar', methods=['POST'])
def eliminar():
    """Elimina una línea de investigación."""
    valor = request.form.get('id', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    
    if exito:
        flash("Registro eliminado correctamente", "success")
    else:
        flash(mensaje, "danger")
        
    return redirect(url_for('linea_investigacion.index'))
