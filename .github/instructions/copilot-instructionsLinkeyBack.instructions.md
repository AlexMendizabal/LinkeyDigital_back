### staticfiles

- Carpeta dedicada al almacenamiento de archivos estáticos (CSS, JS, imágenes, etc.) que serán servidos por Django o el servidor web en producción.
- Estructura:
  - `.keep`: Archivo vacío para asegurar que la carpeta se mantenga en el control de versiones, aunque esté vacía.
- Patrones: uso de archivos `.keep` para mantener carpetas vacías en el repositorio; no contiene lógica de negocio ni archivos de código.

### soyyo_api

- Carpeta principal de configuración y ruteo del proyecto Django.
- Estructura y funciones:
  - `settings.py`: Configuración global del proyecto (apps, base de datos, middleware, etc.).
  - `urls.py`: Ruteo global de la API, incluye las rutas de todas las apps principales.
  - `asgi.py`, `wsgi.py`: Entry points para servidores ASGI/WSGI.
  - `management/commands/`: Comandos personalizados de Django.
- Patrones: centralización de configuración y ruteo; uso de comandos de gestión para tareas administrativas; no contiene modelos ni lógica de negocio propia.

### public

- App Django para exponer endpoints públicos de usuarios, contactos, redes sociales, mapas, teléfonos, emails, WhatsApp y reservas.
- Estructura modular:
  - `views/`: Viewsets y endpoints para exponer datos públicos de usuarios, contactos, redes sociales, mapas, teléfonos, emails, WhatsApp y reservas.
  - `services/`: Lógica de negocio para obtener y procesar datos públicos de usuarios, contactos, reservas y redes sociales.
  - `urls.py`: Ruteo de endpoints públicos para usuarios, contactos y reservas.
  - `apps.py`: Configuración de la app Django.
- Patrones: separación clara entre lógica de negocio (servicios) y presentación (vistas); endpoints RESTful organizados para exponer datos públicos de usuarios y recursos asociados; no define modelos propios, solo utiliza servicios y vistas.

### profile

- App Django para la gestión de perfiles de usuario, redes sociales asociadas, imágenes, emails, mapas, teléfonos, reservas y configuraciones de diseño para usuarios.
- Estructura modular:
  - `models/`: Modelos para perfiles, redes sociales, imágenes, emails, mapas, teléfonos, reservas, diseño, etc.
  - `services/`: Lógica de negocio para perfiles, redes sociales, reservas y vistas.
  - `views/`: Viewsets y endpoints para gestión y consulta de todos los recursos de perfil, métricas y configuraciones.
  - `urls.py`: Ruteo de endpoints de perfil, redes sociales, diseño, reservas, métricas, etc.
  - `apps.py`: Configuración de la app Django.
  - `migrations/`: Migraciones de base de datos.
- Patrones: separación clara entre modelos, servicios y vistas; endpoints RESTful organizados para todos los recursos de perfil; modularidad para múltiples tipos de datos asociados a usuarios.

### pay

- App Django para la gestión de pagos, productos, descuentos y transacciones.
- Estructura modular:
  - `models/`: Modelos de base de datos para transacciones, productos, detalles y descuentos.
  - `serializer.py`: Serializadores para transacciones, productos, usuarios y descuentos.
  - `services/`: Lógica de negocio para productos, transacciones y pagos.
  - `views/`: Endpoints API para pagos, consultas, productos, descuentos y webhooks.
  - `urls.py`: Ruteo de todos los endpoints de pago, productos y descuentos.
  - `utilitiesPay.py`: Utilidades y serializadores auxiliares para pagos y transacciones.
  - `admin.py`: Registro de modelos en el admin.
  - `apps.py`: Configuración de la app Django.
  - `migrations/`: Migraciones de base de datos.
- Patrones: separación clara entre modelos, serializadores, servicios y vistas; endpoints RESTful organizados; lógica de negocio en servicios reutilizables; utilidades centralizadas para validación y construcción de DTOs.

### mercado_pago

- App Django para la integración de pagos y notificaciones con Mercado Pago.
- Estructura modular:
  - `views/`: Endpoints API para iniciar pagos (`mercado_pago_viewset.py`) y recibir notificaciones de Mercado Pago (`webhook_mercado_pago_viewset.py`).
  - `services/`: Lógica de negocio para interactuar con la API de Mercado Pago (`mercado_pago.py`).
  - `urls.py`: Ruteo de endpoints de pago y webhook.
  - `apps.py`: Configuración de la app Django.
