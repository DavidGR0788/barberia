from flask import Flask, render_template, jsonify, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import pymysql
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']

# Configuración Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        port=app.config['MYSQL_PORT'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

class User(UserMixin):
    def __init__(self, id, nombre, email, telefono, rol_id, barberia_id, num_documento, documento, activo):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.rol_id = rol_id
        self.barberia_id = barberia_id
        self.num_documento = num_documento
        self.documento = documento
        self.activo = activo
    
    def get_id(self):
        return str(self.id)
    
    @staticmethod
    def get(user_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.nombre, u.email, u.telefono, u.rol_id, u.barberia_id, 
                       u.num_documento, u.documento, u.activo
                FROM usuarios u 
                WHERE u.id = %s AND u.activo = TRUE
            """, (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user_data:
                return User(
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
            return None
        except Exception as e:
            print(f"Error en User.get: {e}")
            return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        num_documento = request.form['num_documento']
        password = request.form['password']
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT u.id, u.nombre, u.email, u.password, u.telefono, u.rol_id, 
                       u.barberia_id, u.num_documento, u.documento, u.activo
                FROM usuarios u 
                WHERE u.num_documento = %s AND u.activo = TRUE
            """, (num_documento,))
            
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
                return redirect(url_for('dashboard'))
            
            flash('Número de documento o contraseña incorrectos', 'error')
            
        except Exception as e:
            flash('Error al iniciar sesión', 'error')
            print(f"Error en login: {e}")
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('login'))
            
        except Exception as e:
            flash('Error al registrar usuario', 'error')
            print(f"Error en register: {e}")
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Redirigir según el rol
    if current_user.rol_id == 1:  # Admin
        return render_template('dashboard/admin_dashboard.html')
    elif current_user.rol_id == 2:  # Barbero
        return render_template('dashboard/barbero_dashboard.html')
    else:  # Usuario
        return render_template('dashboard/usuario_dashboard.html')

@app.route('/health')
def health_check():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        tables = ['barberias', 'roles', 'usuarios', 'servicios', 'citas', 'cita_servicios']
        counts = {}
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            result = cursor.fetchone()
            counts[table] = result['count']
        
        cursor.close()
        connection.close()
        
        return {
            'status': '✅ SISTEMA OPERATIVO',
            'database': '✅ CONECTADO',
            'tablas': counts,
            'puerto': 5002,
            'mensaje': 'Barbería Elite - Sistema de Citas'
        }
        
    except Exception as e:
        return {
            'status': '❌ ERROR',
            'database': f'❌ {str(e)}',
            'puerto': 5002,
            'mensaje': 'Revisar configuración de MySQL'
        }

if __name__ == '__main__':
    print("🚀 Iniciando Barbería Elite...")
    print("📍 http://localhost:5002")
    print("🔐 http://localhost:5002/login")
    print("👤 http://localhost:5002/register")
    print("📊 http://localhost:5002/health")
    app.run(debug=True, host='0.0.0.0', port=5002)