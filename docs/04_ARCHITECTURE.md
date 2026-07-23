# Arquitectura Nexus Legal AI

## Filosofía

Toda la lógica de negocio vive en el Dominio.

La interfaz únicamente consume Servicios.

Ningún componente Streamlit ejecuta SQL.

---

# Frontend

- Streamlit

---

# Backend

- Python 3.14

---

# Base de datos

- PostgreSQL
- Supabase

---

# Automatización

- GitHub Actions

---

# Capas

Streamlit

↓

Services

↓

Domain Services

↓

Repositories

↓

PostgreSQL

---

# Motores

- Health Engine
- Priority Engine
- AI Engine
- Notification Engine

---

# Servicios

- AuthService
- SessionService
- DashboardService
- ExecutiveService
- PriorityService
- ProcesoService
- ExpedienteService

---

# Repositories

- BaseRepository
- ProcesoRepository

---

# Modelos

- UserContext
- Proceso
- Prioridad
- Actividad
- Health
- Expediente

---

# Principios

## Single Source of Truth

Toda la información proviene del Dominio.

Nunca desde la UI.

---

## Dependency Flow

Aquí no hablaremos de Streamlit.

Hablaremos de capas.

UI

↓

Components

↓

Services

↓

Repositories

↓

Database

↓

Supabase