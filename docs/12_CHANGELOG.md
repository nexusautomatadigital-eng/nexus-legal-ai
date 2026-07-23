# Changelog

## Sprint 1.0
- Se creó ROADMAP_V1.md
- Se creó ARCHITECTURE_V1.md
- Se implementó UserContext
- Se implementó SessionService
## Sprint 1.1
- Se implementó AuthService (estructura)
# Sprint 1.2 - Nexus Core Foundation
Fecha: 16-07-2026
## Objetivo
Iniciar la construcción del núcleo arquitectónico de Nexus Legal AI para desacoplar la lógica de negocio de la interfaz Streamlit y preparar la plataforma para una arquitectura SaaS escalable y multi-tenant.
---
## Implementaciones
### Core
- Se creó `core/context.py`.
- Se implementó la clase `UserContext`.
- Se centralizó la información del usuario autenticado en un único objeto.
### Session
- Se creó `core/session.py`.
- Se implementó `SessionService`.
- Se encapsuló el uso de `st.session_state`.
### Authentication
- Se creó `domain/auth_service.py`.
- Se definió la estructura inicial de `AuthService`.
- Se preparó la arquitectura para desacoplar completamente el login del Dashboard.
### Application Controller
- Se creó `core/app_controller.py`.
- Se implementó el controlador principal de la aplicación.
- Se centralizó el acceso al contexto del usuario.
### Repositories
Se creó la estructura inicial de repositorios:
- ClienteRepository
- ProcesoRepository
- PriorityRepository
- DashboardRepository
---
## Arquitectura
Se definió oficialmente la arquitectura en capas:
UI (Streamlit)
↓
Core
↓
Services
↓
Repositories
↓
Supabase
---
## Beneficios
- Eliminación progresiva del acceso directo a la base de datos desde la interfaz.
- Preparación para arquitectura Multi-Tenant.
- Base preparada para soportar miles de clientes.
- Desacoplamiento entre interfaz y lógica de negocio.
- Mayor mantenibilidad y escalabilidad.
---
## Estado
Sprint completado correctamente.
Pruebas:
- Sin errores de estructura.
- Arquitectura preparada para iniciar la migración del Dashboard V1 hacia el nuevo Centro de Operaciones Jurídicas.
Estado del Proyecto:
Nexus Legal AI V1 continúa según ROADMAP_V1.
# Sprint 2.2 - Base Repository

Fecha: 16-07-2026

## Objetivo

Crear una clase base para centralizar la conexión a la base de datos y evitar duplicación de código en todos los repositorios.

---

## Implementaciones

### Repository Layer

- Se creó `BaseRepository`.
- Se centralizó la conexión mediante herencia.
- `ClienteRepository` ahora hereda de `BaseRepository`.
- Se elimina la necesidad de repetir `get_connection()` en cada repositorio.

---

## Decisiones de Arquitectura

- Todos los repositorios deberán heredar de `BaseRepository`.
- Ningún repositorio abrirá conexiones manualmente.
- Se establece un punto único para gestionar la conexión a Supabase.

---

## Beneficios

- Menor duplicación de código.
- Mayor mantenibilidad.
- Arquitectura consistente para todos los repositorios.
- Base preparada para incorporar nuevos repositorios (Procesos, Dashboard, Prioridades, Alertas).

Estado: ✅ Sprint completado.
# Sprint 3.0 - ProcesoRepository

Fecha: 16-07-2026

## Objetivo

Iniciar la construcción del primer repositorio funcional encargado de acceder a la información de procesos judiciales.

---

## Implementaciones

- Se creó la estructura de `ProcesoRepository`.
- Se agregó el método `get_by_cliente(cliente_id)`.
- Se definió oficialmente `procesos_v2` como la tabla principal del sistema.

---

## Decisiones de Arquitectura

- Toda nueva funcionalidad utilizará exclusivamente las tablas V2.
- Las tablas de la versión anterior pasan a estado Legacy.
- Los repositorios devolverán objetos del dominio en lugar de DataFrames.

---

## Beneficios

