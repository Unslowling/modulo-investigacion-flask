from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('objetivo_desarrollo_sostenible', __name__)
api = ApiService()

TABLA = 'objetivo_desarrollo_sostenible'
CLAVE = 'id'

@bp.route('/objetivo_desarrollo_sostenible')
def index():
    """Muestra la tabla de objetivos de desarrollo sostenible."""
    registros = api.listar(TABLA)
    return render_template('pages/objetivo_desarrollo_sostenible/lista.html', registros=registros)

@bp.route('/objetivo_desarrollo_sostenible/crear', methods=['GET', 'POST'])
def crear():
    """Muestra el formulario y crea un nuevo ODS."""
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre', '').strip(),
            'categoria': request.form.get('categoria', '').strip()
        }
        
        exito, mensaje = api.crear(TABLA, datos)
        if exito:
            flash("Registro creado correctamente", "success")
            return redirect(url_for('objetivo_desarrollo_sostenible.index'))
        else:
            flash(mensaje, "danger")
            
    return render_template('pages/objetivo_desarrollo_sostenible/crear.html')

@bp.route('/objetivo_desarrollo_sostenible/editar/<registro_id>', methods=['GET', 'POST'])
def editar(registro_id):
    """Muestra el formulario precargado y actualiza un ODS."""
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre', '').strip(),
            'categoria': request.form.get('categoria', '').strip()
        }
        
        exito, mensaje = api.actualizar(TABLA, CLAVE, registro_id, datos)
        if exito:
            flash("Registro actualizado correctamente", "success")
            return redirect(url_for('objetivo_desarrollo_sostenible.index'))
        else:
            flash(mensaje, "danger")
            
    registros = api.listar(TABLA)
    registro = next((r for r in registros if str(r.get(CLAVE)) == str(registro_id)), None)
    
    if not registro:
        flash("ODS no encontrado", "danger")
        return redirect(url_for('objetivo_desarrollo_sostenible.index'))

    return render_template('pages/objetivo_desarrollo_sostenible/editar.html', registro=registro)

@bp.route('/objetivo_desarrollo_sostenible/eliminar', methods=['POST'])
def eliminar():
    """Elimina un ODS."""
    valor = request.form.get('id', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    
    if exito:
        flash("Registro eliminado correctamente", "success")
    else:
        flash(mensaje, "danger")
        
    return redirect(url_for('objetivo_desarrollo_sostenible.index'))
