from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('area_conocimiento', __name__)
api = ApiService()

TABLA = 'area_conocimiento'
CLAVE = 'id'

@bp.route('/area_conocimiento')
def index():
    """Muestra la tabla de áreas de conocimiento."""
    registros = api.listar(TABLA)
    return render_template('pages/area_conocimiento/lista.html', registros=registros)

@bp.route('/area_conocimiento/crear', methods=['GET', 'POST'])
def crear():
    """Muestra el formulario y crea una nueva área de conocimiento."""
    if request.method == 'POST':
        datos = {
            'gran_area': request.form.get('gran_area', '').strip(),
            'area': request.form.get('area', '').strip(),
            'disciplina': request.form.get('disciplina', '').strip()
        }
        
        exito, mensaje = api.crear(TABLA, datos)
        if exito:
            flash("Registro creado correctamente", "success")
            return redirect(url_for('area_conocimiento.index'))
        else:
            flash(mensaje, "danger")
            
    return render_template('pages/area_conocimiento/crear.html')

@bp.route('/area_conocimiento/editar/<registro_id>', methods=['GET', 'POST'])
def editar(registro_id):
    """Muestra el formulario precargado y actualiza una área de conocimiento."""
    if request.method == 'POST':
        datos = {
            'gran_area': request.form.get('gran_area', '').strip(),
            'area': request.form.get('area', '').strip(),
            'disciplina': request.form.get('disciplina', '').strip()
        }
        
        exito, mensaje = api.actualizar(TABLA, CLAVE, registro_id, datos)
        if exito:
            flash("Registro actualizado correctamente", "success")
            return redirect(url_for('area_conocimiento.index'))
        else:
            flash(mensaje, "danger")
            
    registros = api.listar(TABLA)
    registro = next((r for r in registros if str(r.get(CLAVE)) == str(registro_id)), None)
    
    if not registro:
        flash("Área de conocimiento no encontrada", "danger")
        return redirect(url_for('area_conocimiento.index'))

    return render_template('pages/area_conocimiento/editar.html', registro=registro)

@bp.route('/area_conocimiento/eliminar', methods=['POST'])
def eliminar():
    """Elimina una área de conocimiento."""
    valor = request.form.get('id', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    
    if exito:
        flash("Registro eliminado correctamente", "success")
    else:
        flash(mensaje, "danger")
        
    return redirect(url_for('area_conocimiento.index'))
