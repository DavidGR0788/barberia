# 💈 BARBERÍA ELITE - Sistema de Gestión de Citas

## 📊 Estado del Proyecto
**FASE ACTUAL:** ✅ **FASE 2 COMPLETADA** - Sistema de Autenticación  
**PRÓXIMA FASE:** 🚀 **FASE 3** - Gestión de Servicios y Precios

---

## 🛠️ Stack Tecnológico
| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Python** | 3.13 | Backend principal |
| **Flask** | 2.3.3 | Framework web |
| **MySQL** | 8.x | Base de datos |
| **Bootstrap** | 5.1.3 | Frontend y UI |
| **PyMySQL** | 1.1.0 | Conexión MySQL |
| **Flask-Login** | 0.6.3 | Autenticación |
| **bcrypt** | 4.0.1 | Encriptación |
| **python-dotenv** | 1.0.0 | Variables entorno |

---

## 📁 Estructura del Proyecto


---

## 🗃️ Base de Datos - Esquema Implementado
### Tablas Principales:
- **barberias** - Gestión multi-sucursal
- **roles** - administrador, barbero, usuario  
- **usuarios** - Usuarios del sistema (todos los roles)
- **servicios** - Cortes, barba, cejas, etc.
- **citas** - Registro de citas
- **cita_servicios** - Relación muchos a muchos

---

## 🔐 Sistema de Autenticación Implementado

### ✅ Funcionalidades Completadas:
- [x] Login con número de documento
- [x] Registro de nuevos usuarios
- [x] Contraseñas seguras con bcrypt
- [x] Protección de rutas por roles
- [x] Dashboards diferenciados
- [x] Gestión de sesiones

### 👥 Usuarios del Sistema:
| Rol | Documento | Contraseña | Acceso |
|-----|-----------|------------|---------|
| Administrador | 1007230985 | 1234567890 | Control total |
| Barbero | 1001234567 | secret | Gestión citas |
| Cliente | 2001234567 | secret | Agendar citas |

---

## 🚀 URLs de la Aplicación

### 🌐 **Páginas Principales:**
- **Inicio:** http://localhost:5002
- **Login:** http://localhost:5002/login
- **Registro:** http://localhost:5002/register
- **Dashboard:** http://localhost:5002/dashboard

### 🔧 **Diagnóstico:**
- **Health Check:** http://localhost:5002/health
- **Debug Usuarios:** http://localhost:5002/debug/users

---

## 📋 Funcionalidades Implementadas

### ✅ FASE 1 - Configuración Inicial
- [x] Estructura de proyecto Flask
- [x] Configuración MySQL con PyMySQL
- [x] Variables de entorno (.env)
- [x] Servidor en puerto 5002
- [x] Base de datos normalizada
- [x] Datos iniciales de prueba

### ✅ FASE 2 - Sistema de Autenticación  
- [x] Login con documento (no email)
- [x] Registro de usuarios
- [x] Contraseñas hasheadas con bcrypt
- [x] Roles: admin, barbero, usuario
- [x] Protección de rutas
- [x] Dashboards por rol
- [x] Gestión de sesiones

---

## 🎯 Próximos Pasos - FASE 3

### Gestión de Servicios y Precios
- [ ] CRUD completo de servicios
- [ ] Gestión de precios y descripciones  
- [ ] Asignación de servicios por barbería
- [ ] Interfaz administrativa para servicios
- [ ] Cálculo automático de totales

### Estructura a Agregar: