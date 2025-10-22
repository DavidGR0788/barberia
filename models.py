from flask_login import UserMixin
import pymysql
from config import Config

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
    def get_db_connection():
        return pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    
    @staticmethod
    def get(user_id):
        try:
            conn = User.get_db_connection()
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