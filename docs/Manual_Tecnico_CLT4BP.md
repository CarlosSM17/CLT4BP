# Manual Técnico — CLT4BP
## Plataforma de Diseño Instruccional basada en Teoría de Carga Cognitiva

**Versión:** 1.0
**Fecha:** Febrero 2026
**Estado del Proyecto:** Sprints 1–7 completados

---

## Tabla de Contenidos

1. [Descripción General](#1-descripción-general)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Stack Tecnológico](#3-stack-tecnológico)
4. [Estructura del Proyecto](#4-estructura-del-proyecto)
5. [Instalación y Configuración](#5-instalación-y-configuración)
6. [Base de Datos](#6-base-de-datos)
7. [Backend Laravel — API REST](#7-backend-laravel--api-rest)
8. [Servicio IA Python](#8-servicio-ia-python)
9. [Frontend Vue.js](#9-frontend-vuejs)
10. [Sistema de Autenticación y Roles](#10-sistema-de-autenticación-y-roles)
11. [Módulos Funcionales](#11-módulos-funcionales)
12. [Endpoints de la API](#12-endpoints-de-la-api)
13. [Variables de Entorno](#13-variables-de-entorno)
14. [Flujo de Datos y Procesos Clave](#14-flujo-de-datos-y-procesos-clave)
15. [Efectos CLT Implementados](#15-efectos-clt-implementados)
16. [Tipos de Evaluaciones](#16-tipos-de-evaluaciones)
17. [Generación de Material con IA](#17-generación-de-material-con-ia)
18. [Comandos de Desarrollo](#18-comandos-de-desarrollo)
19. [Pruebas](#19-pruebas)

---

## 1. Descripción General

**CLT4BP** (*Cognitive Load Theory for Best Practice*) es una plataforma educativa inteligente que integra la **Teoría de Carga Cognitiva (TCC/CLT)** y el modelo instruccional **4C/ID (Four-Component Instructional Design)** para generar materiales de aprendizaje personalizados mediante Inteligencia Artificial.

### Propósito

El sistema permite a instructores:
- Crear cursos con objetivos de aprendizaje estructurados
- Aplicar evaluaciones estandarizadas (MSLQ, CLS, CIS, IMMS, Recall, Comprensión)
- Generar perfiles de aprendizaje individuales y grupales automáticamente
- Seleccionar efectos CLT apropiados para el contexto pedagógico
- Generar materiales instruccionales personalizados asistidos por IA (Claude API)
- Recopilar y exportar datos para investigación educativa

A los estudiantes el sistema les permite:
- Acceder a cursos y materiales de aprendizaje personalizados
- Completar evaluaciones de diagnóstico y de rendimiento
- Visualizar su propio progreso y reporte de aprendizaje

### Fundamento Pedagógico

La plataforma aplica los principios de la **Teoría de Carga Cognitiva** (Sweller, 1988) y el modelo **4C/ID** (van Merriënboer, 1997), que estructuran el diseño instruccional en cuatro componentes:
1. **Tareas de Aprendizaje** — Prácticas de habilidades completas
2. **Información de Soporte** — Base conceptual para la transferencia
3. **Información Procedimental** — Instrucciones paso a paso
4. **Práctica Parte-Tarea** — Ejercicios de automatización

---

## 2. Arquitectura del Sistema

```
┌──────────────────────────────────────────────────────────────────┐
│                         CLIENTE (Navegador)                      │
│                    Vue.js 3 SPA + Tailwind CSS                   │
│                         Puerto: 5173 (dev)                       │
└─────────────────────────────┬────────────────────────────────────┘
                              │ HTTP/REST (Axios)
                              │
┌─────────────────────────────▼────────────────────────────────────┐
│                    BACKEND PRINCIPAL (Laravel 12)                 │
│              REST API + Eloquent ORM + Sanctum Auth              │
│                         Puerto: 8000                             │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │  Controllers │  │   Models     │  │      Services          │ │
│  │  (API REST)  │  │  (Eloquent)  │  │  (ProfileGenerator,    │ │
│  └──────────────┘  └──────────────┘  │   MaterialService)     │ │
│                                      └────────────────────────┘ │
└──────┬────────────────────────────────────────────┬─────────────┘
       │                                            │
┌──────▼───────┐                       ┌────────────▼────────────┐
│  PostgreSQL  │                       │  Servicio IA (Python)   │
│  Puerto 5432 │                       │  FastAPI + Claude API   │
│  Base de     │                       │  Puerto: 8001           │
│  Datos       │                       └─────────────────────────┘
└──────────────┘
       │
┌──────▼───────┐
│    Redis     │
│  Puerto 6379 │
│  Cache/Queue │
│  /Session    │
└──────────────┘
```

### Comunicación entre Servicios

- **Frontend → Laravel**: HTTP REST con tokens Sanctum (Bearer Token)
- **Laravel → Python AI**: HTTP interno con token compartido (`X-API-Token` header)
- **Laravel → PostgreSQL**: Conexión PDO directa vía Eloquent ORM
- **Laravel → Redis**: Predis client para caché, colas y sesiones

---

## 3. Stack Tecnológico

### Backend Principal
| Componente | Tecnología | Versión |
|---|---|---|
| Framework | Laravel | 12.0 |
| Lenguaje | PHP | 8.2+ |
| ORM | Eloquent | — |
| Autenticación | Laravel Sanctum | 4.2 |
| Cliente Redis | Predis | 3.3 |
| Base de datos | PostgreSQL | — |
| Caché / Colas | Redis | — |

### Frontend
| Componente | Tecnología | Versión |
|---|---|---|
| Framework | Vue.js | 3.5.27 |
| Estado global | Pinia | 3.0.4 |
| Enrutamiento | Vue Router | 4.6.4 |
| HTTP Client | Axios | 1.13.2 |
| CSS Framework | Tailwind CSS | 3.4.19 |
| Componentes UI | DaisyUI | 4.12.24 |
| Build Tool | Vite | 7.0.7 |

### Servicio IA
| Componente | Tecnología | Versión |
|---|---|---|
| Framework | FastAPI | 0.128.0 |
| Lenguaje | Python | 3.x |
| Servidor ASGI | Uvicorn | 0.40.0 |
| Validación | Pydantic | 2.12.5 |
| SDK Claude | Anthropic | 0.76.0 |
| HTTP Client | HTTPX | 0.28.1 |

### Infraestructura
| Componente | Detalle |
|---|---|
| Base de datos | PostgreSQL (puerto 5432, base: `clt4bp_dev3`) |
| Caché | Redis (puerto 6379) |
| Colas | Redis Queue |
| IA | Claude API (Anthropic) — modelo `claude-sonnet-4-20250514` |

---

## 4. Estructura del Proyecto

```
CLT4BP/
├── backend-laravel/              # Backend principal Laravel
│   ├── app/
│   │   ├── Http/
│   │   │   ├── Controllers/
│   │   │   │   ├── Api/          # Controladores REST
│   │   │   │   │   ├── AuthController.php
│   │   │   │   │   ├── UserController.php
│   │   │   │   │   ├── CourseController.php
│   │   │   │   │   ├── EnrollmentController.php
│   │   │   │   │   ├── AssessmentController.php
│   │   │   │   │   ├── StudentResponseController.php
│   │   │   │   │   ├── ProfileController.php
│   │   │   │   │   ├── TemplateController.php
│   │   │   │   │   ├── GradingController.php
│   │   │   │   │   ├── DataCollectionController.php
│   │   │   │   │   └── ReportController.php
│   │   │   │   ├── CltEffectsController.php
│   │   │   │   └── MaterialController.php
│   │   │   └── Middleware/
│   │   ├── Models/               # Modelos Eloquent
│   │   │   ├── User.php
│   │   │   ├── Course.php
│   │   │   ├── CourseEnrollment.php
│   │   │   ├── Assessment.php
│   │   │   ├── StudentResponse.php
│   │   │   ├── StudentProfile.php
│   │   │   ├── GroupProfile.php
│   │   │   ├── CltEffectsSelection.php
│   │   │   ├── InstructionalMaterial.php
│   │   │   └── MaterialAccessLog.php
│   │   └── Services/             # Servicios de negocio
│   │       ├── StudentProfileGeneratorService.php
│   │       ├── GroupProfileGeneratorService.php
│   │       └── (MaterialService)
│   ├── database/
│   │   ├── migrations/           # 16 migraciones
│   │   └── seeders/              # Plantillas de evaluaciones
│   ├── resources/
│   │   └── js/                   # Frontend Vue.js
│   │       ├── views/            # Vistas por rol
│   │       │   ├── auth/
│   │       │   ├── admin/
│   │       │   ├── instructor/
│   │       │   ├── student/
│   │       │   ├── courses/
│   │       │   └── assessments/
│   │       ├── stores/           # Pinia stores
│   │       ├── services/         # Módulos Axios
│   │       ├── components/       # Componentes Vue
│   │       ├── router/           # Vue Router config
│   │       └── composables/      # Composables Vue
│   ├── routes/
│   │   └── api.php               # Definición de rutas API
│   ├── composer.json
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend-python/               # Servicio IA FastAPI
│   ├── app/
│   │   ├── main.py               # Punto de entrada FastAPI
│   │   ├── config.py             # Configuración Pydantic Settings
│   │   ├── routers/              # Endpoints FastAPI
│   │   │   └── materials.py
│   │   ├── services/             # Lógica de negocio IA
│   │   ├── schemas/              # Esquemas Pydantic
│   │   ├── models/               # Modelos de datos
│   │   ├── core/                 # Utilidades core
│   │   ├── api/                  # Capa API
│   │   └── utils/                # Herramientas auxiliares
│   ├── requirements.txt
│   └── run.py                    # Arranque Uvicorn
│
├── docs/                         # Documentación
├── scripts/                      # Scripts de despliegue
├── Arquitectura_CLT4BP_MVP.pdf
├── Despliegue.pdf
├── iniciarservers.txt
└── Progreso.txt
```

---

## 5. Instalación y Configuración

### Requisitos Previos

| Software | Versión mínima |
|---|---|
| PHP | 8.2+ |
| Composer | 2.x |
| Node.js | 18+ |
| npm | 9+ |
| PostgreSQL | 14+ |
| Redis | 7+ |
| Python | 3.10+ |

### Instalación del Backend Laravel

```bash
cd backend-laravel

# 1. Instalar dependencias PHP
composer install

# 2. Copiar y configurar el entorno
cp .env.example .env
php artisan key:generate

# 3. Configurar la base de datos en .env (ver sección 13)

# 4. Ejecutar migraciones
php artisan migrate

# 5. Poblar plantillas de evaluaciones
php artisan db:seed

# 6. Instalar dependencias Node.js
npm install

# 7. Compilar assets de producción
npm run build
```

### Instalación del Servicio IA Python

```bash
cd backend-python

# 1. Crear entorno virtual
python -m venv venv

# Activar en Windows
.\venv\Scripts\activate

# Activar en Linux/macOS
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
# Crear archivo .env (ver sección 13)
```

### Iniciar Servicios en Desarrollo

```bash
# Terminal 1: Servidor Laravel (API)
cd backend-laravel
php artisan serve
# Disponible en: http://localhost:8000

# Terminal 2: Vite (Hot-reload frontend)
cd backend-laravel
npm run dev
# Disponible en: http://localhost:5173

# Terminal 3: Servicio IA Python
cd backend-python
.\venv\Scripts\activate  # Windows
python run.py
# Disponible en: http://localhost:8001
```

### Setup automatizado (un solo comando)

```bash
cd backend-laravel
composer run setup    # Instala todo y compila assets
composer run dev      # Inicia todos los procesos en paralelo
```

---

## 6. Base de Datos

### Motor y Configuración

- **Motor**: PostgreSQL
- **Puerto**: 5432
- **Base de datos (desarrollo)**: `clt4bp_dev3`
- **Usuario**: `postgres`

### Esquema de Tablas

#### `users`
```sql
id              BIGINT PRIMARY KEY
name            VARCHAR
email           VARCHAR UNIQUE
password        VARCHAR (hashed)
role            ENUM('admin', 'instructor', 'student')
is_active       BOOLEAN DEFAULT true
last_login      TIMESTAMP NULL
email_verified_at TIMESTAMP NULL
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

#### `courses`
```sql
id                  BIGINT PRIMARY KEY
instructor_id       BIGINT FK → users.id
title               VARCHAR
description         TEXT
learning_objectives JSON        -- Array de objetivos
status              ENUM('draft', 'active', 'inactive', 'completed')
start_date          DATE NULL
end_date            DATE NULL
created_at          TIMESTAMP
updated_at          TIMESTAMP
```

#### `course_enrollments`
```sql
id              BIGINT PRIMARY KEY
student_id      BIGINT FK → users.id
course_id       BIGINT FK → courses.id
status          VARCHAR
enrollment_date DATE
completion_date DATE NULL
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

#### `assessments`
```sql
id                      BIGINT PRIMARY KEY
course_id               BIGINT FK → courses.id
assessment_type         ENUM (ver sección 16)
title                   VARCHAR
description             TEXT NULL
questions               JSON        -- Array de preguntas
config                  JSON NULL   -- Configuración adicional
is_active               BOOLEAN DEFAULT false
time_limit              INT NULL    -- Minutos
is_template             BOOLEAN DEFAULT false
requires_manual_grading BOOLEAN DEFAULT false
source_template_id      BIGINT FK → assessments.id NULL
created_at              TIMESTAMP
updated_at              TIMESTAMP
```

#### `student_responses`
```sql
id              BIGINT PRIMARY KEY
assessment_id   BIGINT FK → assessments.id
student_id      BIGINT FK → users.id
responses       JSON        -- Respuestas por pregunta
score           DECIMAL NULL
time_spent      INT NULL    -- Segundos
started_at      TIMESTAMP NULL
completed_at    TIMESTAMP NULL
grading_status  ENUM('auto_graded', 'pending_grading', 'graded')
manual_scores   JSON NULL   -- Puntuaciones manuales
graded_by       BIGINT FK → users.id NULL
graded_at       TIMESTAMP NULL
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

#### `student_profiles`
```sql
id              BIGINT PRIMARY KEY
student_id      BIGINT FK → users.id
course_id       BIGINT FK → courses.id
profile_data    JSON        -- Datos del perfil generado
generated_at    TIMESTAMP
created_at      TIMESTAMP
updated_at      TIMESTAMP
UNIQUE (student_id, course_id)
```

#### `group_profiles`
```sql
id              BIGINT PRIMARY KEY
course_id       BIGINT FK → courses.id
profile_data    JSON        -- Datos del perfil grupal
student_count   INT
generated_at    TIMESTAMP
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

#### `clt_effects_selections`
```sql
id                BIGINT PRIMARY KEY
course_id         BIGINT FK → courses.id
selected_effects  JSON    -- Array de IDs de efectos seleccionados
created_at        TIMESTAMP
updated_at        TIMESTAMP
```

#### `instructional_materials`
```sql
id                BIGINT PRIMARY KEY
course_id         BIGINT FK → courses.id
material_type     VARCHAR     -- learning_tasks | support_info | procedural_info | verbal_protocols | example
target_type       ENUM('individual', 'group')
target_student_id BIGINT FK → users.id NULL  -- Solo para tipo individual
content           JSON        -- Contenido generado por IA
is_active         BOOLEAN DEFAULT false
timer_seconds     INT NULL
activated_at      TIMESTAMP NULL
deactivated_at    TIMESTAMP NULL
created_at        TIMESTAMP
updated_at        TIMESTAMP
```

#### `material_access_logs`
```sql
id                BIGINT PRIMARY KEY
material_id       BIGINT FK → instructional_materials.id
student_id        BIGINT FK → users.id
started_at        TIMESTAMP
completed_at      TIMESTAMP NULL
duration_seconds  INT NULL
created_at        TIMESTAMP
updated_at        TIMESTAMP
```

#### `personal_access_tokens` (Laravel Sanctum)
```sql
id          BIGINT PRIMARY KEY
tokenable_type  VARCHAR
tokenable_id    BIGINT
name        VARCHAR
token       VARCHAR (hashed)
abilities   TEXT NULL
last_used_at    TIMESTAMP NULL
expires_at  TIMESTAMP NULL
created_at  TIMESTAMP
updated_at  TIMESTAMP
```

### Migraciones

Las migraciones se ejecutan en orden cronológico:

| Migración | Tabla | Descripción |
|---|---|---|
| `0001_01_01_000000` | users | Tabla base de usuarios |
| `0001_01_01_000001` | cache | Tabla de caché |
| `0001_01_01_000002` | jobs | Tabla de colas |
| `2026_01_23_004436` | personal_access_tokens | Tokens Sanctum |
| `2026_01_23_004453` | users | Columna role |
| `2026_01_23_171600` | courses | Tabla de cursos |
| `2026_01_23_171800` | course_enrollments | Inscripciones |
| `2026_01_23_215325` | assessments | Evaluaciones |
| `2026_01_23_215326` | student_responses | Respuestas |
| `2026_01_25_033852` | student_profiles | Perfiles individuales |
| `2026_01_25_034126` | group_profiles | Perfiles grupales |
| `2026_01_25_120000` | assessments | Soporte plantillas y calificación |
| `2026_01_25_130000` | assessments | Tipo prior_knowledge |
| `2026_01_26_230627` | clt_effects_selections | Efectos CLT |
| `2026_01_26_231551` | instructional_materials | Materiales IA |
| `2026_02_11_000001` | material_access_logs | Logs de acceso |

---

## 7. Backend Laravel — API REST

### Organización de Controladores

```
app/Http/Controllers/
├── Api/
│   ├── AuthController.php          # Registro, login, logout, perfil
│   ├── UserController.php          # CRUD usuarios, gestión roles
│   ├── CourseController.php        # CRUD cursos
│   ├── EnrollmentController.php    # Inscripciones estudiantes
│   ├── AssessmentController.php    # CRUD evaluaciones
│   ├── StudentResponseController.php # Respuestas estudiantes
│   ├── ProfileController.php       # Perfiles individuales y grupales
│   ├── TemplateController.php      # Plantillas de evaluaciones
│   ├── GradingController.php       # Calificación manual
│   ├── DataCollectionController.php # Recolección de datos e investigación
│   └── ReportController.php        # Reportes instructor/estudiante
├── CltEffectsController.php        # Gestión de efectos CLT
└── MaterialController.php          # Materiales instruccionales IA
```

### Servicios de Negocio

```
app/Services/
├── StudentProfileGeneratorService.php
│   └── Agrega resultados de evaluaciones y genera perfil JSON del estudiante
└── GroupProfileGeneratorService.php
    └── Consolida perfiles individuales en perfil grupal del curso
```

### Middleware de Roles

La aplicación implementa un middleware `role` personalizado que valida que el usuario autenticado tenga el rol requerido:

```php
Route::middleware('role:admin,instructor')->group(...)
Route::middleware('role:student')->group(...)
```

Los tres roles disponibles son:
- **admin**: Acceso completo al sistema
- **instructor**: Gestión de cursos, evaluaciones y materiales
- **student**: Acceso a materiales, evaluaciones propias y reportes personales

---

## 8. Servicio IA Python

### Arquitectura FastAPI

```
backend-python/app/
├── main.py             # App FastAPI + CORS + middleware + routers
├── config.py           # Pydantic Settings (variables de entorno)
├── routers/
│   └── materials.py    # Endpoints de generación de materiales
├── services/           # Lógica de llamada a Claude API
├── schemas/            # Validación de request/response (Pydantic)
├── models/             # Modelos de datos internos
├── core/               # Utilidades y configuración core
└── utils/              # Herramientas auxiliares
```

### Autenticación del Servicio

El servicio Python valida un token compartido con Laravel en cada petición:

```python
async def verify_api_token(x_api_token: str = Header(...)):
    if x_api_token != settings.laravel_api_token:
        raise HTTPException(status_code=401, detail="Token de API inválido")
```

### Configuración Claude API

| Parámetro | Descripción |
|---|---|
| `ANTHROPIC_API_KEY` | Clave de acceso a la API de Anthropic |
| `CLAUDE_MODEL` | `claude-sonnet-4-20250514` (por defecto) |
| `MAX_TOKENS` | Máximo de tokens en la respuesta |
| `TEMPERATURE` | Creatividad de la generación (0.0–1.0) |
| `MAX_RETRIES` | Reintentos ante errores de rate limit |
| `RETRY_DELAY` | Tiempo de espera entre reintentos |
| `TIMEOUT` | Tiempo máximo de espera por respuesta |

### Endpoints del Servicio Python

```
GET  /                          # Estado del servicio
GET  /health                    # Health check
POST /api/v1/materials/generate # Generar material instruccional
POST /api/v1/materials/validate # Validar conexión API
GET  /api/v1/materials/clt-effects # Listar efectos CLT disponibles
```

### Inicio del Servidor

```python
# run.py
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8001,
    reload=True,     # Solo en desarrollo
    log_level="info"
)
```

---

## 9. Frontend Vue.js

### Estructura de Vistas

```
resources/js/
├── App.vue               # Componente raíz
├── app.js                # Punto de entrada + montaje Vue
├── bootstrap.js          # Configuración Axios
├── router/               # Vue Router — rutas protegidas por rol
├── stores/               # Pinia stores (auth, courses, etc.)
├── services/             # Módulos de llamadas API
├── components/           # Componentes reutilizables
├── composables/          # Lógica reactiva reutilizable
├── utils/                # Funciones auxiliares
└── views/
    ├── auth/
    │   ├── LoginView.vue
    │   └── RegisterView.vue
    ├── DashboardView.vue
    ├── ProfileView.vue
    ├── admin/            # Vistas administrador
    ├── instructor/       # Vistas instructor
    ├── student/          # Vistas estudiante
    ├── courses/          # Vistas de cursos
    └── assessments/      # Vistas de evaluaciones
```

### Rutas Principales

| Ruta | Componente | Rol |
|---|---|---|
| `/login` | `LoginView.vue` | Público |
| `/register` | `RegisterView.vue` | Público |
| `/dashboard` | `DashboardView.vue` | Todos |
| `/admin/users` | Admin views | Admin |
| `/instructor/courses` | Instructor views | Instructor |
| `/student/courses` | Student views | Estudiante |

### Gestión de Estado (Pinia)

Los stores de Pinia mantienen el estado reactivo de la aplicación:
- **Auth store**: Token de sesión, datos del usuario, rol activo
- **Course store**: Cursos cargados, inscripciones
- **Assessment store**: Evaluaciones del curso activo
- **Profile store**: Perfiles cargados
- **Material store**: Materiales instruccionales

### Build y Compilación

```bash
# Desarrollo (con hot-reload)
npm run dev

# Producción (optimizado)
npm run build
# Genera: public/build/
```

### Configuración Vite

```js
// vite.config.js
plugins: [
    laravel({ input: ['resources/css/app.css', 'resources/js/app.js'] }),
    vue()
]
// Alias @ → resources/js
```

---

## 10. Sistema de Autenticación y Roles

### Autenticación con Laravel Sanctum

CLT4BP usa **API Token Authentication** de Sanctum (no cookies SPA). El flujo es:

1. Usuario envía `POST /api/login` con email y contraseña
2. Laravel valida credenciales y genera un token personal
3. El token se retorna en la respuesta y el frontend lo almacena
4. Todas las requests posteriores incluyen el header: `Authorization: Bearer {token}`
5. Al cerrar sesión (`POST /api/logout`), el token es revocado

### Roles y Permisos

| Operación | Admin | Instructor | Student |
|---|:---:|:---:|:---:|
| Crear instructor | ✓ | — | — |
| Desactivar usuario | ✓ | — | — |
| Ver lista de usuarios | ✓ | ✓ | — |
| Crear/editar cursos | ✓ | ✓ | — |
| Inscribir estudiantes | ✓ | ✓ | — |
| Crear evaluaciones | ✓ | ✓ | — |
| Calificar manualmente | ✓ | ✓ | — |
| Generar perfiles IA | ✓ | ✓ | — |
| Seleccionar efectos CLT | ✓ | ✓ | — |
| Generar materiales IA | ✓ | ✓ | — |
| Ver reportes instructor | ✓ | ✓ | — |
| Exportar datos CSV | ✓ | ✓ | — |
| Tomar evaluaciones | — | — | ✓ |
| Ver materiales asignados | — | — | ✓ |
| Ver reporte propio | — | — | ✓ |
| Ver mis cursos inscritos | — | — | ✓ |

---

## 11. Módulos Funcionales

### 11.1 Gestión de Usuarios

**Archivo:** `app/Http/Controllers/Api/UserController.php`

Permite al administrador crear cuentas de instructores, listar todos los usuarios y desactivar cuentas. Los instructores pueden ver la lista de usuarios del sistema. Todos los usuarios pueden actualizar su propio perfil.

### 11.2 Gestión de Cursos

**Archivo:** `app/Http/Controllers/Api/CourseController.php`

Los cursos tienen estados de ciclo de vida: `draft → active → inactive / completed`. Cada curso incluye:
- Título y descripción
- Objetivos de aprendizaje (JSON array)
- Fechas de inicio y fin opcionales
- Lista de estudiantes inscritos

### 11.3 Sistema de Evaluaciones

**Archivo:** `app/Http/Controllers/Api/AssessmentController.php`

Las evaluaciones se crean desde cero o a partir de plantillas predefinidas. Soportan:
- **Preguntas de opción múltiple**: Auto-calificadas comparando con `correct_answer`
- **Preguntas abiertas** (text, essay): Requieren calificación manual
- **Escala Likert**: Para cuestionarios psicométricos (MSLQ, CLS, IMMS, CIS)
- **Límite de tiempo**: Timer configurable en minutos

#### Estados de Calificación

```
auto_graded       → Solo preguntas objetivas, calificadas automáticamente
pending_grading   → Contiene preguntas abiertas sin calificar
graded            → Todas las preguntas calificadas (auto + manual)
```

### 11.4 Perfiles de Aprendizaje

**Archivo:** `app/Http/Controllers/Api/ProfileController.php`
**Servicios:** `StudentProfileGeneratorService`, `GroupProfileGeneratorService`

El sistema genera automáticamente perfiles de aprendizaje consultando los resultados de todas las evaluaciones del estudiante en el curso:

**Perfil Individual incluye:**
- Nivel de conocimiento (recall + comprensión)
- Nivel de motivación (MSLQ motivación)
- Estrategias de aprendizaje (MSLQ estrategias)
- Carga cognitiva (CLS)
- Interés en el curso (CIS)
- Motivación hacia los materiales (IMMS)
- Métricas de rendimiento pre/post

**Perfil Grupal incluye:**
- Promedios de todos los indicadores individuales
- Distribución estadística del grupo
- Número de estudiantes considerados
- Recomendaciones para el grupo

### 11.5 Efectos CLT

**Archivo:** `app/Http/Controllers/CltEffectsController.php`

El instructor selecciona hasta 16 efectos CLT para orientar la generación de materiales. Los efectos seleccionados se almacenan por curso y se incorporan al prompt de IA.

### 11.6 Generación de Materiales con IA

**Archivo:** `app/Http/Controllers/MaterialController.php`

El instructor solicita la generación de un material especificando:
- Tipo de material (learning_tasks, support_info, procedural_info, verbal_protocols, example)
- Destino: individual (un estudiante) o grupal (todo el curso)
- Tema específico a desarrollar

El sistema:
1. Recupera el perfil del estudiante o grupo objetivo
2. Obtiene los efectos CLT seleccionados para el curso
3. Envía el request al servicio Python con todos los datos
4. El servicio llama a Claude API con un prompt estructurado
5. El material generado se almacena como `is_active = false` (pendiente de revisión)
6. El instructor revisa y activa el material

### 11.7 Calificación Manual

**Archivo:** `app/Http/Controllers/Api/GradingController.php`

Para evaluaciones con preguntas abiertas (essay, text), el instructor puede:
- Ver la lista de respuestas pendientes de calificación
- Revisar cada respuesta individualmente
- Asignar puntuaciones manuales por pregunta
- Revertir una calificación manual si es necesario
- Recalcular el estado de calificación del curso

### 11.8 Recolección de Datos e Investigación

**Archivo:** `app/Http/Controllers/Api/DataCollectionController.php`

Proporciona herramientas para investigadores y instructores:
- **Resumen del curso**: Estadísticas generales de participación y rendimiento
- **Comparación pre/post**: Contraste de métricas antes y después de la intervención
- **Exportación CSV**: Todos los datos del curso en formato tabular para análisis externo
- **Detalle por estudiante**: Datos completos de un estudiante individual

### 11.9 Reportes

**Archivo:** `app/Http/Controllers/Api/ReportController.php`

- **Reporte del Instructor**: Vista consolidada del rendimiento del curso, estadísticas de evaluaciones y acceso a materiales
- **Reporte del Estudiante**: Progreso personal, puntuaciones por evaluación y materiales accedidos

### 11.10 Logs de Acceso a Materiales

El sistema registra cuando los estudiantes:
- **Inician** el acceso a un material (`POST .../access/start`)
- **Completan** la revisión del material (`POST .../access/complete`)

Esto permite al instructor ver quién ha accedido a cada material y cuánto tiempo dedicó.

---

## 12. Endpoints de la API

**Base URL**: `http://localhost:8000/api`

### Autenticación

| Método | Ruta | Descripción | Roles |
|---|---|---|---|
| POST | `/register` | Registrar usuario | Público |
| POST | `/login` | Iniciar sesión | Público |
| POST | `/logout` | Cerrar sesión | Todos |
| GET | `/me` | Obtener usuario actual | Todos |
| GET | `/health` | Estado del servidor | Público |

### Usuarios

| Método | Ruta | Descripción | Roles |
|---|---|---|---|
| GET | `/users` | Listar usuarios | Admin, Instructor |
| GET | `/users/{id}` | Ver usuario | Todos |
| PUT | `/users/{id}` | Actualizar usuario | Todos |
| POST | `/users/instructors` | Crear instructor | Admin |
| DELETE | `/users/{id}/deactivate` | Desactivar usuario | Admin |

### Cursos

| Método | Ruta | Descripción | Roles |
|---|---|---|---|
| GET | `/courses/{id}` | Ver curso | Todos |
| GET | `/courses` | Listar cursos | Admin, Instructor |
| POST | `/courses` | Crear curso | Admin, Instructor |
| PUT | `/courses/{id}` | Actualizar curso | Admin, Instructor |
| DELETE | `/courses/{id}` | Eliminar curso | Admin, Instructor |
| POST | `/courses/{id}/enroll` | Inscribir estudiante | Admin, Instructor |
| GET | `/courses/{id}/students` | Listar inscritos | Admin, Instructor |
| DELETE | `/courses/{id}/students/{sid}` | Desinscribir estudiante | Admin, Instructor |
| GET | `/my-enrollments` | Mis cursos inscritos | Student |

### Evaluaciones

| Método | Ruta | Descripción | Roles |
|---|---|---|---|
| GET | `/courses/{c}/assessments` | Listar evaluaciones | Todos |
| POST | `/courses/{c}/assessments` | Crear evaluación | Admin, Instructor |
| GET | `/courses/{c}/assessments/{a}` | Ver evaluación | Todos |
| PUT | `/courses/{c}/assessments/{a}` | Actualizar evaluación | Admin, Instructor |
| DELETE | `/courses/{c}/assessments/{a}` | Eliminar evaluación | Admin, Instructor |
| POST | `/courses/{c}/assessments/{a}/toggle` | Activar/desactivar | Admin, Instructor |
| POST | `/courses/{c}/assessments/from-template/{t}` | Crear desde plantilla | Admin, Instructor |
| GET | `/courses/{c}/available-templates` | Plantillas disponibles | Admin, Instructor |
| GET | `/assessment-templates` | Listar plantillas globales | Admin, Instructor |

### Respuestas de Estudiantes

| Método | Ruta | Descripción | Roles |
|---|---|---|---|
| POST | `/courses/{c}/assessments/{a}/start` | Iniciar evaluación | Student |
| POST | `/courses/{c}/assessments/{a}/save` | Guardar respuesta | Student |
| GET | `/courses/{c}/assessments/{a}/my-response` | Ver mi respuesta | Student |
| GET | `/courses/{c}/assessments/{a}/responses` | Ver todas las respuestas | Admin, Instructor |
| GET | `/courses/{c}/my-responses` | Mis respuestas en el curso | Student |

### Perfiles

| Método | Ruta | Descripción | Roles |
|---|---|---|---|
| GET | `/courses/{c}/profiles/students` | Perfiles del curso | Admin, Instructor |
| GET | `/courses/{c}/profiles/students/{sid}` | Perfil de estudiante | Admin, Instructor |
| GET | `/courses/{c}/profiles/group` | Perfil grupal | Admin, Instructor |
| POST | `/courses/{c}/profiles/students/{sid}/generate` | Generar perfil individual | Admin, Instructor |
| POST | `/courses/{c}/profiles/students/generate-all` | Generar todos los perfiles | Admin, Instructor |
| POST | `/courses/{c}/profiles/group/generate` | Generar perfil grupal | Admin, Instructor |
| POST | `/courses/{c}/profiles/regenerate-all` | Regenerar todos | Admin, Instructor |

### Efectos CLT

| Método | Ruta | Descripción | Roles |
|---|---|---|---|
| GET | `/courses/{c}/clt-effects/available` | Efectos disponibles | Todos |
| GET | `/courses/{c}/clt-effects/selection` | Efectos seleccionados | Todos |
| POST | `/courses/{c}/clt-effects/selection` | Guardar selección | Admin, Instructor |
| GET | `/courses/{c}/clt-effects/recommendations` | Recomendaciones | Todos |

### Materiales Instruccionales

| Método | Ruta | Descripción | Roles |
|---|---|---|---|
| POST | `/courses/{c}/materials/generate` | Generar con IA | Admin, Instructor |
| GET | `/courses/{c}/materials` | Listar materiales | Admin, Instructor |
| GET | `/courses/{c}/materials/{m}` | Ver material | Admin, Instructor |
| POST | `/courses/{c}/materials/{m}/toggle-active` | Activar/desactivar | Admin, Instructor |
| PUT | `/courses/{c}/materials/{m}/timer` | Configurar timer | Admin, Instructor |
| GET | `/courses/{c}/materials/{m}/access-logs` | Ver logs de acceso | Admin, Instructor |
| GET | `/courses/{c}/materials/student/list` | Ver mis materiales | Student |
| POST | `/courses/{c}/materials/{m}/access/start` | Registrar inicio acceso | Student |
| POST | `/courses/{c}/materials/{m}/access/complete` | Registrar fin acceso | Student |

### Calificación Manual

| Método | Ruta | Descripción | Roles |
|---|---|---|---|
| GET | `/courses/{c}/pending-grading` | Pendientes del curso | Admin, Instructor |
| POST | `/courses/{c}/recalculate-grading` | Recalcular estados | Admin, Instructor |
| GET | `/courses/{c}/assessments/{a}/pending-grading` | Pendientes por evaluación | Admin, Instructor |
| GET | `/courses/{c}/assessments/{a}/responses/{r}/grading` | Ver para calificar | Admin, Instructor |
| POST | `/courses/{c}/assessments/{a}/responses/{r}/grade` | Enviar calificación | Admin, Instructor |
| POST | `/courses/{c}/assessments/{a}/responses/{r}/revert-grade` | Revertir calificación | Admin, Instructor |

### Reportes y Datos

| Método | Ruta | Descripción | Roles |
|---|---|---|---|
| GET | `/courses/{c}/reports/instructor` | Reporte instructor | Admin, Instructor |
| GET | `/courses/{c}/reports/my-report` | Reporte estudiante | Student |
| GET | `/courses/{c}/data-collection/summary` | Resumen recolección | Admin, Instructor |
| GET | `/courses/{c}/data-collection/pre-post-comparison` | Comparación pre/post | Admin, Instructor |
| GET | `/courses/{c}/data-collection/export` | Exportar CSV | Admin, Instructor |
| GET | `/courses/{c}/data-collection/student/{sid}` | Detalle estudiante | Admin, Instructor |

---

## 13. Variables de Entorno

### Laravel (`backend-laravel/.env`)

```env
# Aplicación
APP_NAME=CLT4BP
APP_ENV=local
APP_KEY=base64:...           # Generado por artisan key:generate
APP_DEBUG=true
APP_URL=http://localhost:8000
APP_LOCALE=en

# Logs
LOG_CHANNEL=stack
LOG_LEVEL=debug

# Base de datos PostgreSQL
DB_CONNECTION=pgsql
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=clt4bp_dev3
DB_USERNAME=postgres
DB_PASSWORD=tu_password

# Redis
REDIS_CLIENT=predis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0

# Cache y Colas
CACHE_DRIVER=redis
QUEUE_CONNECTION=redis
SESSION_DRIVER=redis

# Sanctum
SANCTUM_STATEFUL_DOMAINS=localhost:3000

# Servicio IA Python
AI_SERVICE_URL=http://localhost:8001
AI_SERVICE_TOKEN=tu_token_compartido
AI_SERVICE_TIMEOUT=120

# Claude API (si se usa directamente desde Laravel)
CLAUDE_API_KEY=sk-ant-...
CLAUDE_API_VERSION=2023-06-01
CLAUDE_MODEL=claude-sonnet-4-20250514
```

### Python (`backend-python/.env`)

```env
# Servicio
APP_NAME=CLT4BP-AI-Service
APP_VERSION=1.0.0
DEBUG=true

# Claude API
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=4096
TEMPERATURE=0.7

# Laravel API (para validación de tokens)
LARAVEL_API_URL=http://localhost:8000
LARAVEL_API_TOKEN=tu_token_compartido

# Configuración del servicio
LOG_LEVEL=info
MAX_RETRIES=3
RETRY_DELAY=1.0
TIMEOUT=120
```

---

## 14. Flujo de Datos y Procesos Clave

### 14.1 Ciclo Completo de Aprendizaje

```
1. Instructor crea Curso
         ↓
2. Instructor inscribe Estudiantes
         ↓
3. Instructor crea Evaluaciones (desde plantillas)
   - Pre-test: recall_initial, comprehension_initial
   - Diagnóstico: mslq_motivation_initial, cognitive_load
         ↓
4. Estudiantes toman las Evaluaciones
         ↓
5. Instructor genera Perfiles de Aprendizaje
   (StudentProfileGeneratorService agrega los datos)
         ↓
6. Instructor selecciona Efectos CLT apropiados
         ↓
7. Instructor genera Materiales con IA
   (Claude genera contenido personalizado)
         ↓
8. Instructor revisa y Activa los Materiales
         ↓
9. Estudiantes acceden a los Materiales
         ↓
10. Instructor crea Evaluaciones finales
    - Post-test: recall_final, comprehension_final
    - Cierre: mslq_motivation_final, imms, course_interest
         ↓
11. Instructor exporta Datos para investigación (CSV)
```

### 14.2 Flujo de Generación de Material IA

```
Laravel MaterialController
    └─ Recibe request con: courseId, materialType, targetType,
       targetStudentId (si individual), topic
         ↓
    └─ Obtiene perfil del estudiante/grupo (de student_profiles o group_profiles)
         ↓
    └─ Obtiene efectos CLT seleccionados (de clt_effects_selections)
         ↓
    └─ Construye payload para servicio Python
         ↓
Python FastAPI Service (POST /api/v1/materials/generate)
    └─ Valida X-API-Token
         ↓
    └─ Construye prompt del sistema (principios CLT + 4C/ID)
         ↓
    └─ Llama a Claude API con: system prompt + datos del perfil + efectos CLT
         ↓
    └─ Claude genera el material en formato JSON estructurado
         ↓
    └─ Valida estructura del JSON generado
         ↓
    └─ Retorna material a Laravel
         ↓
Laravel guarda InstructionalMaterial con is_active = false
    └─ Instructor revisa y activa
```

### 14.3 Flujo de Generación de Perfil de Estudiante

```
ProfileController::generateStudentProfile
    └─ Obtiene todas las respuestas del estudiante en el curso
         ↓
StudentProfileGeneratorService
    └─ Extrae datos de: recall_initial + recall_final
    └─ Extrae datos de: comprehension_initial + comprehension_final
    └─ Extrae datos de: cognitive_load (CLS)
    └─ Extrae datos de: mslq_motivation_initial/final
    └─ Extrae datos de: mslq_strategies
    └─ Extrae datos de: course_interest (CIS)
    └─ Extrae datos de: imms
         ↓
    └─ Calcula: knowledge_level = promedio(recall + comprehension scores)
    └─ Calcula: motivation_level = promedio(MSLQ motivation scores)
    └─ Calcula: learning_strategies = promedio(MSLQ strategies scores)
         ↓
    └─ Genera profile_data JSON con todos los indicadores
         ↓
Guarda en student_profiles (upsert por student_id + course_id)
```

---

## 15. Efectos CLT Implementados

La plataforma implementa **16 efectos CLT** organizados en dos categorías:

### Para Conocimiento Nuevo

| ID | Efecto | Descripción |
|---|---|---|
| 1 | Goal-Free Effect | Resolver problemas sin un objetivo específico para reducir la búsqueda de medios-fines |
| 2 | Worked Examples | Presentar ejemplos resueltos antes de que el estudiante intente solo |
| 3 | Completion Problems | Proporcionar soluciones parciales que el estudiante debe completar |
| 4 | Split Attention Management | Integrar fuentes de información separadas para evitar atención dividida |
| 5 | Modality Effect | Combinar información visual y auditiva en lugar de solo visual |
| 6 | Redundancy Elimination | Eliminar información redundante que incrementa innecesariamente la carga |
| 7 | Variability | Variar los ejemplos para facilitar la transferencia del aprendizaje |
| 8 | Isolated Elements | Presentar elementos de forma aislada antes de combinarlos |
| 9 | Element Interactivity | Gestionar la interacción entre elementos de información |

### Para Conocimiento Previo

| ID | Efecto | Descripción |
|---|---|---|
| 10 | Self-Explanation | Pedir al estudiante que explique el material con sus propias palabras |
| 11 | Imagination/Visualization | Pedir al estudiante que visualice conceptos mentalmente |
| 12 | Expertise Reversal | Reducir apoyo a medida que el estudiante adquiere competencia |
| 13 | Guidance-Fading | Retirar gradualmente las guías conforme aumenta el conocimiento |
| 14 | Collective Memory | Aprovechar el conocimiento distribuido del grupo |
| 15 | Self-Management | Permitir al estudiante gestionar su propio aprendizaje |
| 16 | Human Movement | Incorporar demostración de movimientos humanos para tareas procedimentales |
| — | Transient Information Management | Gestionar información transitoria para reducir su efecto de desvanecimiento |

---

## 16. Tipos de Evaluaciones

El sistema soporta los siguientes tipos de evaluaciones estandarizadas:

| Tipo | Nombre Completo | Propósito |
|---|---|---|
| `recall_initial` | Prueba de Recuerdo Inicial | Medir conocimiento previo antes de la instrucción |
| `recall_final` | Prueba de Recuerdo Final | Medir retención después de la instrucción |
| `comprehension_initial` | Prueba de Comprensión Inicial | Medir comprensión conceptual pre-instrucción |
| `comprehension_final` | Prueba de Comprensión Final | Medir comprensión conceptual post-instrucción |
| `cognitive_load` | Escala de Carga Cognitiva (CLS) | Medir la carga cognitiva percibida durante el aprendizaje |
| `mslq_motivation_initial` | MSLQ Motivación Inicial | Medir motivación para aprender (Pintrich et al.) |
| `mslq_motivation_final` | MSLQ Motivación Final | Comparar motivación después de la intervención |
| `mslq_strategies` | MSLQ Estrategias de Aprendizaje | Evaluar estrategias cognitivas y metacognitivas |
| `course_interest` | Escala de Interés en el Curso (CIS) | Medir el interés del estudiante en el curso |
| `imms` | Escala IMMS | Medir motivación hacia los materiales instruccionales (Keller) |

### Tipos de Preguntas Soportados

| Tipo | Calificación | Descripción |
|---|---|---|
| `multiple_choice` | Automática | Opción única con `correct_answer` definida |
| `likert` | Automática | Escala numérica (1–5 o 1–7) |
| `text` | Manual | Respuesta corta de texto abierto |
| `essay` | Manual | Respuesta larga de desarrollo |

---

## 17. Generación de Material con IA

### Tipos de Materiales

| Tipo | Componente 4C/ID | Descripción |
|---|---|---|
| `learning_tasks` | Tareas de Aprendizaje | Actividades prácticas completas y auténticas |
| `support_info` | Información de Soporte | Base conceptual y modelos mentales |
| `procedural_info` | Información Procedimental | Instrucciones paso a paso y reglas |
| `verbal_protocols` | Protocolos Verbales | Ejemplos de razonamiento experto en voz alta |
| `example` | Ejemplo Trabajado | Solución completa de un problema representativo |

### Destino del Material

- **Individual** (`target_type: 'individual'`): Generado específicamente para el perfil de un estudiante
- **Grupal** (`target_type: 'group'`): Generado para el perfil agregado de todo el curso

### Ciclo de Vida del Material

```
generate (is_active = false)
    ↓ Instructor revisa
toggle-active (is_active = true)
    ↓ Estudiante accede
access/start → access/complete
    ↓ Instructor monitorea
access-logs
```

### Integración con Claude API

El prompt enviado a Claude incluye:
1. **Rol y contexto**: Experto en diseño instruccional basado en CLT y 4C/ID
2. **Perfil del aprendiz**: Nivel de conocimiento, motivación, estrategias, carga cognitiva
3. **Objetivos del curso**: Los `learning_objectives` definidos por el instructor
4. **Efectos CLT aplicar**: Lista de efectos seleccionados con sus descripciones
5. **Tipo de material**: Qué componente 4C/ID debe generarse
6. **Tema específico**: El contenido temático a desarrollar
7. **Formato de salida**: JSON estructurado con campos validados

---

## 18. Comandos de Desarrollo

### Laravel (Artisan)

```bash
# Servidor de desarrollo
php artisan serve

# Migraciones
php artisan migrate
php artisan migrate:rollback
php artisan migrate:fresh --seed

# Seeders
php artisan db:seed
php artisan db:seed --class=AssessmentTemplateSeeder

# Caché
php artisan config:clear
php artisan cache:clear
php artisan route:clear
php artisan view:clear

# Colas
php artisan queue:listen --tries=1 --timeout=0
php artisan queue:work

# Tinker (REPL interactivo)
php artisan tinker

# Logs en tiempo real
php artisan pail --timeout=0

# Linting (Laravel Pint)
./vendor/bin/pint
```

### Node.js / Frontend

```bash
# Instalar dependencias
npm install

# Desarrollo con hot-reload
npm run dev

# Build producción
npm run build

# Todos los procesos en paralelo
composer run dev
```

### Python

```bash
# Activar entorno virtual (Windows)
.\venv\Scripts\activate

# Activar entorno virtual (Linux/macOS)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor de desarrollo
python run.py

# Directamente con Uvicorn (sin reload)
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

---

## 19. Pruebas

### Laravel Tests

```bash
# Ejecutar todos los tests
php artisan test

# Con output detallado
php artisan test --verbose

# Test específico
php artisan test --filter NombreDelTest

# Con cobertura de código
php artisan test --coverage
```

La configuración de tests se encuentra en `phpunit.xml`.

### Python Tests

```bash
# Directorio de tests
cd backend-python/tests/

# Ejecutar tests con pytest (si está instalado)
pytest

# Con output detallado
pytest -v
```

---

## Historial de Versiones

| Sprint | Funcionalidades Completadas |
|---|---|
| Sprint 1 | Autenticación, roles, CRUD de cursos, inscripciones |
| Sprint 2 | Sistema de evaluaciones, respuestas de estudiantes, auto-calificación |
| Sprint 3 | Plantillas de evaluaciones, calificación manual |
| Sprint 4 | Perfiles de aprendizaje individuales y grupales con IA |
| Sprint 5 | Efectos CLT, generación de materiales instruccionales con Claude API |
| Sprint 6 | Logs de acceso a materiales, timers, sistema de reportes |
| Sprint 7 | Tests finales (Recall/Comprehension), cuestionarios CS/CIS/IMMS, MSLQ final, recolección de datos y exportación CSV |

---

*Manual Técnico generado automáticamente — CLT4BP v1.0 — Febrero 2026*
