# Manual de Usuario — CLT4BP

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Acceso al Sistema](#2-acceso-al-sistema)
3. [Roles de Usuario](#3-roles-de-usuario)
4. [Módulo de Cursos](#4-módulo-de-cursos)
5. [Módulo de Evaluaciones](#5-módulo-de-evaluaciones)
6. [Perfiles de Aprendizaje](#6-perfiles-de-aprendizaje)
7. [Efectos CLT](#7-efectos-clt)
8. [Generación de Materiales con IA](#8-generación-de-materiales-con-ia)
9. [Calificación](#9-calificación)
10. [Reportes y Análisis de Datos](#10-reportes-y-análisis-de-datos)
11. [Vista del Estudiante](#11-vista-del-estudiante)
12. [Administración del Sistema](#12-administración-del-sistema)
13. [Glosario](#13-glosario)

---

## 1. Introducción

**CLT4BP** (*Cognitive Load Theory for Best Practice*) es una plataforma educativa inteligente que combina la **Teoría de Carga Cognitiva (CLT)** con el modelo de diseño instruccional **4C/ID** (Four-Component Instructional Design) para generar materiales de aprendizaje personalizados asistidos por inteligencia artificial.

### ¿Qué hace el sistema?

El sistema permite a los instructores:

- Crear y gestionar cursos con objetivos de aprendizaje estructurados.
- Aplicar evaluaciones estandarizadas para medir la carga cognitiva, motivación y estrategias de aprendizaje de los estudiantes.
- Generar perfiles de aprendizaje individuales y grupales automáticamente.
- Seleccionar efectos CLT apropiados para el contexto del curso.
- Generar materiales instruccionales optimizados cognitivamente con ayuda de IA (Claude de Anthropic).
- Calificar respuestas y obtener reportes de desempeño.

A los estudiantes les permite:

- Acceder a cursos y materiales personalizados.
- Completar evaluaciones formativas y sumativas.
- Visualizar su progreso y perfil de aprendizaje.

---

## 2. Acceso al Sistema

### 2.1 Ingreso (Login)

1. Abra su navegador y acceda a la URL del sistema.
2. Ingrese su **correo electrónico** y **contraseña**.
3. Haga clic en **Iniciar Sesión**.

El sistema redirige automáticamente al panel principal según su rol (Administrador, Instructor o Estudiante).

### 2.2 Cierre de Sesión (Logout)

Haga clic en su nombre de usuario en la esquina superior derecha y seleccione **Cerrar Sesión**.

### 2.3 Recuperación de Cuenta

Si no recuerda su contraseña, contacte al administrador del sistema para que restablezca sus credenciales.

---

## 3. Roles de Usuario

| Rol | Descripción |
|-----|-------------|
| **Administrador** | Gestiona usuarios, tiene acceso completo al sistema y puede generar reportes globales. |
| **Instructor** | Crea y gestiona cursos, evalúa estudiantes, genera materiales con IA y consulta reportes. |
| **Estudiante** | Accede a cursos inscritos, completa evaluaciones y consulta sus materiales y progreso. |

---

## 4. Módulo de Cursos

> Disponible para: **Administrador**, **Instructor**

### 4.1 Crear un Curso

1. En el menú lateral, seleccione **Cursos** → **Nuevo Curso**.
2. Complete los campos del formulario:
   - **Título:** Nombre del curso.
   - **Descripción:** Resumen del contenido.
   - **Objetivos de Aprendizaje:** Liste los objetivos que el curso busca alcanzar.
   - **Fecha de inicio y fin** (opcionales).
3. Haga clic en **Guardar**.

El curso se crea en estado **Borrador**. Puede activarlo cuando esté listo para los estudiantes.

### 4.2 Estados de un Curso

| Estado | Descripción |
|--------|-------------|
| `draft` | Borrador, no visible para estudiantes. |
| `active` | Activo y accesible para estudiantes inscritos. |
| `inactive` | Temporalmente desactivado. |
| `completed` | Curso finalizado. |

### 4.3 Editar o Eliminar un Curso

- En la lista de cursos, haga clic en el ícono de **edición** (lápiz) junto al curso.
- Para eliminar, haga clic en el ícono de **eliminar** (papelera). Esta acción es irreversible.

### 4.4 Inscribir Estudiantes

1. Abra el curso deseado.
2. Vaya a la pestaña **Estudiantes**.
3. Haga clic en **Inscribir Estudiante**.
4. Busque al estudiante por nombre o correo y confirme la inscripción.

Para **desinscribir** a un estudiante, haga clic en el botón de eliminar junto a su nombre en la lista.

---

## 5. Módulo de Evaluaciones

> Disponible para: **Instructor** (creación/gestión), **Estudiante** (completar)

### 5.1 Tipos de Evaluación Disponibles

| Tipo | Descripción |
|------|-------------|
| **Recall** | Preguntas de recuerdo y comprensión del contenido. |
| **Comprehension** | Evaluación de comprensión conceptual. |
| **MSLQ** | Motivated Strategies for Learning Questionnaire — mide motivación y estrategias de aprendizaje. |
| **CLS** | Cognitive Load Scale — mide la carga cognitiva percibida. |
| **CIS** | Course Interest Scale — mide el interés en el curso. |
| **IMMS** | Instructional Materials Motivation Scale — evalúa la motivación hacia los materiales. |

### 5.2 Crear una Evaluación desde Plantilla

1. Dentro del curso, vaya a la pestaña **Evaluaciones**.
2. Haga clic en **Nueva Evaluación** → **Desde Plantilla**.
3. Seleccione el tipo de plantilla (MSLQ, CLS, etc.).
4. La evaluación se crea con las preguntas estandarizadas predefinidas.
5. Configure opciones adicionales si es necesario (tiempo límite, instrucciones).

### 5.3 Crear una Evaluación Personalizada

1. Seleccione **Nueva Evaluación** → **Personalizada**.
2. Defina el título e instrucciones.
3. Agregue preguntas de los siguientes tipos:
   - **Opción múltiple**
   - **Texto libre**
   - **Escala Likert**
   - **Escala numérica**
4. Guarde la evaluación.

### 5.4 Activar / Desactivar una Evaluación

Las evaluaciones se crean en estado **inactivo** por defecto. Para que los estudiantes puedan completarla:

1. Localice la evaluación en la lista.
2. Haga clic en el botón **Activar**.

Para cerrar la evaluación, haga clic nuevamente en **Desactivar**.

### 5.5 Ver Respuestas de Estudiantes

1. Abra la evaluación.
2. Vaya a la pestaña **Respuestas**.
3. Visualice la lista de estudiantes con su estado (pendiente, auto-calificado, calificado).

---

## 6. Perfiles de Aprendizaje

> Disponible para: **Instructor**

Los perfiles de aprendizaje se generan automáticamente a partir de las respuestas de los estudiantes a las evaluaciones estandarizadas (MSLQ, CLS, CIS, IMMS).

### 6.1 Generar Perfil Individual

1. Dentro del curso, vaya a **Perfiles** → **Estudiantes**.
2. Seleccione al estudiante.
3. Haga clic en **Generar Perfil**.

El sistema analiza las respuestas y crea un perfil con dimensiones como:
- **Motivación intrínseca / extrínseca**
- **Estrategias de aprendizaje** (organización, elaboración, repetición)
- **Carga cognitiva percibida** (intrínseca, extrínseca, germana)
- **Autoeficacia**
- **Interés en el curso y los materiales**

### 6.2 Generar Perfiles en Masa

1. Vaya a **Perfiles** → **Generar Todos**.
2. El sistema procesa todos los estudiantes con respuestas disponibles.

### 6.3 Perfil Grupal

1. Vaya a **Perfiles** → **Grupo**.
2. Haga clic en **Generar Perfil Grupal**.

El perfil grupal agrega las métricas de todos los estudiantes del curso y sirve como base para la generación de materiales.

---

## 7. Efectos CLT

> Disponible para: **Instructor**

Los **Efectos CLT** son estrategias instruccionales derivadas de la Teoría de Carga Cognitiva. La selección correcta de estos efectos determina cómo se generarán los materiales de aprendizaje.

### 7.1 Ver Efectos Disponibles

1. Dentro del curso, vaya a **Efectos CLT**.
2. El sistema muestra los efectos organizados en dos categorías:
   - **Para conocimiento nuevo** (ej. efecto de ejemplo resuelto, efecto de redundancia reducida)
   - **Para conocimiento previo** (ej. efecto de expertise reverso, efecto de atención dividida)

### 7.2 Seleccionar Efectos para el Curso

1. Marque los efectos que desea aplicar.
2. El sistema puede ofrecer **recomendaciones** basadas en el perfil grupal de los estudiantes.
3. Haga clic en **Guardar Selección**.

La selección queda guardada y se usará en la siguiente generación de materiales.

---

## 8. Generación de Materiales con IA

> Disponible para: **Instructor**

Esta es la funcionalidad central del sistema. Los materiales se generan utilizando el modelo de IA **Claude (Anthropic)** y están optimizados según la Teoría de Carga Cognitiva y el modelo 4C/ID.

### 8.1 Tipos de Materiales (Modelo 4C/ID)

| Tipo | Descripción |
|------|-------------|
| **Learning Task** | Tarea de aprendizaje principal que el estudiante debe completar. |
| **Support Info** | Información de soporte conceptual y contextual. |
| **Procedural Info** | Pasos y procedimientos concretos (cómo hacer algo). |
| **Verbal Protocol** | Guion verbal o explicación paso a paso. |
| **Examples** | Ejemplos resueltos y casos de estudio. |

### 8.2 Generar un Material

1. Dentro del curso, vaya a **Materiales** → **Generar Material**.
2. Configure los parámetros de generación:
   - **Tipo de material** (Learning Task, Support Info, etc.)
   - **Estudiante o grupo destinatario**
   - **Objetivos de aprendizaje** que cubre el material
   - **Efectos CLT** que se aplicarán (se cargan automáticamente desde la selección previa)
3. Haga clic en **Generar**.

El sistema envía la solicitud al servicio de IA y devuelve el material en segundos. El material se crea en estado **inactivo**.

### 8.3 Revisar y Activar un Material

1. En la lista de materiales, haga clic sobre el material generado para revisarlo.
2. Si el contenido es adecuado, haga clic en **Activar**.
3. El material queda disponible para los estudiantes del curso.

### 8.4 Configurar Temporizador (Timer)

Para materiales con tiempo límite:

1. Abra el material.
2. Haga clic en **Configurar Temporizador**.
3. Defina la duración en minutos.
4. Guarde. El estudiante verá un contador regresivo al acceder.

### 8.5 Logs de Acceso

El sistema registra automáticamente:
- Cuándo el estudiante accede al material.
- Cuándo lo completa.
- Tiempo total invertido.

Puede ver estos registros en la pestaña **Accesos** del material.

---

## 9. Calificación

> Disponible para: **Instructor**

### 9.1 Calificación Automática

Las preguntas de opción múltiple y escala son calificadas automáticamente al momento de envío. El sistema asigna puntajes y actualiza el estado de la respuesta a `auto-graded`.

### 9.2 Calificación Manual

Las preguntas de texto libre requieren revisión del instructor:

1. Vaya a **Calificación** → **Pendientes** (o desde la evaluación → pestaña Respuestas).
2. Seleccione la respuesta pendiente.
3. Lea la respuesta del estudiante.
4. Asigne una puntuación numérica y opcionalmente un comentario.
5. Haga clic en **Guardar Calificación**.

### 9.3 Revertir Calificación

Si necesita corregir una calificación ya asignada:

1. Abra la respuesta calificada.
2. Haga clic en **Revertir Calificación**.
3. La respuesta vuelve a estado pendiente para re-calificar.

### 9.4 Resumen de Calificaciones Pendientes

El panel **Calificación Pendiente** en el curso muestra un resumen de todas las evaluaciones con respuestas sin calificar, agrupadas por evaluación.

---

## 10. Reportes y Análisis de Datos

> Disponible para: **Instructor**, **Administrador**

### 10.1 Reporte del Instructor

Acceda desde **Reportes** → **Reporte del Curso**. Incluye:

- Total de estudiantes inscritos.
- Tasas de completación de evaluaciones.
- Puntajes promedio por evaluación.
- Datos agregados de carga cognitiva.
- Estadísticas de engagement con materiales.

### 10.2 Comparación Pre/Post

Útil para medir el impacto de la intervención instruccional:

1. Vaya a **Recolección de Datos** → **Comparación Pre/Post**.
2. Seleccione las evaluaciones de pre-test y post-test a comparar.
3. El sistema calcula diferencias de puntaje y cambios en carga cognitiva.

### 10.3 Exportar Datos (CSV)

Para análisis externos o investigación:

1. Vaya a **Recolección de Datos** → **Exportar**.
2. Haga clic en **Descargar CSV**.

El archivo incluye datos de respuestas, puntajes, perfiles y accesos a materiales.

### 10.4 Datos por Estudiante

1. Vaya a **Recolección de Datos** → seleccione un estudiante.
2. Visualice el historial completo: evaluaciones, respuestas, puntajes, accesos a materiales y evolución del perfil.

---

## 11. Vista del Estudiante

> Disponible para: **Estudiante**

### 11.1 Panel Principal

Al iniciar sesión, el estudiante ve sus cursos inscritos con estado y progreso general.

### 11.2 Acceder a un Curso

1. Haga clic sobre el nombre del curso.
2. Visualiza las evaluaciones y materiales disponibles (activos).

### 11.3 Completar una Evaluación

1. Haga clic en la evaluación disponible.
2. Lea las instrucciones con atención.
3. Si la evaluación tiene tiempo límite, el contador iniciará automáticamente al comenzar.
4. Responda todas las preguntas y haga clic en **Enviar**.

> **Importante:** Una vez enviada, no podrá modificar sus respuestas.

### 11.4 Acceder a Materiales de Aprendizaje

1. En el curso, vaya a la pestaña **Materiales**.
2. Haga clic en el material para abrirlo.
3. Si tiene temporizador, verá un contador regresivo.
4. Al terminar, haga clic en **Completar** para registrar su progreso.

### 11.5 Ver Mi Reporte Personal

1. Vaya a **Mi Reporte** dentro del curso.
2. Visualiza su puntaje en evaluaciones, perfil de aprendizaje y materiales completados.

### 11.6 Ver Mi Perfil de Aprendizaje

El perfil de aprendizaje (generado por el instructor) muestra:
- Nivel de motivación y estrategias predominantes.
- Carga cognitiva reportada.
- Recomendaciones de estudio.

---

## 12. Administración del Sistema

> Disponible para: **Administrador**

### 12.1 Gestión de Usuarios

1. Vaya a **Administración** → **Usuarios**.
2. Puede:
   - **Crear** nuevos instructores o estudiantes.
   - **Editar** datos de un usuario existente.
   - **Desactivar** una cuenta (el usuario no podrá iniciar sesión).

### 12.2 Asignación de Roles

Al crear o editar un usuario, seleccione el rol correspondiente:
- `admin` — Administrador
- `instructor` — Instructor
- `student` — Estudiante

### 12.3 Reportes Globales

Desde el panel de administración puede acceder a métricas globales del sistema:
- Total de cursos, usuarios e inscripciones activas.
- Actividad reciente de instructores y estudiantes.

---

## 13. Glosario

| Término | Definición |
|---------|------------|
| **CLT** | Cognitive Load Theory — Teoría de Carga Cognitiva. Marco teórico que describe cómo la mente humana procesa y almacena información. |
| **4C/ID** | Four-Component Instructional Design — Modelo de diseño instruccional que estructura materiales en cuatro componentes: tareas de aprendizaje, información de soporte, información procedimental y protocolos verbales. |
| **Carga Cognitiva Intrínseca** | Esfuerzo mental asociado a la complejidad inherente del contenido. |
| **Carga Cognitiva Extrínseca** | Esfuerzo mental generado por un diseño instruccional deficiente. |
| **Carga Cognitiva Germana** | Esfuerzo mental dedicado a construir y automatizar esquemas de conocimiento. |
| **MSLQ** | Motivated Strategies for Learning Questionnaire — instrumento para medir motivación y estrategias de aprendizaje. |
| **CLS** | Cognitive Load Scale — escala de medición de la carga cognitiva percibida. |
| **CIS** | Course Interest Scale — escala de interés en el curso. |
| **IMMS** | Instructional Materials Motivation Scale — escala de motivación hacia los materiales instruccionales. |
| **Perfil de Aprendizaje** | Conjunto de métricas que describe las características cognitivas y motivacionales de un estudiante. |
| **Efectos CLT** | Estrategias instruccionales derivadas de la investigación en CLT (ej. efecto de ejemplo resuelto, efecto de redundancia, efecto de expertise reverso). |
| **Material 4C/ID** | Contenido educativo generado según los cuatro componentes del modelo 4C/ID. |
| **Sanctum** | Sistema de autenticación basado en tokens usado por el backend. |
| **Estado activo/inactivo** | Indica si una evaluación o material está disponible para los estudiantes. |

---


