<template>
  <AppLayout>
    <div class="container mx-auto max-w-4xl">
      <div class="flex items-center mb-8">
        <router-link :to="`/instructor/courses/${route.params.courseId}/assessments`" class="btn btn-ghost btn-circle mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </router-link>
        <h1 class="text-4xl font-bold">Crear Evaluaci&oacute;n</h1>
      </div>

      <!-- Opci&oacute;n para crear desde plantilla -->
      <div v-if="availableTemplates.length > 0" class="card bg-primary/10 shadow-xl mb-6">
        <div class="card-body">
          <h2 class="card-title text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Plantillas Disponibles
          </h2>
          <p class="text-sm mb-4">
            Puedes crear una evaluaci&oacute;n r&aacute;pidamente usando una de las plantillas predefinidas con todas las preguntas ya configuradas.
          </p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
              v-for="template in availableTemplates"
              :key="template.id"
              class="card bg-base-100 cursor-pointer hover:shadow-lg transition-shadow"
              @click="createFromTemplate(template)"
            >
              <div class="card-body p-4">
                <h3 class="font-bold">{{ template.title }}</h3>
                <p class="text-sm text-gray-600">{{ template.description }}</p>
                <div class="flex gap-2 mt-2">
                  <span class="badge badge-primary">{{ getTemplateTypeLabel(template.assessment_type) }}</span>
                  <span class="badge badge-ghost">{{ template.time_limit ? template.time_limit + ' min' : 'Sin l&iacute;mite' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="divider" v-if="availableTemplates.length > 0">O crear manualmente</div>

      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <form @submit.prevent="handleSubmit">
            <div v-if="error" class="alert alert-error mb-4">
              <span>{{ error }}</span>
            </div>

            <!-- Tipo de Evaluaci&oacute;n -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Tipo de Evaluaci&oacute;n *</span>
              </label>
              <select v-model="form.assessment_type" class="select select-bordered" required @change="onTypeChange">
                <option value="">Seleccionar tipo...</option>
                <option value="prior_knowledge">Conocimiento Previo</option>
                <option value="recall_initial">Recall Inicial</option>
                <option value="comprehension_initial">Comprensi&oacute;n Inicial</option>
                <option value="mslq_motivation_initial">MSLQ Motivaci&oacute;n Inicial</option>
                <option value="mslq_strategies">MSLQ Estrategias</option>
                <option value="recall_final">Recall Final</option>
                <option value="comprehension_final">Comprensi&oacute;n Final</option>
                <option value="cognitive_load">Carga Cognitiva</option>
                <option value="mslq_motivation_final">MSLQ Motivaci&oacute;n Final</option>
                <option value="course_interest">Inter&eacute;s en el Curso (CIS)</option>
                <option value="imms">Materiales Motivacionales (IMMS)</option>
              </select>
            </div>

            <!-- Alerta de plantilla disponible -->
            <div v-if="templateForType" class="alert alert-info mt-4">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <div>
                <h3 class="font-bold">Plantilla disponible</h3>
                <div class="text-sm">
                  Existe una plantilla con {{ templateForType.questions?.length || 'todas las' }} preguntas predefinidas para este tipo de evaluaci&oacute;n.
                </div>
              </div>
              <button type="button" class="btn btn-sm btn-primary" @click="loadTemplateQuestions">
                Cargar Preguntas
              </button>
            </div>

            <!-- T&iacute;tulo -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">T&iacute;tulo *</span>
              </label>
              <input
                v-model="form.title"
                type="text"
                placeholder="Ej: Evaluaci&oacute;n de Conocimientos Previos"
                class="input input-bordered"
                required
              />
            </div>

            <!-- Descripci&oacute;n -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Descripci&oacute;n</span>
              </label>
              <textarea
                v-model="form.description"
                placeholder="Descripci&oacute;n de la evaluaci&oacute;n..."
                class="textarea textarea-bordered h-24"
              ></textarea>
            </div>

            <!-- Tiempo L&iacute;mite -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Tiempo L&iacute;mite (minutos)</span>
              </label>
              <input
                v-model.number="form.time_limit"
                type="number"
                placeholder="Dejar vac&iacute;o para sin l&iacute;mite"
                class="input input-bordered"
                min="1"
              />
            </div>

            <!-- Preguntas -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Preguntas * ({{ form.questions.length }} preguntas)</span>
              </label>

              <!-- Resumen de preguntas cargadas desde plantilla -->
              <div v-if="questionsLoadedFromTemplate" class="alert alert-success mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ form.questions.length }} preguntas cargadas desde la plantilla. Puedes editarlas si lo necesitas.</span>
                <button type="button" class="btn btn-sm btn-ghost" @click="toggleQuestionsVisibility">
                  {{ showQuestions ? 'Ocultar' : 'Mostrar' }} Preguntas
                </button>
              </div>

              <div v-show="!questionsLoadedFromTemplate || showQuestions" class="space-y-4">
                <div v-for="(question, index) in form.questions" :key="question.id || index" class="card bg-base-200">
                  <div class="card-body">
                    <div class="flex justify-between items-start">
                      <h3 class="font-bold">Pregunta {{ index + 1 }}</h3>
                      <button
                        type="button"
                        @click="removeQuestion(index)"
                        class="btn btn-error btn-sm btn-circle"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>

                    <!-- Dimensi&oacute;n (solo para MSLQ) -->
                    <div v-if="question.dimension" class="badge badge-outline mb-2">
                      {{ formatDimension(question.dimension) }}
                    </div>

                    <!-- Tipo de Pregunta -->
                    <div class="form-control">
                      <label class="label">
                        <span class="label-text">Tipo de Pregunta</span>
                      </label>
                      <select v-model="question.type" class="select select-bordered select-sm">
                        <option value="multiple_choice">Opci&oacute;n M&uacute;ltiple</option>
                        <option value="text">Respuesta Abierta</option>
                        <option value="scale">Escala (1-5)</option>
                        <option value="likert">Likert (1-7)</option>
                      </select>
                    </div>

                    <!-- Texto de la Pregunta -->
                    <div class="form-control">
                      <label class="label">
                        <span class="label-text">Pregunta</span>
                      </label>
                      <textarea
                        v-model="question.question"
                        class="textarea textarea-bordered textarea-sm"
                        required
                      ></textarea>
                    </div>

                    <!-- Opciones (solo para multiple_choice) -->
                    <div v-if="question.type === 'multiple_choice'" class="form-control">
                      <label class="label">
                        <span class="label-text">Opciones</span>
                      </label>
                      <div class="space-y-2">
                        <div v-for="(option, optIndex) in question.options" :key="optIndex" class="flex gap-2">
                          <input
                            v-model="question.options[optIndex]"
                            type="text"
                            placeholder="Opci&oacute;n..."
                            class="input input-bordered input-sm flex-1"
                          />
                          <button
                            type="button"
                            @click="removeOption(index, optIndex)"
                            class="btn btn-error btn-sm btn-square"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                          </button>
                        </div>
                        <button
                          type="button"
                          @click="addOption(index)"
                          class="btn btn-outline btn-sm"
                        >
                          Agregar Opci&oacute;n
                        </button>
                      </div>
                    </div>

                    <!-- Opciones Likert (solo lectura) -->
                    <div v-if="question.type === 'likert' && question.options" class="form-control">
                      <label class="label">
                        <span class="label-text">Escala Likert</span>
                      </label>
                      <div class="flex flex-wrap gap-2">
                        <span v-for="opt in question.options" :key="opt.value" class="badge badge-outline">
                          {{ opt.value }}: {{ opt.label || '-' }}
                        </span>
                      </div>
                    </div>

                    <!-- Respuesta Correcta (opcional para multiple_choice) -->
                    <div v-if="question.type === 'multiple_choice' && Array.isArray(question.options)" class="form-control">
                      <label class="label">
                        <span class="label-text">Respuesta Correcta (opcional para autocalificaci&oacute;n)</span>
                      </label>
                      <select v-model="question.correct_answer" class="select select-bordered select-sm">
                        <option value="">Sin respuesta correcta definida</option>
                        <option v-for="(opt, i) in question.options" :key="i" :value="i">
                          Opci&oacute;n {{ i + 1 }}: {{ typeof opt === 'string' ? opt : opt.label }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>

                <button type="button" @click="addQuestion" class="btn btn-outline w-full">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Agregar Pregunta
                </button>
              </div>
            </div>

            <!-- Estado Inicial -->
            <div class="form-control">
              <label class="label cursor-pointer">
                <span class="label-text font-bold">Activar evaluaci&oacute;n inmediatamente</span>
                <input v-model="form.is_active" type="checkbox" class="checkbox checkbox-primary" />
              </label>
            </div>

            <div class="alert alert-info mt-6">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <div>
                <h3 class="font-bold">Informaci&oacute;n</h3>
                <div class="text-xs">
                  Las evaluaciones inactivas no ser&aacute;n visibles para los estudiantes hasta que las actives.
                </div>
              </div>
            </div>

            <div class="divider"></div>

            <div class="card-actions justify-end">
              <router-link :to="`/instructor/courses/${route.params.courseId}/assessments`" class="btn btn-outline">
                Cancelar
              </router-link>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="assessmentStore.loading || form.questions.length === 0"
              >
                <span v-if="assessmentStore.loading" class="loading loading-spinner"></span>
                <span v-else>Crear Evaluaci&oacute;n</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAssessmentStore } from '../../stores/assessments';
import AppLayout from '../../components/layout/AppLayout.vue';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const assessmentStore = useAssessmentStore();

const form = ref({
  assessment_type: '',
  title: '',
  description: '',
  time_limit: null,
  questions: [],
  is_active: false,
});

const error = ref(null);
const availableTemplates = ref([]);
const allTemplates = ref([]);
const questionsLoadedFromTemplate = ref(false);
const showQuestions = ref(false);

// Cargar plantillas disponibles al iniciar
onMounted(async () => {
  try {
    // Cargar plantillas disponibles para el curso
    const response = await axios.get(
      `http://localhost:8000/api/courses/${route.params.courseId}/available-templates`
    );
    availableTemplates.value = response.data.available_templates || [];

    // Cargar todas las plantillas para referencia
    const allResponse = await axios.get('http://localhost:8000/api/assessment-templates');
    allTemplates.value = allResponse.data.templates || [];
  } catch (err) {
    console.error('Error al cargar plantillas:', err);
  }
});

// Plantilla correspondiente al tipo seleccionado
const templateForType = computed(() => {
  if (!form.value.assessment_type) return null;
  return allTemplates.value.find(t => t.assessment_type === form.value.assessment_type);
});

const getTemplateTypeLabel = (type) => {
  const labels = {
    'mslq_motivation_initial': 'MSLQ Motivaci\u00f3n',
    'mslq_strategies': 'MSLQ Estrategias',
    'prior_knowledge': 'Conocimiento Previo',
    'cognitive_load': 'Carga Cognitiva',
  };
  return labels[type] || type;
};

const formatDimension = (dimension) => {
  const translations = {
    'intrinsic_goal_orientation': 'Orientaci\u00f3n a metas intr\u00ednsecas',
    'extrinsic_goal_orientation': 'Orientaci\u00f3n a metas extr\u00ednsecas',
    'task_value': 'Valor de la tarea',
    'control_beliefs': 'Creencias de control',
    'self_efficacy': 'Autoeficacia',
    'test_anxiety': 'Ansiedad ante ex\u00e1menes',
    'rehearsal': 'Repaso',
    'elaboration': 'Elaboraci\u00f3n',
    'organization': 'Organizaci\u00f3n',
    'critical_thinking': 'Pensamiento cr\u00edtico',
    'metacognitive_self_regulation': 'Autorregulaci\u00f3n metacognitiva',
    'time_management': 'Gesti\u00f3n del tiempo',
    'effort_regulation': 'Regulaci\u00f3n del esfuerzo',
    'peer_learning': 'Aprendizaje entre pares',
    'help_seeking': 'B\u00fasqueda de ayuda'
  };
  return translations[dimension] || dimension;
};

const onTypeChange = () => {
  // Si cambia el tipo, resetear las preguntas si fueron cargadas de plantilla
  if (questionsLoadedFromTemplate.value) {
    questionsLoadedFromTemplate.value = false;
    form.value.questions = [];
  }
};

const loadTemplateQuestions = async () => {
  if (!templateForType.value) return;

  try {
    // Obtener detalles completos de la plantilla
    const response = await axios.get(
      `http://localhost:8000/api/assessment-templates/${templateForType.value.id}`
    );

    const template = response.data.template;

    // Cargar datos de la plantilla
    form.value.title = template.title;
    form.value.description = template.description || '';
    form.value.time_limit = template.time_limit;

    // Cargar preguntas de la plantilla
    form.value.questions = (template.questions || []).map(q => ({
      ...q,
      id: q.id || Date.now().toString() + Math.random().toString(36).substr(2, 9)
    }));

    questionsLoadedFromTemplate.value = true;
    showQuestions.value = false;
  } catch (err) {
    console.error('Error al cargar plantilla:', err);
    error.value = 'Error al cargar las preguntas de la plantilla';
  }
};

const createFromTemplate = async (template) => {
  try {
    // Crear evaluaci\u00f3n directamente desde la plantilla usando el endpoint
    const response = await axios.post(
      `http://localhost:8000/api/courses/${route.params.courseId}/assessments/from-template/${template.id}`
    );

    // Redirigir a la lista de evaluaciones
    router.push(`/instructor/courses/${route.params.courseId}/assessments`);
  } catch (err) {
    if (err.response?.status === 409) {
      error.value = err.response.data.message || 'Ya existe una evaluaci\u00f3n de este tipo en el curso';
    } else {
      error.value = err.response?.data?.message || 'Error al crear la evaluaci\u00f3n desde plantilla';
    }
  }
};

const toggleQuestionsVisibility = () => {
  showQuestions.value = !showQuestions.value;
};

const addQuestion = () => {
  form.value.questions.push({
    id: Date.now().toString(),
    type: 'multiple_choice',
    question: '',
    options: [''],
    correct_answer: '',
  });
};

const removeQuestion = (index) => {
  form.value.questions.splice(index, 1);
};

const addOption = (questionIndex) => {
  form.value.questions[questionIndex].options.push('');
};

const removeOption = (questionIndex, optionIndex) => {
  form.value.questions[questionIndex].options.splice(optionIndex, 1);
};

const handleSubmit = async () => {
  error.value = null;

  if (form.value.questions.length === 0) {
    error.value = 'Debes agregar al menos una pregunta';
    return;
  }

  try {
    await assessmentStore.createAssessment(route.params.courseId, form.value);
    router.push(`/instructor/courses/${route.params.courseId}/assessments`);
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al crear la evaluaci\u00f3n';
  }
};
</script>
