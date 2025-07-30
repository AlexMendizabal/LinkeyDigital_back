# Plan de Migración y Convenciones de Nombres para LinkeyDigital_back

## 1. Plan de Migración a la Nueva Estructura

### a) Preparación

- Haz un backup completo del proyecto y la base de datos.
- Informa al equipo y congela cambios en producción durante la migración.

### b) Reorganización de Carpetas

1. **Crear carpetas principales:**
   - `apps/` para todas las apps Django.
   - `config/` para settings y archivos de configuración global.
   - `common/` para utilidades, permisos, mixins, helpers, i18n.
2. **Mover apps existentes:**
   - Mueve cada app (`authentication`, `profile`, `pay`, etc.) a `apps/`.
   - Actualiza los imports en todo el proyecto para reflejar la nueva ruta (`from apps.profile.models import ...`).
3. **Centralizar settings:**
   - Mueve `settings.py`, `urls.py`, `asgi.py`, `wsgi.py` a `config/`.
   - Divide settings en `base.py`, `dev.py`, `prod.py` si es necesario.
   - Ajusta el `DJANGO_SETTINGS_MODULE` en los scripts y variables de entorno.
4. **Unificar utilidades:**
   - Mueve utilidades compartidas a `common/`.
   - Crea subcarpetas como `common/i18n/` para internacionalización.
5. **Actualizar rutas de archivos estáticos y media:**
   - Asegúrate de que las rutas en settings apunten a las nuevas ubicaciones.
6. **Actualizar scripts y documentación:**
   - Modifica `manage.py` y cualquier script custom para los nuevos paths.
   - Actualiza el README y la documentación interna.

### c) Refactorización de Archivos y Convenciones

- Renombra archivos a plural donde corresponda: `serializers.py`, `services.py`, `tests/`.
- Unifica nombres de modelos, vistas y utilidades siguiendo el patrón `CamelCase` para clases y `snake_case` para funciones/archivos.
- Añade o actualiza `__init__.py` en cada paquete.

### d) Pruebas y Validación

- Ejecuta todas las migraciones y tests.
- Verifica que los endpoints y comandos de gestión funcionen.
- Haz pruebas de integración y validación manual.

### e) Despliegue

- Despliega en entorno de staging antes de producción.
- Informa al equipo cuando la migración esté completa.

---

## 2. Convenciones de Nombres y Estructura

### Carpetas y Archivos

- Apps en `apps/`, utilidades en `common/`, settings en `config/`.
- Archivos en plural: `serializers.py`, `services.py`, `tests/`, `migrations/`.
- Un solo modelo por archivo si es complejo, o todos en `models.py` si son simples.
- Pruebas en carpeta `tests/` dentro de cada app.

### Clases y Funciones

- Clases: `CamelCase` (ej. `UserProfileViewSet`, `PaymentService`).
- Funciones y variables: `snake_case` (ej. `get_user_profile`, `calculate_discount`).
- Constantes: `UPPER_SNAKE_CASE`.

### Internacionalización

- Archivos de traducción en `locale/` y helpers en `common/i18n/`.
- Usa `ugettext_lazy` para textos en modelos y vistas.

### Documentación

- README global y uno por app si es necesario.
- Docstrings en clases, métodos y funciones públicas.

### Otros

- Usa rutas absolutas en imports internos (`from apps.profile.models import ...`).
- Mantén los archivos `__init__.py` en todos los paquetes.
- No dejes archivos vacíos ni código muerto.

---

¿Quieres que genere ejemplos de archivos base para alguna app o módulo específico?
