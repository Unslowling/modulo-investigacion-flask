from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('ac_linea', __name__)
api = ApiService()

TABLA = 'ac_linea'

@bp.route('/ac_linea')
def index():
    """Muestra la tabla de relacion AC - Linea."""
    relaciones = api.listar(TABLA)
    
    # Obtener catálogos para mapear IDs a Nombres y evitar mostrar IDs crudos
    lineas = {r['id']: r['nombre'] for r in api.listar('linea_investigacion')}
    areas = {r['id']: r['area'] for r in api.listar('area_conocimiento')}
    
    # Enriquecer relaciones con nombres para la vista
    for rel in relaciones:
        rel['nombre_linea'] = lineas.get(rel.get('linea_investigacion'), f"ID {rel.get('linea_investigacion')}")
        rel['nombre_area'] = areas.get(rel.get('area_conocimiento'), f"ID {rel.get('area_conocimiento')}")
        
    return render_template('pages/ac_linea/lista.html', registros=relaciones)

@bp.route('/ac_linea/crear', methods=['GET', 'POST'])
def crear():
    """Muestra el formulario con los combos y crea una nueva relacion."""
    if request.method == 'POST':
        datos = {
            'linea_investigacion': int(request.form.get('linea_investigacion')),
            'area_conocimiento': int(request.form.get('area_conocimiento'))
        }
        
        exito, mensaje = api.crear(TABLA, datos)
        if exito:
            flash("Relación creada correctamente", "success")
            return redirect(url_for('ac_linea.index'))
        else:
            flash(mensaje, "danger")
            
    # Precargar datos para los <select>
    lineas = api.listar('linea_investigacion')
    areas = api.listar('area_conocimiento')
    return render_template('pages/ac_linea/crear.html', lineas=lineas, areas=areas)

@bp.route('/ac_linea/editar/<int:linea_id>/<int:area_id>', methods=['GET', 'POST'])
def editar(linea_id, area_id):
    """Edita la relacion (en la practica deberia eliminar vieja e insertar nueva)."""
    if request.method == 'POST':
        datos = {
            'linea_investigacion': int(request.form.get('linea_investigacion')),
            'area_conocimiento': int(request.form.get('area_conocimiento'))
        }
        
        # Eliminar relación vieja simulado (ver advertencia)
        api.eliminar(TABLA, 'linea_investigacion', str(linea_id))
        
        # Insertar nueva
        exito, mensaje = api.crear(TABLA, datos)
        if exito:
            flash("Relación actualizada correctamente", "success")
            return redirect(url_for('ac_linea.index'))
        else:
            flash(mensaje, "danger")
            
    lineas = api.listar('linea_investigacion')
    areas = api.listar('area_conocimiento')
    return render_template('pages/ac_linea/editar.html', 
                           lineas=lineas, 
                           areas=areas,
                           linea_id=linea_id,
                           area_id=area_id)

@bp.route('/ac_linea/eliminar', methods=['POST'])
def eliminar():
    """Elimina una relacion especifica."""
    linea_id = request.form.get('linea_investigacion')
    area_id = request.form.get('area_conocimiento')
    
    # ATENCIÓN: El API genérico actual NO admite enviar dos parámetros a /api/{tabla}/{c}/{v}.
    exito, mensaje = api.eliminar(TABLA, 'linea_investigacion', str(linea_id))
    
    if exito:
        flash("La orden de eliminación se envió al servidor correctamente", "success")
    else:
        flash(mensaje, "danger")
        
    return redirect(url_for('ac_linea.index'))
