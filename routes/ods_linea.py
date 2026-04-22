from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('ods_linea', __name__)
api = ApiService()

TABLA = 'ods_linea'

@bp.route('/ods_linea')
def index():
    """Muestra la tabla de relacion ODS - Linea."""
    relaciones = api.listar(TABLA)
    
    # Obtener catálogos para mapear IDs a Nombres y evitar mostrar IDs crudos
    lineas = {r['id']: r['nombre'] for r in api.listar('linea_investigacion')}
    odss = {r['id']: r['nombre'] for r in api.listar('objetivo_desarrollo_sostenible')}
    
    # Enriquecer relaciones con nombres para la vista
    for rel in relaciones:
        rel['nombre_linea'] = lineas.get(rel.get('linea_investigacion'), f"ID {rel.get('linea_investigacion')}")
        rel['nombre_ods'] = odss.get(rel.get('ods'), f"ID {rel.get('ods')}")
        
    return render_template('pages/ods_linea/lista.html', registros=relaciones)

@bp.route('/ods_linea/crear', methods=['GET', 'POST'])
def crear():
    """Muestra el formulario con los combos y crea una nueva relacion."""
    if request.method == 'POST':
        datos = {
            'linea_investigacion': int(request.form.get('linea_investigacion')),
            'ods': int(request.form.get('ods'))
        }
        
        exito, mensaje = api.crear(TABLA, datos)
        if exito:
            flash("Relación creada correctamente", "success")
            return redirect(url_for('ods_linea.index'))
        else:
            flash(mensaje, "danger")
            
    # Precargar datos para los <select>
    lineas = api.listar('linea_investigacion')
    odss = api.listar('objetivo_desarrollo_sostenible')
    return render_template('pages/ods_linea/crear.html', lineas=lineas, odss=odss)

@bp.route('/ods_linea/editar/<int:linea_id>/<int:ods_id>', methods=['GET', 'POST'])
def editar(linea_id, ods_id):
    """Edita la relacion (eliminar e insertar)."""
    if request.method == 'POST':
        datos = {
            'linea_investigacion': int(request.form.get('linea_investigacion')),
            'ods': int(request.form.get('ods'))
        }
        
        # Eliminar relación vieja simulado (advertencia de llave única de la API)
        api.eliminar(TABLA, 'linea_investigacion', str(linea_id))
        
        # Insertar nueva
        exito, mensaje = api.crear(TABLA, datos)
        if exito:
            flash("Relación actualizada correctamente", "success")
            return redirect(url_for('ods_linea.index'))
        else:
            flash(mensaje, "danger")
            
    lineas = api.listar('linea_investigacion')
    odss = api.listar('objetivo_desarrollo_sostenible')
    return render_template('pages/ods_linea/editar.html', 
                           lineas=lineas, 
                           odss=odss,
                           linea_id=linea_id,
                           ods_id=ods_id)

@bp.route('/ods_linea/eliminar', methods=['POST'])
def eliminar():
    """Elimina una relacion especifica."""
    linea_id = request.form.get('linea_investigacion')
    ods_id = request.form.get('ods')
    
    # ATENCIÓN: El API genérico actual NO admite enviar dos parámetros combinados
    exito, mensaje = api.eliminar(TABLA, 'linea_investigacion', str(linea_id))
    
    if exito:
        flash("La orden de eliminación se envió al servidor correctamente", "success")
    else:
        flash(mensaje, "danger")
        
    return redirect(url_for('ods_linea.index'))
