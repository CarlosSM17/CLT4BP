<template>
  <AppLayout>
    <div class="container mx-auto max-w-4xl">
      <div class="flex items-center mb-8">
        <router-link :to="`/instructor/courses/${route.params.courseId}/assessments`" class="btn btn-ghost btn-circle mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </router-link>
        <h1 class="text-4xl font-bold">Editar Evaluación</h1>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-16">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <div v-else class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <form @submit.prevent="handleSubmit">
            <div v-if="error" class="alert alert-error mb-4">
              <span>{{ error }}</span>
            </div>

            <!-- Tipo de Evaluación (solo lectura) -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Tipo de Evaluación</span>
              </label>
              <select v-model="form.assessment_type" class="select select-bordered" disabled>
                <option value="recall_initial">Recall Inicial</option>
                <option value="comprehension_initial">Comprensión Inicial</option>
                <option value="mslq_motivation_initial">MSLQ Motivación Inicial</option>
                <option value="mslq_strategies">MSLQ Estrategias</option>
                <option value="recall_final">Recall Final</option>
                <option value="comprehension_final">Comprensión Final</option>
                <option value="cognitive_load">Carga Cognitiva</option>
                <option value="mslq_motivation_final">MSLQ Motivación Final</option>
                <option value="course_interest">Interés en el Curso (CIS)</option>
                <option value="imms">Materiales Motivacionales (IMMS)</option>
              </select>
              <label class="label">
                <span class="label-text-alt">El tipo de evaluación no se puede cambiar después de crear</span>
              </label>
            </div>

            <!-- Título -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Título *</span>
              </label>
              <input
                v-model="form.title"
                type="text"
                placeholder="Ej: Evaluación de Conocimientos Previos"
                class="input input-bordered"
                required
              />
            </div>

            <!-- Descripción -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Descripción</span>
              </label>
              <textarea
                v-model="form.description"
                placeholder="Descripción de la evaluación..."
                class="textarea textarea-bordered h-24"
              ></textarea>
            </div>

            <!-- Tiempo Límite -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Tiempo Límite (minutos)</span>
              </label>
              <input
                v-model.number="form.time_limit"
                type="number"
                placeholder="Dejar vacío para sin límite"
                class="input input-bordered"
                min="1"
              />
            </div>

            <!-- Preguntas -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Preguntas *</span>
              </label>

              <div class="space-y-4">
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

                    <!-- Tipo de Pregunta -->
                    <div class="form-control">
                      <label class="label">
                        <span class="label-text">Tipo de Pregunta</span>
                      </label>
                      <select v-model="question.type" class="select select-bordered select-sm">
                        <option value="multiple_choice">Opción Múltiple</option>
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
                            placeholder="Opción..."
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
                          Agregar Opción
                        </button>
                      </div>
                    </div>

                    <!-- Respuesta Correcta (opcional para multiple_choice) -->
                    <div v-if="question.type === 'multiple_choice'" class="form-control">
                      <label class="label">
                        <span class="label-text">Respuesta Correcta (opcional para autocalificación)</span>
                      </label>
                      <select v-model="question.correct_answer" class="select select-bordered select-sm">
                        <option value="">Sin respuesta correcta definida</option>
                        <option v-for="(opt, i) in question.options" :key="i" :value="i">
                          Opción {{ i + 1 }}: {{ opt }}
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

            <!-- Estado -->
            <div class="form-control">
              <label class="label cursor-pointer">
                <span class="label-text font-bold">Evaluación activa</span>
                <input v-model="form.is_active" type="checkbox" class="checkbox checkbox-primary" />
              </label>
            </div>

            <div v-if="hasResponses" class="alert alert-warning mt-6">
              <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <div>
                <h3 class="font-bold">Advertencia</h3>
                <div class="text-xs">
                  Esta evaluación ya tiene respuestas de estudiantes. Los cambios pueden afectar la consistencia de los datos.
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
                <span v-else>Guardar Cambios</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAssessmentStore } from '../../stores/assessments';
import AppLayout from '../../components/layout/AppLayout.vue';

const route = useRoute();
const router = useRouter();
const assessmentStore = useAssessmentStore();

const loading = ref(true);
const hasResponses = ref(false);
const form = ref({
  assessment_type: '',
  title: '',
  description: '',
  time_limit: null,
  questions: [],
  is_active: false,
});

const error = ref(null);

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
    await assessmentStore.updateAssessment(
      route.params.courseId,
      route.params.assessmentId,
      form.value
    );
    router.push(`/instructor/courses/${route.params.courseId}/assessments`);
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al actualizar la evaluación';
  }
};

onMounted(async () => {
  try {
    loading.value = true;
    const assessment = await assessmentStore.fetchAssessment(
      route.params.courseId,
      route.params.assessmentId
    );

    // Cargar datos en el formulario
    form.value = {
      assessment_type: assessment.assessment_type,
      title: assessment.title,
      description: assessment.description || '',
      time_limit: assessment.time_limit,
      questions: JSON.parse(JSON.stringify(assessment.questions || [])),
      is_active: assessment.is_active,
    };

    // Verificar si hay respuestas
    hasResponses.value = assessment.responses && assessment.responses.length > 0;
  } catch (err) {
    error.value = 'Error al cargar la evaluación';
    console.error(err);
  } finally {
    loading.value = false;
  }
});
</script>