- Preparación para eliminar la dependencia de Pandas en la capa de presentación.
- Base para la migración del Dashboard al nuevo Centro de Operaciones Jurídicas.
- Arquitectura preparada para un modelo SaaS multi-tenant.

Estado: ✅ Sprint completado.

# Sprint 4 - Primer Repository Funcional

## Objetivo

Implementar el primer acceso real a la base de datos utilizando la nueva arquitectura Repository.

---

## Implementaciones

- Se implementó `ProcesoRepository.get_by_cliente(cliente_id)`.
- Se migró la primera consulta SQL desde la arquitectura anterior hacia la nueva capa Repository.
- Se implementó el primer test unitario para Repository.

---

## Decisiones de Arquitectura

- Repository será la única capa autorizada para consultar la base de datos.
- Los Services dejarán de ejecutar SQL directamente.
- Se inicia oficialmente la migración del Dashboard Legacy hacia Nexus Core.

---

## Beneficios

- Primer paso para eliminar SQL del Dashboard.
- Preparación para desacoplar completamente la interfaz.
- Base para construir el Centro de Operaciones Jurídicas.

Estado: ✅ Sprint completado.

# Sprint 4 - Primer Repository Funcional

Fecha: 16-07-2026

## Objetivo

Implementar el primer acceso real a la base de datos mediante la nueva arquitectura Repository.

---

## Implementaciones

- Se implementó `ProcesoRepository.get_by_cliente(cliente_id)`.
- Se migró la primera consulta SQL desde la arquitectura Legacy.
- Se creó el primer test unitario para Repository.
- Se validó el filtrado por `cliente_id`.

---

## Resultado de Pruebas

Cliente 83:

- Total procesos: 1
- Consulta ejecutada correctamente.
- Se confirmó el aislamiento de datos entre clientes.

---

## Decisiones de Arquitectura

- Repository será la única capa autorizada para acceder a `procesos_v2`.
- El siguiente paso será reemplazar las tuplas por objetos del dominio (`Proceso`).

---

Estado: ✅ Sprint aprobado.

# Sprint 5 - Migración de ProcesoService

Objetivo:

Separar completamente la lógica de negocio del acceso a datos.

Se iniciará la migración de ProcesoService para consumir ProcesoRepository y delegar el cálculo del Health Score al HealthEngine.

# Sprint 5.1 - Desacoplamiento de ProcesoService

Fecha: 16-07-2026

## Objetivo

Separar la lógica de acceso a datos de la lógica de negocio.

---

## Implementaciones

- `ProcesoService` deja de abrir conexiones a la base de datos.
- Se incorpora `ProcesoRepository` como única fuente de datos.
- El método `get_procesos()` ahora recibe `cliente_id`.
- La construcción de `Actividad`, `Health` y `Proceso` permanece en la capa de servicio.

---

## Decisiones de Arquitectura

- El acceso a Supabase queda centralizado en los repositorios.
- Los servicios solo coordinan lógica de negocio y composición de modelos.
- Se refuerza el aislamiento de datos por cliente (multi-tenant).

---

## Beneficios

- Menor acoplamiento entre lógica de negocio y persistencia.
- Mayor facilidad para probar los servicios con repositorios simulados (mocks).
- Base preparada para sustituir el origen de datos sin modificar la lógica del negocio.

Estado: ✅ Sprint completado.

# Sprint 6 - ClienteRepository Funcional

Fecha: 16-07-2026

## Objetivo

Implementar el acceso centralizado a la información del cliente autenticado.

---

## Implementaciones

- Se implementó `ClienteRepository.get_by_usuario(usuario)`.
- Se agregó el primer test del repositorio de clientes.
- Se centralizó el acceso a la información del cliente en la capa Repository.

---

## Decisiones de Arquitectura

- AuthService consumirá ClienteRepository para recuperar la información del usuario autenticado.
- Se evita que el login consulte directamente la base de datos.

---

## Beneficios

- Menor acoplamiento entre autenticación y persistencia.
- Base preparada para incorporar roles, permisos y nuevos tipos de usuarios.
- Continúa la migración hacia una arquitectura limpia y desacoplada.

Estado: ✅ Sprint completado.

