from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('aa_linea', __name__)
api = ApiService()

TABLA = 'aa_linea'

@bp.route('/aa_linea')
def index():
    """Muestra la tabla de relacion Area Aplicacion - Linea."""
    relaciones = api.listar(TABLA)
    
    # Obtener catálogos para mapear IDs a Nombres y evitar mostrar IDs crudos
    lineas = {r['id']: r['nombre'] for r in api.listar('linea_investigacion')}
    areas = {r['id']: r['nombre'] for r in api.listar('area_aplicacion')}
    
    # Enriquecer relaciones con nombres para la vista
    for rel in relaciones:
        rel['nombre_linea'] = lineas.get(rel.get('linea_investigacion'), f"ID {rel.get('linea_investigacion')}")
        rel['nombre_area'] = areas.get(rel.get('area_aplicacion'), f"ID {rel.get('area_aplicacion')}")
        
    return render_template('pages/aa_linea/lista.html', registros=relaciones)

@bp.route('/aa_linea/crear', methods=['GET', 'POST'])
def crear():
    """Muestra el formulario con los combos y crea una nueva relacion."""
    if request.method == 'POST':
        datos = {
            'area_aplicacion': int(request.form.get('area_aplicacion')),
            'linea_investigacion': int(request.form.get('linea_investigacion'))
        }
        
        exito, mensaje = api.crear(TABLA, datos)
        if exito:
            flash("Relación creada correctamente", "success")
            return redirect(url_for('aa_linea.index'))
        else:
            flash(mensaje, "danger")
            
    # Precargar datos para los <select>
    areas = api.listar('area_aplicacion')
    lineas = api.listar('linea_investigacion')
    return render_template('pages/aa_linea/crear.html', areas=areas, lineas=lineas)

@bp.route('/aa_linea/editar/<int:area_id>/<int:linea_id>', methods=['GET', 'POST'])
def editar(area_id, linea_id):
    """Edita la relacion (en la practica eliminaria vieja e inserta nueva)."""
    if request.method == 'POST':
        datos = {
            'area_aplicacion': int(request.form.get('area_aplicacion')),
            'linea_investigacion': int(request.form.get('linea_investigacion'))
        }
        
        # Eliminar relación vieja simulado (ver advertencia en codigo previo)
        api.eliminar(TABLA, 'area_aplicacion', str(area_id))
        
        # Insertar nueva
        exito, mensaje = api.crear(TABLA, datos)
        if exito:
            flash("Relación actualizada correctamente", "success")
            return redirect(url_for('aa_linea.index'))
        else:
            flash(mensaje, "danger")
            
    areas = api.listar('area_aplicacion')
    lineas = api.listar('linea_investigacion')
    return render_template('pages/aa_linea/editar.html', 
                           areas=areas, 
                           lineas=lineas,
                           area_id=area_id,
                           linea_id=linea_id)

@bp.route('/aa_linea/eliminar', methods=['POST'])
def eliminar():
    """Elimina una relacion especifica."""
    area_id = request.form.get('area_aplicacion')
    linea_id = request.form.get('linea_investigacion')
    
    # ATENCIÓN: El API genérico actual NO admite enviar dos parámetros.
    exito, mensaje = api.eliminar(TABLA, 'area_aplicacion', str(area_id))
    
    if exito:
        flash("La orden de eliminación se envió al servidor correctamente", "success")
    else:
        flash(mensaje, "danger")
        
    return redirect(url_for('aa_linea.index'))