- Función: Permite iniciar pagos, calcular montos, validar datos y recibir notificaciones de eventos de Mercado Pago para actualizar el estado de las transacciones.
- No define modelos propios.
- Patrones: separación clara entre lógica de negocio (servicios) y endpoints (vistas); integración directa con API externa; endpoints RESTful organizados.

# Copilot Instructions for LinkeyDigital_back

## Estructura y Función de Carpetas Clave

### .idea

- Carpeta generada por PyCharm/JetBrains IDEs.
- Solo contiene configuraciones del entorno de desarrollo (rutas, historial, preferencias, etc.).
- No contiene código ni lógica del proyecto. No modificar ni versionar.

### administration/api

- Expone endpoints RESTful para el modelo `Customer` usando Django REST Framework.
- Incluye un `CustomerViewSet` para CRUD de clientes y un `CustomerSerializer` para serializar todos los campos.
- Patrón: separar lógica de serialización y vistas en archivos distintos.

### administration/models

- `Licencia`: licencia de uso/admin, con relación a usuario admin, plan, fechas, cobro, duración y status. Incluye historial y DTO auxiliar.
- `Subscription`: suscripción, con valor, moneda, vigencia y estado.
- `CustomerType`: tipo de cliente.
- `Devices`: dispositivos asociados a clientes.
- `CustomerSubscription`: relación cliente-suscripción, con estado.
- `CustomerUserDevices`: dispositivos vinculados a usuarios, con estado y nombre.
- `Discount`: códigos de descuento, fechas y tasa.
- `Currencies`: monedas soportadas, símbolos, estado.
- Permite una gestión administrativa flexible y multi-entidad.

- `licencia_service.py`: Métodos para gestionar licencias (crear, obtener, eliminar, actualizar, conectar usuarios, listar usuarios por licencia, etc.). Ejemplo: `get_licencia`, `createLicencia`, `updateLicencia`, `get_Users`.

- Implementa los endpoints de API para la administración de licencias y el bloqueo de usuarios, usando clases tipo `APIView` de Django REST Framework.
- `licencias_viewset.py`: Endpoints para consultar, crear, actualizar y administrar licencias. Incluye serializadores personalizados y lógica de permisos.

### authentication

- App Django para autenticación y gestión de usuarios.
- Estructura modular:
  - `models/`: Modelos de usuario personalizado.
  - `views/`: Vistas y viewsets para endpoints de autenticación y gestión de usuarios.
  - `services/`: Lógica de negocio para autenticación.
  - `form/`: Formularios personalizados para el admin.
  - `secrets/`: Archivos de configuración de Firebase (no versionar).
  - `migrations/`: Migraciones de base de datos.
  - `exceptions.py`: Excepciones personalizadas para autenticación.
  - `authentication.py`: Lógica de autenticación con Firebase.
  - `urls.py`: Ruteo de endpoints de autenticación.
  - `apps.py`: Configuración de la app Django.
  - `admin.py`: Registro de modelos en el admin.
- Patrones: separación clara entre modelos, vistas, servicios y formularios; autenticación externa (Firebase); modularidad para múltiples roles; secretos fuera de control de versiones.

### booking

- App Django para la gestión de reservas (bookings) y configuraciones asociadas.
- Estructura modular:
  - `models/`: Modelos de reservas y configuraciones.
  - `serializer.py`: Serializadores para reservas y configuraciones.
  - `services/`: Lógica de negocio para reservas y configuraciones.
  - `views/`: Viewsets y endpoints para reservas públicas, privadas, configuración y búsqueda.
  - `migrations/`: Migraciones de base de datos.
  - `urls.py`: Ruteo de endpoints de reservas.
  - `apps.py`: Configuración de la app Django.
- Patrones: separación clara entre modelos, serializadores, servicios y vistas; endpoints RESTful organizados; lógica de negocio en servicios.

### client_contact

- App Django para la gestión de contactos de clientes y sus configuraciones.
- Estructura modular:
  - `models/`: Modelos de contacto y configuración.
  - `serializers.py`: Serializadores para contacto y configuración.
  - `views/`: Viewsets y endpoints para gestión y consulta de contactos y configuraciones.
  - `migrations/`: Migraciones de base de datos.
  - `urls.py`: Ruteo de endpoints de contacto.
  - `apps.py`: Configuración de la app Django.
