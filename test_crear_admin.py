import pymysql
import bcrypt
from config import Config

def hash_password_bcrypt(password):
    """Hashear contraseña con bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def update_admin_password():
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        cursor = connection.cursor()
        
        # Contraseña que quieres usar
        new_password = '1234567890'
        hashed_password = hash_password_bcrypt(new_password)
        
        print(f"🔑 Actualizando contraseña del admin...")
        print(f"📝 Nueva contraseña: {new_password}")
        print(f"🔐 Hash generado: {hashed_password}")
        
        # Actualizar el usuario admin
        cursor.execute("""
            UPDATE usuarios SET password = %s 
            WHERE num_documento = '1007230985'
        """, (hashed_password,))
        
        connection.commit()
        
        # Verificar que se actualizó
        cursor.execute("SELECT nombre, num_documento FROM usuarios WHERE num_documento = '1007230985'")
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        print(f"✅ Contraseña actualizada exitosamente para: {user['nombre']}")
        print(f"📋 Credenciales:")
        print(f"   Documento: 1007230985")
        print(f"   Contraseña: 1234567890")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    update_admin_password()