# Sprint 7 - Inicio de migración de AuthService

Fecha: 16-07-2026

## Objetivo

Desacoplar la autenticación del acceso directo a la base de datos.

---

## Implementaciones

- AuthService ahora utiliza ClienteRepository.
- Se creó el primer flujo de autenticación basado en la nueva arquitectura.
- Se añadió un test independiente para AuthService.

---

## Decisiones de Arquitectura

- AuthService será la única puerta de entrada para la autenticación.
- ClienteRepository será la única capa autorizada para consultar la información del cliente durante el login.

---

## Beneficios

- Separación clara entre autenticación y persistencia.
- Base preparada para incorporar validación de contraseñas, sesiones y roles.
- Continúa la eliminación de lógica del Dashboard heredado.

Estado: ✅ Sprint completado.

# Sprint 8 - Cliente como Modelo de Dominio

Fecha: 16-07-2026

## Objetivo

Eliminar el uso de tuplas en la autenticación y trabajar con objetos de dominio.

---

## Implementaciones

- Se creó el modelo `Cliente`.
- `ClienteRepository` ahora devuelve instancias de `Cliente`.
- `AuthService` continúa funcionando sin cambios gracias al desacoplamiento entre capas.

---

## Decisiones de Arquitectura

- Los repositorios devolverán modelos del dominio en lugar de estructuras anónimas.
- Los servicios no dependerán de la representación interna de los datos.

---

## Beneficios

- Mayor legibilidad.
- Menor acoplamiento.
- Preparación para incorporar roles, permisos y datos adicionales del cliente sin afectar al resto del sistema.

Estado: ✅ Sprint completado.

# Sprint 8 - Cliente como Modelo de Dominio

Fecha: 17-07-2026

## Objetivo

Migrar la autenticación para utilizar objetos del dominio en lugar de tuplas.

---

## Implementaciones

- Se creó el modelo `Cliente`.
- `ClienteRepository` devuelve instancias de `Cliente`.
- `AuthService` continúa funcionando sin modificaciones gracias al desacoplamiento entre capas.
- Se validó el flujo completo de autenticación con pruebas.

---

## Resultado de Pruebas

- Login exitoso.
- Se obtiene un objeto `Cliente`.
- Acceso a propiedades mediante atributos (`cliente.nombre`, `cliente.email`, `cliente.plan`).

---

## Decisiones de Arquitectura

- Los repositorios devolverán exclusivamente modelos del dominio.
- Los servicios serán independientes de la representación física de los datos.

Estado: ✅ Sprint completado.

# Sprint 9.1 - Primer paso de la migración del Dashboard

Fecha: 17-07-2026

## Objetivo

Eliminar la primera consulta SQL directa del Dashboard sin modificar la interfaz.

---

## Implementaciones

- Se añadió `ProcesoService.get_procesos_dataframe(cliente_id)`.
- El Dashboard dejará de consultar la base de datos directamente.
- Se introduce un adaptador temporal entre los modelos del dominio y Pandas.

---

## Decisiones de Arquitectura

- Toda consulta a procesos pasa por `ProcesoService`.
- Pandas permanecerá únicamente como capa de compatibilidad durante la migración.
- El SQL desaparece progresivamente del Dashboard.

---

Estado: ✅ Sprint completado.

# Sprint 9.2 - Primera migración del Dashboard

Fecha: 17-07-2026

## Objetivo

Eliminar la primera consulta SQL directa del Dashboard.

---

## Implementaciones

- Se agregó `get_procesos_dataframe()` en `ProcesoService`.
- El Dashboard obtiene los procesos mediante `ProcesoService`.
- Se elimina la dependencia directa de `pd.read_sql()` para la carga inicial de procesos.

---

## Decisiones de Arquitectura

- Toda consulta de procesos debe pasar por `ProcesoService`.
- El Dashboard deja de acceder directamente a la base de datos para este caso de uso.

---

## Beneficios

- Primer bloque SQL eliminado del Dashboard.
- Inicio de la migración funcional hacia una arquitectura por capas.
- Se mantiene compatibilidad temporal con Pandas durante la transición.

Estado: ✅ Sprint completado.

