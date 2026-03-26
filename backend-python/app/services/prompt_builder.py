# app/services/prompt_builder.py
import json
import os
from typing import Dict, List, Union
from app.models.prompts import (
    MaterialGenerationRequest, MaterialType, ProfileType, CltEffect
)
from app.models.profiles import StudentProfile, GroupProfile

class PromptBuilder:
    """
    Construye prompts estructurados para Claude API
    """
    
    # Definición de efectos CLT
    CLT_EFFECTS = {
        # Efectos para Nuevo Conocimiento
        "goal_free": CltEffect(
            id="goal_free",
            name="Solución Libre (Goal-Free Effect)",
            description="Eliminar metas específicas para reducir carga cognitiva y permitir exploración",
            category="new_knowledge",
            application_guidance="Presenta problemas sin objetivos específicos, permitiendo que el estudiante explore diferentes soluciones"
        ),
        "worked_example": CltEffect(
            id="worked_example",
            name="Ejemplo Resuelto (Worked Example Effect)",
            description="Mostrar ejemplos completamente resueltos con explicaciones paso a paso",
            category="new_knowledge",
            application_guidance="Incluye ejemplos completamente trabajados antes de tareas similares"
        ),
        "completion_problem": CltEffect(
            id="completion_problem",
            name="Problema por Completar (Completion Problem)",
            description="Proporcionar problemas parcialmente resueltos para completar",
            category="new_knowledge",
            application_guidance="Da problemas iniciados que el estudiante debe completar"
        ),
        "split_attention": CltEffect(
            id="split_attention",
            name="Atención Dividida (Split Attention)",
            description="Integrar información relacionada espacialmente para evitar división de atención",
            category="new_knowledge",
            application_guidance="Mantén texto explicativo cerca de diagramas/código relacionado"
        ),
        "modality": CltEffect(
            id="modality",
            name="Modalidad (Modality Effect)",
            description="Usar combinación de modos de presentación (visual + auditivo)",
            category="new_knowledge",
            application_guidance="Combina explicaciones textuales con descripciones verbales cuando sea posible"
        ),
        "redundancy": CltEffect(
            id="redundancy",
            name="Redundancia (Redundancy Effect)",
            description="Evitar información redundante que no agrega valor",
            category="new_knowledge",
            application_guidance="Elimina información duplicada; presenta cada concepto una vez de forma clara"
        ),
        "variability": CltEffect(
            id="variability",
            name="Variabilidad (Variability Effect)",
            description="Usar múltiples ejemplos variados del mismo concepto",
            category="new_knowledge",
            application_guidance="Proporciona varios ejemplos que muestren diferentes aplicaciones del mismo concepto"
        ),
        "isolated_elements": CltEffect(
            id="isolated_elements",
            name="Elementos Aislados (Isolated Elements)",
            description="Presentar elementos complejos de forma aislada primero",
            category="new_knowledge",
            application_guidance="Introduce conceptos complejos elemento por elemento antes de combinarlos"
        ),
        "element_interactivity": CltEffect(
            id="element_interactivity",
            name="Interactividad (Element Interactivity)",
            description="Gestionar la interactividad entre elementos de información",
            category="new_knowledge",
            application_guidance="Estructura el contenido para minimizar elementos que deben procesarse simultáneamente"
        ),
        
        # Efectos para Conocimiento Previo
        "self_explanation": CltEffect(
            id="self_explanation",
            name="Auto-explicación (Self-Explanation)",
            description="Promover que el estudiante explique conceptos con sus propias palabras",
            category="prior_knowledge",
            application_guidance="Incluye preguntas que requieran que el estudiante explique el 'por qué' y 'cómo'"
        ),
        "imagination": CltEffect(
            id="imagination",
            name="Imaginación (Imagination Effect)",
            description="Pedir al estudiante que imagine o visualice procedimientos",
            category="prior_knowledge",
            application_guidance="Solicita que el estudiante visualice mentalmente procesos antes de ejecutarlos"
        ),
        "expertise_reversal": CltEffect(
            id="expertise_reversal",
            name="Reversión de Experiencia (Expertise Reversal)",
            description="Reducir guía explícita para estudiantes con conocimiento previo",
            category="prior_knowledge",
            application_guidance="Minimiza instrucciones paso a paso; proporciona problemas más abiertos"
        ),
        "guidance_fading": CltEffect(
            id="guidance_fading",
            name="Desvanecimiento de Guía (Guidance-Fading)",
            description="Reducir gradualmente el nivel de guía proporcionada",
            category="prior_knowledge",
            application_guidance="Comienza con guía completa y reduce progresivamente el soporte"
        ),
        "collective_memory": CltEffect(
            id="collective_memory",
            name="Memoria Colectiva (Collective Memory)",
            description="Aprovechar conocimiento compartido en actividades grupales",
            category="prior_knowledge",
            application_guidance="Diseña actividades que permitan a estudiantes compartir conocimientos previos"
        ),
        "self_management": CltEffect(
            id="self_management",
            name="Autogestión (Self-Management)",
            description="Fomentar que estudiantes gestionen su propio aprendizaje",
            category="prior_knowledge",
            application_guidance="Da autonomía al estudiante en la selección de estrategias y secuencia de aprendizaje"
        ),
        "human_movement": CltEffect(
            id="human_movement",
            name="Movimiento Humano (Human Movement)",
            description="Incorporar actividades que involucren movimiento físico",
            category="prior_knowledge",
            application_guidance="Sugiere actividades prácticas que requieran movimiento o manipulación física"
        ),
        "transient_information": CltEffect(
            id="transient_information",
            name="Información Transitoria (Transient Information)",
            description="Gestionar información temporal para evitar sobrecarga",
            category="prior_knowledge",
            application_guidance="Proporciona referencias permanentes para información que desaparece rápidamente"
        )
    }
    
    def __init__(self):
        pass
    
    def build_system_prompt(self) -> str:
        """
        Construye el system prompt base para Claude
        """
        return """Eres un diseñador instruccional experto especializado en:
- Teoría de Carga Cognitiva (CLT - Cognitive Load Theory)
- Modelo 4C/ID (Four-Component Instructional Design)
- Modelo ARCS de motivación (Attention, Relevance, Confidence, Satisfaction)
- Estrategias de aprendizaje diferenciadas
- Programación y desarrollo de software

Tu tarea es generar material instruccional de alta calidad, personalizado según 
el perfil del estudiante o grupo, aplicando los principios pedagógicos solicitados.

IMPORTANTE:
- Genera contenido en español claro y profesional
- Sigue estrictamente las instrucciones sobre efectos CLT
- Aplica el modelo ARCS en todo el material
- Adapta el contenido al nivel de conocimiento previo del estudiante
- Usa ejemplos concretos y relevantes en programación
- Proporciona el contenido en el formato JSON estructurado solicitado"""
    
    def build_profile_section(
        self,
        profile_type: ProfileType,
        profile_data: Union[Dict, StudentProfile, GroupProfile]
    ) -> str:
        """
        Construye la sección de perfil del prompt
        """
        if profile_type == ProfileType.INDIVIDUAL:
            return self._build_individual_profile_section(profile_data)
        else:
            return self._build_group_profile_section(profile_data)
    
    def _build_individual_profile_section(self, profile: Union[Dict, StudentProfile]) -> str:
        """
        Perfil individual del estudiante
        """
        if isinstance(profile, dict):
            summary = profile.get('profile_summary', {})
            knowledge = profile.get('knowledge_assessment', {})
        else:
            summary = profile.profile_summary.dict()
            knowledge = profile.knowledge_assessment.dict()
        
        # Scores de evaluaciones de conocimiento
        recall_initial = knowledge.get('recall', {}).get('percentage', 0)
        comprehension_initial = knowledge.get('comprehension', {}).get('percentage', 0)
        recall_final = knowledge.get('recall_final', {}).get('percentage')
        comprehension_final = knowledge.get('comprehension_final', {}).get('percentage')

        section = f"""
## PERFIL DEL ESTUDIANTE

### Resumen General
- **Nivel de Motivación**: {summary.get('overall_motivation', 'N/A')}
- **Nivel de Estrategias de Aprendizaje**: {summary.get('overall_strategies', 'N/A')}
- **Nivel de Conocimiento Previo**: {summary.get('prior_knowledge', 'N/A')}

### Scores de Evaluaciones de Conocimiento
- **Recall Inicial**: {recall_initial}% correcto
- **Comprensión Inicial**: {comprehension_initial}% correcto
"""
        if recall_final is not None:
            section += f"- **Recall Final**: {recall_final}% correcto\n"
        if comprehension_final is not None:
            section += f"- **Comprensión Final**: {comprehension_final}% correcto\n"

        section += f"""- **Nivel General de Conocimiento**: {knowledge.get('overall_level', 'N/A')}
"""

        # Agregar scores MSLQ por dimensión si están disponibles
        mslq_scores = profile.get('mslq_scores', {}) if isinstance(profile, dict) else {}
        if mslq_scores:
            MSLQ_LABELS = {
                'intrinsic_goal_orientation': 'Orientación a Metas Intrínsecas',
                'extrinsic_goal_orientation': 'Orientación a Metas Extrínsecas',
                'task_value': 'Valor de la Tarea',
                'control_beliefs': 'Creencias de Control',
                'self_efficacy': 'Autoeficacia',
                'test_anxiety': 'Ansiedad ante Exámenes',
                'rehearsal': 'Repaso',
                'elaboration': 'Elaboración',
                'organization': 'Organización',
                'critical_thinking': 'Pensamiento Crítico',
                'metacognitive_self_regulation': 'Autorregulación Metacognitiva',
                'time_study_environment': 'Manejo del Tiempo y Ambiente',
                'effort_regulation': 'Regulación del Esfuerzo',
                'peer_learning': 'Aprendizaje entre Pares',
                'help_seeking': 'Búsqueda de Ayuda',
            }
            section += "\n### Escalas MSLQ (Motivación y Estrategias de Aprendizaje)\n"
            section += "*(escala 1-7: bajo <3.5, medio 3.5-5.4, alto ≥5.5)*\n"
            for dim, data in mslq_scores.items():
                label = MSLQ_LABELS.get(dim, dim)
                avg = data.get('average', 0)
                level = data.get('level', 'N/A')
                section += f"- **{label}**: {avg:.2f} ({level})\n"

        section += f"""
### Fortalezas Identificadas
{self._format_list(summary.get('key_strengths', []))}

### Áreas que Requieren Apoyo
{self._format_list(summary.get('areas_for_support', []))}

### Recomendaciones Instruccionales
Este estudiante se beneficiará de:
"""
        
        # Agregar recomendaciones específicas basadas en el perfil
        if isinstance(profile, dict):
            recommendations = profile.get('recommendations', [])
        else:
            recommendations = profile.recommendations
        
        for rec in recommendations:
            section += f"- {rec}\n"
        
        return section
    
    def _build_group_profile_section(self, profile: Union[Dict, GroupProfile]) -> str:
        """
        Perfil grupal del curso
        """
        if isinstance(profile, dict):
            summary = profile.get('group_summary', {})
            knowledge = profile.get('knowledge_averages', {})
            student_count = profile.get('student_count', 0)
        else:
            summary = profile.group_summary
            knowledge = profile.knowledge_averages
            student_count = profile.student_count
        
        section = f"""
## PERFIL DEL GRUPO

### Información General
- **Número de Estudiantes**: {student_count}
- **Característica del Grupo**: {summary.get('group_characteristics', 'N/A')}

### Niveles Predominantes
- **Motivación**: {summary.get('predominant_motivation', 'N/A')}
- **Estrategias de Aprendizaje**: {summary.get('predominant_strategies', 'N/A')}
- **Conocimiento Previo**: {summary.get('predominant_knowledge', 'N/A')}

### Promedios de Conocimiento Previo
- **Recall Promedio**: {knowledge.get('recall', {}).get('average', 0)}%
- **Comprensión Promedio**: {knowledge.get('comprehension', {}).get('average', 0)}%
- **Nivel General del Grupo**: {knowledge.get('overall', {}).get('level', 'N/A')}

### Recomendaciones para Enseñanza Grupal
"""
        
        if isinstance(profile, dict):
            recommendations = profile.get('teaching_recommendations', [])
        else:
            recommendations = profile.teaching_recommendations
        
        for rec in recommendations:
            section += f"- {rec}\n"
        
        return section
    
    def build_learning_objectives_section(self, objectives: List[Dict]) -> str:
        """
        Construye la sección de objetivos de aprendizaje
        """
        section = """
## OBJETIVOS DE APRENDIZAJE DEL CURSO

El material instruccional debe estar alineado con los siguientes objetivos:

"""
        for i, obj in enumerate(objectives, 1):
            section += f"{i}. {obj.get('description', '')}\n"
            if obj.get('bloom_level'):
                section += f"   (Nivel de Bloom: {obj['bloom_level']})\n"
        
        return section
    
    def build_clt_effects_section(self, selected_effects: List[str]) -> str:
        """
        Construye la sección de efectos CLT a aplicar
        """
        section = """
## EFECTOS DE TEORÍA DE CARGA COGNITIVA A APLICAR

Debes aplicar los siguientes efectos CLT en el material que generes:

"""
        for effect_id in selected_effects:
            effect = self.CLT_EFFECTS.get(effect_id)
            if effect:
                section += f"""
### {effect.name}
**Descripción**: {effect.description}
**Cómo aplicarlo**: {effect.application_guidance}

"""
        
        return section
    
    def build_arcs_section(self) -> str:
        """
        Construye la sección del modelo ARCS
        """
        return """
## APLICACIÓN DEL MODELO ARCS

Debes integrar los cuatro componentes del modelo ARCS en el material:

### A - Atención (Attention)
- Captura la atención del estudiante desde el inicio
- Usa elementos sorprendentes o intrigantes
- Varía el formato y estilo de presentación

### R - Relevancia (Relevance)
- Conecta el contenido con experiencias previas del estudiante
- Muestra aplicaciones prácticas y del mundo real
- Explica el "por qué" y "para qué" del tema

### C - Confianza (Confidence)
- Estructura el contenido con dificultad creciente
- Proporciona expectativas claras de lo que se logrará
- Ofrece oportunidades para el éxito

### S - Satisfacción (Satisfaction)
- Proporciona retroalimentación positiva y constructiva
- Muestra el progreso y logros alcanzados
- Conecta el aprendizaje con metas futuras
"""
    
    def build_differentiated_strategies_section(self, profile_type: ProfileType) -> str:
        """
        Construye la sección de estrategias diferenciadas
        """
        if profile_type == ProfileType.GROUP:
            return ""  # No se aplican estrategias individuales en material grupal
        
        return """
## ESTRATEGIAS DE APRENDIZAJE DIFERENCIADAS

Basándote en el perfil del estudiante, incorpora estrategias específicas:

### Si el estudiante tiene debilidades en estrategias cognitivas:
- Modela explícitamente técnicas de repaso y elaboración
- Proporciona organizadores gráficos y mapas conceptuales
- Incluye guías para toma de notas efectiva

### Si el estudiante tiene debilidades en autorregulación:
- Incluye checklist de pasos a seguir
- Proporciona estrategias de monitoreo de comprensión
- Sugiere técnicas de autoevaluación

### Si el estudiante tiene alta ansiedad ante evaluaciones:
- Usa lenguaje alentador y positivo
- Proporciona práctica en entornos de bajo riesgo
- Incluye estrategias de manejo de ansiedad
"""
    
    def build_material_type_instructions(
        self,
        material_type: MaterialType,
        topic: str
    ) -> str:
        """
        Construye instrucciones específicas según el tipo de material
        """
        instructions = {
            MaterialType.LEARNING_TASKS: f"""
## TIPO DE MATERIAL: TAREAS DE APRENDIZAJE

Genera una secuencia de tareas de aprendizaje sobre: **{topic}**

### Características Requeridas:
1. **Dificultad Creciente**: Diseña 3-5 tareas que incrementen progresivamente en complejidad
2. **Escenarios Auténticos**: Usa situaciones realistas de programación
3. **Explicación del POR QUÉ y PARA QUÉ**: Explica claramente la relevancia de cada tarea
4. **Elementos del 4C/ID**:
   - Tareas significativas y completas
   - Presentación en contexto auténtico
   - Soporte gradualmente decreciente

### Formato de Salida JSON:
```json
{{
  "tasks": [
    {{
      "task_number": 1,
      "title": "Título de la tarea",
      "difficulty_level": "básico|intermedio|avanzado",
      "description": "Descripción completa del problema",
      "context": "Escenario del mundo real",
      "why_relevant": "Por qué esta tarea es importante",
      "expected_outcome": "Qué se logrará",
      "estimated_time": "tiempo en minutos",
      "support_level": "alto|medio|bajo",
      "arcs_integration": {{
        "attention": "Cómo captura atención",
        "relevance": "Por qué es relevante",
        "confidence": "Cómo construye confianza",
        "satisfaction": "Cómo genera satisfacción"
      }}
    }}
  ]
}}
```
""",
            MaterialType.SUPPORT_INFO: f"""
## TIPO DE MATERIAL: INFORMACIÓN DE SOPORTE

Genera información de soporte teórica sobre: **{topic}**

### Características Requeridas:
1. **Teoría Fundamental**: Conceptos básicos y fundamentos teóricos
2. **Explicaciones Claras**: Lenguaje accesible adaptado al nivel del estudiante
3. **Ejemplos Ilustrativos**: Ejemplos concretos de cada concepto
4. **Organización Lógica**: Estructura que facilite la comprensión

### Formato de Salida JSON:
```json
{{
  "sections": [
    {{
      "title": "Título de la sección",
      "order": 1,
      "content": "Contenido explicativo completo",
      "key_concepts": ["concepto1", "concepto2"],
      "examples": [
        {{
          "description": "Descripción del ejemplo",
          "code": "código si aplica"
        }}
      ],
      "arcs_integration": {{
        "attention": "Elemento que captura atención",
        "relevance": "Conexión con aplicaciones reales",
        "confidence": "Cómo ayuda a sentirse capaz",
        "satisfaction": "Qué logro representa"
      }}
    }}
  ],
  "summary": "Resumen general del contenido",
  "key_takeaways": ["punto clave 1", "punto clave 2"]
}}
```
""",
            MaterialType.PROCEDURAL_INFO: f"""
## TIPO DE MATERIAL: INFORMACIÓN PROCEDIMENTAL

Genera información procedimental (ejemplos, guías, modelos) sobre: **{topic}**

### Características Requeridas:
1. **Ejemplos Isomórficos**: Ejemplos con estructura similar pero contexto diferente
2. **Guías de Preguntas**: Preguntas que guíen el pensamiento
3. **Modelos y Mapas**: Representaciones visuales del conocimiento
4. **Procedimientos Paso a Paso**: Cuando sea apropiado

### Formato de Salida JSON:
```json
{{
  "worked_examples": [
    {{
      "title": "Título del ejemplo",
      "problem": "Descripción del problema",
      "solution_steps": [
        {{
          "step_number": 1,
          "description": "Qué se hace",
          "explanation": "Por qué se hace",
          "code": "código si aplica"
        }}
      ],
      "key_insights": ["insight 1", "insight 2"]
    }}
  ],
  "guiding_questions": [
    "¿Pregunta que promueve reflexión?",
    "¿Pregunta que conecta conceptos?"
  ],
  "conceptual_models": [
    {{
      "title": "Título del modelo",
      "description": "Descripción del modelo mental",
      "visual_representation": "Descripción de cómo visualizarlo"
    }}
  ]
}}
```
""",
            MaterialType.VERBAL_PROTOCOLS: f"""
## TIPO DE MATERIAL: PROTOCOLOS VERBALES

Genera un protocolo verbal (think-aloud) sobre: **{topic}**

### Características Requeridas:
1. **Perspectiva de Experto**: Desde el punto de vista de un programador experimentado
2. **Enfoque en CÓMO y POR QUÉ**: Explicar el proceso de pensamiento
3. **Naturalidad**: Como si estuvieras pensando en voz alta
4. **Transparencia de Proceso**: Mostrar también dudas y decisiones

### Formato de Salida JSON:
```json
{{
  "protocol_title": "Título del protocolo",
  "scenario": "Descripción del escenario/problema",
  "think_aloud_transcript": "Transcripción completa del pensamiento en voz alta, incluyendo:\n- Análisis inicial del problema\n- Consideraciones y alternativas\n- Decisiones tomadas y por qué\n- Proceso de implementación\n- Reflexiones durante el proceso\n- Validación de la solución",
  "key_thinking_patterns": [
    "Patrón de pensamiento 1",
    "Patrón de pensamiento 2"
  ],
  "teaching_points": [
    "Punto de enseñanza 1",
    "Punto de enseñanza 2"
  ]
}}
```
""",
            MaterialType.EXAMPLE: f"""
## TIPO DE MATERIAL: EJEMPLO REAL

Genera un ejemplo real y completo sobre: **{topic}**

### Características Requeridas:
1. **Completitud**: Ejemplo funcional y completo
2. **Calidad Profesional**: Código que siga best practices
3. **Comentarios Explicativos**: Código bien comentado
4. **Aplicación Práctica**: Problema del mundo real

### Formato de Salida JSON:
```json
{{
  "example_title": "Título del ejemplo",
  "description": "Descripción del problema que resuelve",
  "use_case": "Caso de uso del mundo real",
  "code": "Código completo con comentarios",
  "explanation": "Explicación detallada de cómo funciona",
  "key_concepts_demonstrated": ["concepto 1", "concepto 2"],
  "possible_variations": [
    "Variación 1 del ejemplo",
    "Variación 2 del ejemplo"
  ],
  "common_mistakes": [
    "Error común 1 y cómo evitarlo",
    "Error común 2 y cómo evitarlo"
  ]
}}
```
"""
        }
        
        return instructions.get(material_type, "")
    
    def build_output_format_section(self) -> str:
        """
        Construye la sección de formato de salida
        """
        return """
## FORMATO DE SALIDA

IMPORTANTE: 
- Devuelve ÚNICAMENTE el JSON solicitado, sin texto adicional antes o después
- NO incluyas markdown code blocks (```)
- El JSON debe ser válido y parseable
- Usa español para todo el contenido
- Sé específico y detallado en las explicaciones
"""
    
    def build_complete_prompt(self, request: MaterialGenerationRequest) -> tuple[str, str]:
        """
        Construye el prompt completo para Claude API
        Returns: (system_prompt, user_prompt)
        """
        system_prompt = self.build_system_prompt()
        
        user_prompt = f"""
{self.build_profile_section(request.profile_type, request.profile_data)}

{self.build_learning_objectives_section([obj.dict() for obj in request.learning_objectives])}

{self.build_clt_effects_section(request.selected_clt_effects)}

{self.build_arcs_section()}

{self.build_differentiated_strategies_section(request.profile_type)}

{self.build_material_type_instructions(request.material_type, request.topic)}

{self.build_output_format_section()}
"""
        
        if request.additional_context:
            user_prompt += f"""
## CONTEXTO ADICIONAL

{request.additional_context}
"""
        type_m =request.material_type
        carpeta_destino = "C:/Projects/CLT4BP/docs/"
        prefijo = "backup_"
        nombre_archivo = "material.json"
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
        ruta_completa = os.path.join(carpeta_destino, f"{prefijo}{nombre_archivo}")

        # 4. Guardar la variable en el archivo JSON
        with open(ruta_completa, 'w', encoding='utf-8') as f:
            json.dump(user_prompt, f, indent=4, ensure_ascii=False)
        return system_prompt, user_prompt
    
    def _format_list(self, items: List[str]) -> str:
        """
        Formatea una lista de items
        """
        if not items:
            return "- Ninguna identificada\n"
        return "\n".join([f"- {item}" for item in items]) + "\n"