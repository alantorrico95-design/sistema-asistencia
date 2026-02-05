from flask import Blueprint, request, jsonify, send_file
from backend.app import db
from backend.app.modelos import Persona, Administrador, Empleado, Horario, Asistencia, Permiso
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
import qrcode
import io

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/login', methods=['POST'])
def login():
    datos = request.json
    identificador = (datos.get('correo') or datos.get('dni') or "").strip()
    password = (datos.get('password') or "").strip()
    
    print(f"DEBUG LOGIN: Intentando entrar con ID: {identificador}")
    
    # 1. Intentar como Administrador
    admin = Administrador.query.filter_by(correo=identificador).first()
    if admin:
        print(f"DEBUG LOGIN: Encontrado Administrador. Verificando pass...")
        if check_password_hash(admin.contraseña, password):
            return jsonify({
                'mensaje': 'Login exitoso (Administrador)', 
                'status': 'success', 
                'rol': 'admin',
                'nombre': admin.persona.nombre
            })
    
    # 2. Intentar como Empleado
    persona = Persona.query.filter_by(dni=identificador).first()
    if persona and persona.empleado:
        print(f"DEBUG LOGIN: Encontrado Empleado (DNI: {persona.dni}). Verificando pass...")
        if check_password_hash(persona.empleado.contraseña, password):
            return jsonify({
                'mensaje': 'Login exitoso (Empleado)', 
                'status': 'success', 
                'rol': 'empleado',
                'dni': persona.dni,
                'nombre': f"{persona.nombre} {persona.apellido}"
            })
            
    return jsonify({'mensaje': 'Credenciales inválidas', 'status': 'error'}), 401

@bp.route('/marcar', methods=['POST'])
def marcar_asistencia():
    datos = request.json
    dni = datos.get('dni')
    
    persona = Persona.query.filter_by(dni=dni).first()
    if not persona or not persona.empleado or persona.empleado.estado != 'Activo':
        return jsonify({'mensaje': 'Empleado no encontrado o inactivo', 'status': 'error'}), 404

    empleado = persona.empleado
    ahora = datetime.now()
    hoy = ahora.date()
    hora_actual = ahora.time()
    
    # Lógica de Marcado: Buscamos si ya tiene un registro de asistencia hoy
    asistencia = Asistencia.query.filter_by(
        idEmpleado=empleado.id, 
        fecha=hoy
    ).first()
    
    if not asistencia:
        # Registrar Entrada
        horario = empleado.horario
        entrada_prog = datetime.combine(hoy, horario.horario_inicio)
        margen = timedelta(minutes=10)
        
        estado_msg = "Puntual"
        if ahora > entrada_prog + margen:
            estado_msg = "Tarde"
            
        nueva_asistencia = Asistencia(
            fecha=hoy,
            hora_entrada=hora_actual,
            idEmpleado=empleado.id
        )
        db.session.add(nueva_asistencia)
        db.session.commit()
        return jsonify({
            'mensaje': f'Entrada marcada: {estado_msg}', 
            'status': 'success', 
            'nombre': f'{persona.nombre} {persona.apellido}'
        })
    
    elif asistencia.hora_salida is None:
        # Registrar Salida
        asistencia.hora_salida = hora_actual
        db.session.commit()
        return jsonify({
            'mensaje': 'Salida marcada', 
            'status': 'success', 
            'nombre': f'{persona.nombre} {persona.apellido}'
        })
    else:
        return jsonify({'mensaje': 'Ya se marcaron entrada y salida hoy', 'status': 'warning'}), 400