# Changelog

## Sprint 11.1

### Added
- Nuevo modelo Proceso basado en procesos_v2.

### Changed
- Se elimina dependencia de Health y Actividad del modelo.

### Notes
- El modelo ahora representa exactamente la estructura persistente de la BD.

Sprint 11.3

Changed

ProcesoService reconstruido para la arquitectura V2.
Eliminadas las dependencias de HealthEngine y Actividad.
Eliminada la lógica basada en índices de tuplas (row[n]).

Architecture

El flujo queda establecido como:
Dashboard → ProcesoService → ProcesoRepository → procesos_v2

Sprint 11.4 (Inicio)

Objetivo

Migrar la sesión del usuario para utilizar cliente_id como identificador principal.

Motivo

El repositorio ya trabaja con procesos_v2.
procesos_v2 está relacionado con clientes mediante cliente_id.
El Dashboard debe dejar de depender del nombre del cliente para realizar consultas.

Sprint 11.4
Fixed
El Dashboard deja de utilizar st.session_state.nombre como identificador para las consultas.
Las consultas pasan a utilizar st.session_state.cliente_id, alineándose con la relación clientes.id → procesos_v2.cliente_id.
Architecture
La autenticación no requirió cambios porque ya almacenaba correctamente el cliente_id.
El cambio se realizó únicamente en la capa de presentación.
Sprint 12.1

Objetivo

Crear la estructura de paquetes de la arquitectura V2 sin modificar el comportamiento del sistema.

Resultado esperado

Nuevos paquetes (services, dto) preparados.
Sin cambios en los imports existentes.
Riesgo de regresión prácticamente nulo.

# Sprint 13.1
## Fecha
2026-06-14

### Nuevo

- Se crea Executive Brief como nueva cabecera del Command Center.
- ExecutiveService incorpora el método get_executive_brief().
- Se unifica la información ejecutiva para el Dashboard.
- Se personaliza el saludo del abogado.
- Se agrega resumen ejecutivo del despacho.

### Mejoras

- Se desacopla parcialmente la construcción del Dashboard.
- Se prepara la integración con Priority Card.
- Se prepara la evolución hacia Command Center.

### Impacto

El abogado recibe un resumen ejecutivo inmediatamente después del login en lugar de únicamente KPIs.

## Sprint 13.1 - Executive Brief

### Nuevas funcionalidades
- Se implementa ExecutiveService.get_executive_brief().
- Se crea el componente Executive Brief.
- Se integra el resumen ejecutivo en el Command Center.

### Arquitectura
- ExecutiveService ahora utiliza PriorityService.
- PriorityService recibe cliente_id.
- Se inicializa correctamente PriorityEngine.

### Calidad
- Se crea test_executive_service.py.
- Primera prueba unitaria del ExecutiveService superada.
# Changelog

Todas las modificaciones importantes del proyecto serán registradas aquí.

---

# v0.13.0
Fecha: 19 Julio 2026

## Sprint 13 - Estabilización del Dominio y Executive Dashboard

### Arquitectura

- Se consolidó la arquitectura basada en Servicios + Repositories.
- El Dashboard dejó de depender de consultas SQL directas.
- Se incorporó SessionService como punto único de acceso al contexto del usuario.
- Se implementó bootstrap_dev_session() para desarrollo local.

### Dominio

Se estabilizaron los siguientes servicios:

- ExecutiveService
- PriorityService
- ProcesoService

Se adaptó PriorityEngine al nuevo modelo Proceso V2.

Se eliminaron las dependencias al modelo antiguo:

- proceso.actividad
- proceso.numero
- proceso.cliente

Ahora el motor utiliza exclusivamente el modelo Proceso actual.

### Testing

Se agregaron pruebas para ExecutiveService.

Resultado:

PASS
tests/test_executive_service.py

### Dashboard

Se integró Executive Brief.

Se implementaron:

- KPIs
- Executive Summary
- Priority Card
- Recent Events

El Dashboard quedó completamente funcional utilizando la arquitectura del dominio.

### Estado

Sprint 13 finalizado.

El proyecto entra en la etapa de UX del Command Center.