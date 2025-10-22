from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import get_db_connection
from models import User
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT u.id, u.nombre, u.email, u.password, u.telefono, u.rol_id, 
                       u.barberia_id, u.num_documento, u.documento, u.activo
                FROM usuarios u 
                WHERE u.email = %s AND u.activo = TRUE
            """, (email,))
            
            user_data = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if user_data and check_password_hash(user_data['password'], password):
                user = User(
                    id=user_data['id'],
                    nombre=user_data['nombre'],
                    email=user_data['email'],
                    telefono=user_data['telefono'],
                    rol_id=user_data['rol_id'],
                    barberia_id=user_data['barberia_id'],
                    num_documento=user_data['num_documento'],
                    documento=user_data['documento'],
                    activo=user_data['activo']
                )
                
                login_user(user)
                flash(f'¡Bienvenido {user.nombre}!', 'success')
                
                # Redirigir según el rol
                return redirect(url_for('dashboard'))
            
            flash('Email o contraseña incorrectos', 'error')
            
        except Exception as e:
            flash('Error al iniciar sesión', 'error')
            print(f"Error en login: {e}")
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        telefono = request.form['telefono']
        documento = request.form['documento']
        num_documento = request.form['num_documento']
        
        # Validaciones
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return render_template('auth/register.html')
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Verificar si el email ya existe
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('El email ya está registrado', 'error')
                return render_template('auth/register.html')
            
            # Verificar si el documento ya existe
            cursor.execute("SELECT id FROM usuarios WHERE num_documento = %s", (num_documento,))
            if cursor.fetchone():
                flash('El número de documento ya está registrado', 'error')
                return render_template('auth/register.html')
            
            # Crear usuario (rol usuario por defecto = 3)
            hashed_password = generate_password_hash(password)
            cursor.execute("""
                INSERT INTO usuarios (nombre, email, password, telefono, documento, num_documento, rol_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, email, hashed_password, telefono, documento, num_documento, 3))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            flash('¡Registro exitoso! Ahora puedes iniciar sesión', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            flash('Error al registrar usuario', 'error')
            print(f"Error en register: {e}")
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))