@bp.route('/asistencias/hoy', methods=['GET'])
def asistencias_hoy():
    hoy = datetime.now().date()
    asistencias = Asistencia.query.filter_by(fecha=hoy).all()
    resultado = []
    for a in asistencias:
        # Calcular horas trabajadas si ya salió
        horas_trabajadas = "---"
        if a.hora_entrada and a.hora_salida:
            e = datetime.combine(hoy, a.hora_entrada)
            s = datetime.combine(hoy, a.hora_salida)
            diff = s - e
            segundos = diff.total_seconds()
            horas = int(segundos // 3600)
            minutos = int((segundos % 3600) // 60)
            horas_trabajadas = f"{horas}h {minutos}m"

        resultado.append({
            'nombre': f'{a.empleado.persona.nombre} {a.empleado.persona.apellido}',
            'entrada': a.hora_entrada.strftime('%H:%M:%S'),
            'salida': a.hora_salida.strftime('%H:%M:%S') if a.hora_salida else 'Pendiente',
            'dni': a.empleado.persona.dni,
            'horas': horas_trabajadas
        })
    return jsonify(resultado)

@bp.route('/admin/reporte/general', methods=['GET'])
def reporte_general():
    asistencias = Asistencia.query.order_by(Asistencia.fecha.desc()).all()
    resultado = []
    for a in asistencias:
        status = "Puntual"
        horario = a.empleado.horario
        entrada_prog = datetime.combine(a.fecha, horario.horario_inicio)
        margen = timedelta(minutes=10)
        ahora_entrada = datetime.combine(a.fecha, a.hora_entrada)
        
        if ahora_entrada > entrada_prog + margen:
            status = "Tarde"

        horas_trabajadas = "---"
        if a.hora_entrada and a.hora_salida:
            e = datetime.combine(a.fecha, a.hora_entrada)
            s = datetime.combine(a.fecha, a.hora_salida)
            diff = s - e
            segundos = diff.total_seconds()
            horas = int(segundos // 3600)
            minutos = int((segundos % 3600) // 60)
            horas_trabajadas = f"{horas}h {minutos}m"

        resultado.append({
            'fecha': a.fecha.strftime('%Y-%m-%d'),
            'nombre': f'{a.empleado.persona.nombre} {a.empleado.persona.apellido}',
            'dni': a.empleado.persona.dni,
            'entrada': a.hora_entrada.strftime('%H:%M:%S'),
            'salida': a.hora_salida.strftime('%H:%M:%S') if a.hora_salida else 'Pendiente',
            'estado': status,
            'horas': horas_trabajadas
        })
    return jsonify(resultado)

@bp.route('/admin/reporte/tardanzas', methods=['GET'])
def reporte_tardanzas():
    asistencias = Asistencia.query.all()
    resultado = []
    for a in asistencias:
        horario = a.empleado.horario
        entrada_prog = datetime.combine(a.fecha, horario.horario_inicio)
        margen = timedelta(minutes=10)
        ahora_entrada = datetime.combine(a.fecha, a.hora_entrada)
        
        if ahora_entrada > entrada_prog + margen:
            resultado.append({
                'fecha': a.fecha.strftime('%Y-%m-%d'),
                'nombre': f'{a.empleado.persona.nombre} {a.empleado.persona.apellido}',
                'dni': a.empleado.persona.dni,
                'entrada': a.hora_entrada.strftime('%H:%M:%S'),
                'retraso': str(ahora_entrada - entrada_prog)
            })
    return jsonify(resultado)

# NUEVAS RUTAS: CÓDIGOS QR Y PANEL PERSONAL

@bp.route('/empleado/<dni>/qr', methods=['GET'])
def generar_qr(dni):
    persona = Persona.query.filter_by(dni=dni).first()
    if not persona:
        return jsonify({'error': 'Empleado no encontrado'}), 404
    
    img = qrcode.make(dni)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@bp.route('/empleado/<dni>/datos', methods=['GET'])
def obtener_datos_empleado(dni):
    persona = Persona.query.filter_by(dni=dni).first()
    if not persona or not persona.empleado:
        return jsonify({'error': 'Empleado no encontrado'}), 404
    
    asistencias = []
    for a in persona.empleado.asistencias:
        asistencias.append({
            'fecha': a.fecha.strftime('%Y-%m-%d'),
            'entrada': a.hora_entrada.strftime('%H:%M:%S'),
            'salida': a.hora_salida.strftime('%H:%M:%S') if a.hora_salida else '---'
        })
        
    permisos = []
    for p in persona.empleado.asistencias:
        if p.permiso:
            permisos.append({
                'fecha': p.permiso.fecha.strftime('%Y-%m-%d'),
                'tipo': p.permiso.nombre,
                'descripcion': p.permiso.descripcion
            })
            
    horario = persona.empleado.horario
    return jsonify({
        'nombre': f'{persona.nombre} {persona.apellido}',
        'dni': persona.dni,
        'horario': {
            'turno': horario.turno,
            'inicio': horario.horario_inicio.strftime('%H:%M'),
            'fin': horario.horario_fin.strftime('%H:%M'),
            'dias': horario.dias or "Todos los días"
        },
        'asistencias': asistencias,
        'permisos': permisos
    })

# RUTAS ADMINISTRATIVAS: GESTIÓN DE PERSONAL

@bp.route('/admin/empleados', methods=['GET'])
def listar_empleados():
    empleados = Empleado.query.all()
    resultado = []
    for e in empleados:
        resultado.append({
            'id': e.id,
            'dni': e.persona.dni,
            'nombre': e.persona.nombre,
            'apellido': e.persona.apellido,
            'idHorario': e.idHorario,
            'horario': e.horario.turno,
            'estado': e.estado
        })
    return jsonify(resultado)

@bp.route('/admin/horarios', methods=['GET'])
def listar_horarios():
    horarios = Horario.query.all()
    return jsonify([{
        'id': h.id,
        'turno': h.turno,
        'inicio': h.horario_inicio.strftime('%H:%M'),
        'fin': h.horario_fin.strftime('%H:%M'),
        'dias': h.dias or "No definido"
    } for h in horarios])

@bp.route('/admin/empleado/crear', methods=['POST'])
def crear_empleado():
    datos = request.json
    try:
        nueva_persona = Persona(
            dni=datos['dni'],
            nombre=datos['nombre'],
            apellido=datos['apellido']
        )
        db.session.add(nueva_persona)
        db.session.flush()
        
        nuevo_empleado = Empleado(
            id=nueva_persona.id,
            idHorario=datos['idHorario'],
            estado='Activo',
            contraseña=generate_password_hash('12345')
        )
        db.session.add(nuevo_empleado)
        db.session.commit()
        return jsonify({'mensaje': 'Empleado creado correctamente', 'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': f'Error al crear: {str(e)}', 'status': 'error'}), 400

@bp.route('/admin/empleado/editar/<int:id>', methods=['PUT', 'POST'])
def editar_empleado(id):
    datos = request.json
    empleado = Empleado.query.get_or_404(id)
    persona = empleado.persona
    
    try:
        persona.dni = datos.get('dni', persona.dni)
        persona.nombre = datos.get('nombre', persona.nombre)
        persona.apellido = datos.get('apellido', persona.apellido)
        empleado.idHorario = datos.get('idHorario', empleado.idHorario)
        empleado.estado = datos.get('estado', empleado.estado)
        
        db.session.commit()
        return jsonify({'mensaje': 'Empleado actualizado', 'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': str(e), 'status': 'error'}), 400

@bp.route('/admin/horario/crear', methods=['POST'])
def crear_horario():
    datos = request.json
    try:
        nuevo = Horario(
            turno=datos['turno'],
            horario_inicio=datetime.strptime(datos['inicio'], '%H:%M').time(),
            horario_fin=datetime.strptime(datos['fin'], '%H:%M').time(),
            dias=datos.get('dias', '')
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'mensaje': 'Horario creado', 'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': str(e), 'status': 'error'}), 400

@bp.route('/admin/horario/editar/<int:id>', methods=['PUT', 'POST'])
def editar_horario(id):
    datos = request.json
    horario = Horario.query.get_or_404(id)
    try:
        if 'turno' in datos: horario.turno = datos['turno']
        if 'inicio' in datos: horario.horario_inicio = datetime.strptime(datos['inicio'], '%H:%M').time()
        if 'fin' in datos: horario.horario_fin = datetime.strptime(datos['fin'], '%H:%M').time()
        if 'dias' in datos: horario.dias = datos['dias']
        
        db.session.commit()
        return jsonify({'mensaje': 'Horario actualizado', 'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': str(e), 'status': 'error'}), 400