- Patrones: separación clara entre modelos, serializadores y vistas; endpoints RESTful organizados; uso de serializadores para validación y presentación de datos.

### contact

- App Django para la gestión y envío de correos electrónicos desde la plataforma.
- Estructura modular:
  - `html_model_emails.py`: Funciones para generar el contenido HTML de los emails.
  - `services/`: Lógica de negocio para el envío de correos.
  - `views/`: Viewsets y endpoints para el envío de correos y soporte.
  - `urls.py`: Ruteo de endpoints de contacto.
  - `__init__.py`: Inicialización de paquete (importa utilidades de emails).
- Patrones: separación clara entre generación de contenido, lógica de envío y endpoints; uso de plantillas HTML para personalización de correos; endpoints RESTful organizados.

### ecommerce

- App Django para la gestión de botones de e-commerce asociados a usuarios.
- Estructura modular:
  - `models/`: Modelo de botón de e-commerce.
  - `serializers.py`: Serializador para el modelo de botón.
  - `views/`: Viewsets y endpoints para gestión y consulta de botones.
  - `migrations/`: Migraciones de base de datos.
  - `urls.py`: Ruteo de endpoints de e-commerce.
  - `apps.py`: Configuración de la app Django.
- Patrones: separación clara entre modelo, serializador y vistas; endpoints RESTful organizados para la gestión de botones de e-commerce.

### fixture

- Carpeta para datos de carga inicial (fixtures) en formato JSON.
- Permite poblar la base de datos con información base o de prueba.
- Archivos:
  - `base_data.json`: Permisos y datos base para la app `auth` y otras entidades.
  - `design_profile.json`: Perfiles de diseño para la app `profile`.
  - `social_media.json`: Redes sociales para la app `profile`.
- Patrones: uso de fixtures para desarrollo, testing y despliegue inicial; estructura clara por modelo.

### administration

- App Django para la gestión administrativa: clientes, licencias, suscripciones, dispositivos, tipos de cliente, descuentos y monedas.
- Estructura modular:
  - `api/`: Endpoints REST para `Customer`.
  - `models/`: Modelos de base de datos administrativos.
  - `services/`: Lógica de negocio reutilizable (servicios).
  - `views/`: Endpoints API para licencias y bloqueo de usuarios.
  - `migrations/`: Migraciones de base de datos.
  - `UtilitiesAdministration.py`: Utilidades para validación de permisos y licencias.
  - `urls.py`: Ruteo de endpoints administrativos.
  - `apps.py`: Configuración de la app Django.
- Patrones: separación clara entre API, modelos, servicios y vistas; utilidades centralizadas; migraciones versionadas; ruteo explícito.

### media

- Carpeta dedicada al almacenamiento de archivos multimedia y documentos subidos por los usuarios o generados por la plataforma.
- Estructura interna:
  - `custom_social_media/`: Imágenes y recursos gráficos personalizados para redes sociales.
  - `files/`: Documentos PDF, Word, presentaciones, catálogos, currículums, etc. utilizados o generados por usuarios y administradores.
  - `productos_images/`: Imágenes asociadas a productos, perfiles, promociones, etc.
  - `profile/`: Imágenes de perfil de usuario y otros recursos gráficos relacionados con perfiles.
- Función: Centraliza y organiza todos los recursos multimedia y documentos que requieren acceso público o privado desde la plataforma web y móvil.
- No contiene archivos de código ni lógica de negocio.

---

## Resumen Final

Este proyecto Django está organizado de manera modular, siguiendo buenas prácticas de separación de responsabilidades entre modelos, servicios, vistas, serializadores y utilidades. Cada app cumple una función clara y específica, facilitando el mantenimiento y la escalabilidad. La gestión de archivos estáticos y multimedia está centralizada y bien estructurada. El entorno de desarrollo utiliza un único entorno virtual relevante (`venv`), y la documentación de estructura y patrones está actualizada para facilitar la colaboración y la intervención de agentes de IA o desarrolladores.

**Estado:** Documentación y limpieza completadas. Instrucciones listas para uso y referencia.

- App Django para la gestión de botones de e-commerce asociados a usuarios.
