<!-- src/views/instructor/GradingDashboard.vue -->
<template>
  <AppLayout>
    <div class="container mx-auto p-6">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-3xl font-bold">Calificaciones Pendientes</h1>
          <p class="text-gray-600 mt-1">
            Curso: {{ courseName }}
          </p>
        </div>

        <router-link
          :to="`/instructor/courses/${courseId}`"
          class="btn btn-outline"
        >
          Volver al Curso
        </router-link>
      </div>

      <!-- Resumen general -->
      <div class="stats shadow mb-6 w-full">
        <div class="stat">
          <div class="stat-title">Total Pendientes</div>
          <div class="stat-value text-primary">{{ gradingSummary.total_pending || 0 }}</div>
          <div class="stat-desc">Respuestas por calificar</div>
        </div>
        <div class="stat">
          <div class="stat-title">Evaluaciones</div>
          <div class="stat-value">{{ gradingSummary.assessments?.length || 0 }}</div>
          <div class="stat-desc">Con respuestas pendientes</div>
        </div>
      </div>

      <!-- Lista de evaluaciones con pendientes -->
      <div v-if="loading" class="flex justify-center py-12">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <div v-else-if="gradingSummary.assessments?.length === 0" class="space-y-4">
        <div class="alert alert-success">
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>No hay respuestas pendientes de calificación en este curso.</span>
        </div>

        <div class="alert alert-info">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <div>
            <span>Si hay evaluaciones con preguntas abiertas y respuestas completadas, puedes recalcular los estados.</span>
          </div>
          <button
            class="btn btn-sm btn-primary"
            :disabled="recalculating"
            @click="recalculateGradingStatus"
          >
            <span v-if="recalculating" class="loading loading-spinner loading-sm"></span>
            {{ recalculating ? 'Recalculando...' : 'Recalcular Estados' }}
          </button>
        </div>
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="assessment in gradingSummary.assessments"
          :key="assessment.id"
          class="card bg-base-100 shadow-xl"
        >
          <div class="card-body">
            <div class="flex justify-between items-start">
              <div>
                <h2 class="card-title">{{ assessment.title }}</h2>
                <p class="text-sm text-gray-600">
                  Tipo: {{ formatAssessmentType(assessment.assessment_type) }}
                </p>
              </div>
              <div class="badge badge-lg badge-warning">
                {{ assessment.pending_count }} pendientes
              </div>
            </div>

            <div class="card-actions justify-end mt-4">
              <button
                class="btn btn-primary"
                @click="viewPendingResponses(assessment)"
              >
                Ver Respuestas Pendientes
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal para ver respuestas pendientes -->
      <div v-if="selectedAssessment" class="modal modal-open">
        <div class="modal-box max-w-5xl">
          <button
            class="btn btn-sm btn-circle absolute right-2 top-2"
            @click="closeModal"
          >
            X
          </button>

          <h2 class="font-bold text-xl mb-4">
            {{ selectedAssessment.title }} - Respuestas Pendientes
          </h2>

          <!-- Estadísticas de calificación -->
          <div class="stats shadow mb-4 w-full">
            <div class="stat">
              <div class="stat-title">Completadas</div>
              <div class="stat-value text-sm">{{ gradingStats.total_completed || 0 }}</div>
            </div>
            <div class="stat">
              <div class="stat-title">Auto-calificadas</div>
              <div class="stat-value text-sm text-success">{{ gradingStats.auto_graded || 0 }}</div>
            </div>
            <div class="stat">
              <div class="stat-title">Pendientes</div>
              <div class="stat-value text-sm text-warning">{{ gradingStats.pending_grading || 0 }}</div>
            </div>
            <div class="stat">
              <div class="stat-title">Calificadas</div>
              <div class="stat-value text-sm text-primary">{{ gradingStats.graded || 0 }}</div>
            </div>
          </div>

          <!-- Lista de respuestas pendientes -->
          <div v-if="loadingResponses" class="flex justify-center py-8">
            <span class="loading loading-spinner loading-md"></span>
          </div>

          <div v-else-if="pendingResponses.length === 0" class="alert alert-info">
            No hay respuestas pendientes de calificación.
          </div>

          <div v-else class="overflow-x-auto">
            <table class="table">
              <thead>
                <tr>
                  <th>Estudiante</th>
                  <th>Email</th>
                  <th>Completado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="response in pendingResponses" :key="response.id">
                  <td>{{ response.student?.name }}</td>
                  <td>{{ response.student?.email }}</td>
                  <td>{{ formatDate(response.completed_at) }}</td>
                  <td>
                    <button
                      class="btn btn-sm btn-primary"
                      @click="gradeResponse(response)"
                    >
                      Calificar
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="modal-action">
            <button class="btn" @click="closeModal">Cerrar</button>
          </div>
        </div>
        <div class="modal-backdrop bg-black/50" @click="closeModal"></div>
      </div>

      <!-- Modal para calificar respuesta individual -->
      <div v-if="responseToGrade" class="modal modal-open">
        <div class="modal-box max-w-4xl max-h-[90vh] overflow-y-auto">
          <button
            class="btn btn-sm btn-circle absolute right-2 top-2"
            @click="closeGradingModal"
          >
            X
          </button>

          <h2 class="font-bold text-xl mb-2">
            Calificar Respuesta
          </h2>
          <p class="text-gray-600 mb-4">
            Estudiante: {{ responseToGrade.student?.name }}
          </p>

          <!-- Preguntas abiertas para calificar -->
          <div class="space-y-6">
            <div
              v-for="(item, index) in openEndedDetails"
              :key="item.question.id"
              class="card bg-base-200"
            >
              <div class="card-body">
                <h3 class="font-semibold">
                  Pregunta {{ index + 1 }}: {{ item.question.question }}
                </h3>

                <div class="bg-base-100 p-4 rounded-lg mt-2">
                  <p class="text-sm text-gray-600 mb-1">Respuesta del estudiante:</p>
                  <p class="whitespace-pre-wrap">{{ item.student_answer || 'Sin respuesta' }}</p>
                </div>

                <div class="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <label class="label">
                      <span class="label-text">Puntaje</span>
                    </label>
                    <input
                      type="number"
                      v-model.number="grades[item.question.id].score"
                      :min="0"
                      :max="grades[item.question.id].max_score"
                      class="input input-bordered w-full"
                    />
                  </div>
                  <div>
                    <label class="label">
                      <span class="label-text">Puntaje Máximo</span>
                    </label>
                    <input
                      type="number"
                      v-model.number="grades[item.question.id].max_score"
                      min="1"
                      class="input input-bordered w-full"
                    />
                  </div>
                </div>

                <div class="mt-2">
                  <label class="label">
                    <span class="label-text">Retroalimentación (opcional)</span>
                  </label>
                  <textarea
                    v-model="grades[item.question.id].feedback"
                    class="textarea textarea-bordered w-full"
                    rows="2"
                    placeholder="Escribe retroalimentación para el estudiante..."
                  ></textarea>
                </div>
              </div>
            </div>
          </div>

          <div v-if="gradingError" class="alert alert-error mt-4">
            <span>{{ gradingError }}</span>
          </div>

          <div class="modal-action">
            <button class="btn" @click="closeGradingModal">Cancelar</button>
            <button
              class="btn btn-primary"
              :disabled="submittingGrade"
              @click="submitGrade"
            >
              <span v-if="submittingGrade" class="loading loading-spinner loading-sm"></span>
              {{ submittingGrade ? 'Guardando...' : 'Guardar Calificación' }}
            </button>
          </div>
        </div>
        <div class="modal-backdrop bg-black/50" @click="closeGradingModal"></div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';
import { useRoute } from 'vue-router';
import AppLayout from '@/components/layout/AppLayout.vue';
import axios from 'axios';

const route = useRoute();

const courseId = computed(() => route.params.courseId);
const courseName = ref('');

const loading = ref(true);
const loadingResponses = ref(false);
const submittingGrade = ref(false);
const recalculating = ref(false);

const gradingSummary = ref({ total_pending: 0, assessments: [] });
const selectedAssessment = ref(null);
const pendingResponses = ref([]);
const gradingStats = ref({});
const openEndedQuestions = ref([]);

const responseToGrade = ref(null);
const openEndedDetails = ref([]);
const grades = reactive({});
const gradingError = ref(null);

const loadCoursePendingGrading = async () => {
  try {
    loading.value = true;
    const response = await axios.get(
      `/api/courses/${courseId.value}/pending-grading`
    );
    gradingSummary.value = response.data.grading_summary;
    courseName.value = response.data.course?.title || '';
  } catch (error) {
    console.error('Error al cargar resumen de calificaciones:', error);
  } finally {
    loading.value = false;
  }
};

const viewPendingResponses = async (assessment) => {
  selectedAssessment.value = assessment;
  loadingResponses.value = true;

  try {
    const response = await axios.get(
      `/api/courses/${courseId.value}/assessments/${assessment.id}/pending-grading`
    );
    pendingResponses.value = response.data.pending_responses;
    gradingStats.value = response.data.stats;
    openEndedQuestions.value = response.data.open_ended_questions;
  } catch (error) {
    console.error('Error al cargar respuestas pendientes:', error);
  } finally {
    loadingResponses.value = false;
  }
};

const gradeResponse = async (response) => {
  try {
    const result = await axios.get(
      `/api/courses/${courseId.value}/assessments/${selectedAssessment.value.id}/responses/${response.id}/grading`
    );

    responseToGrade.value = result.data.response;
    openEndedDetails.value = result.data.open_ended_details;

    // Inicializar grades con los datos existentes o valores por defecto
    openEndedDetails.value.forEach(item => {
      const existingScore = item.manual_score;
      grades[item.question.id] = {
        question_id: item.question.id,
        score: existingScore?.score ?? 0,
        max_score: existingScore?.max_score ?? 10,
        feedback: existingScore?.feedback ?? ''
      };
    });

    gradingError.value = null;
  } catch (error) {
    console.error('Error al cargar respuesta para calificar:', error);
  }
};

const submitGrade = async () => {
  submittingGrade.value = true;
  gradingError.value = null;

  try {
    const gradesArray = Object.values(grades);

    // Validar que todos los puntajes estén dentro del rango
    for (const grade of gradesArray) {
      if (grade.score < 0 || grade.score > grade.max_score) {
        gradingError.value = `El puntaje debe estar entre 0 y ${grade.max_score}`;
        submittingGrade.value = false;
        return;
      }
    }

    await axios.post(
      `/api/courses/${courseId.value}/assessments/${selectedAssessment.value.id}/responses/${responseToGrade.value.id}/grade`,
      { grades: gradesArray }
    );

    // Cerrar modal y recargar datos
    closeGradingModal();
    await viewPendingResponses(selectedAssessment.value);
    await loadCoursePendingGrading();

  } catch (error) {
    console.error('Error al guardar calificación:', error);
    gradingError.value = error.response?.data?.message || 'Error al guardar la calificación';
  } finally {
    submittingGrade.value = false;
  }
};

const closeModal = () => {
  selectedAssessment.value = null;
  pendingResponses.value = [];
  gradingStats.value = {};
};

const closeGradingModal = () => {
  responseToGrade.value = null;
  openEndedDetails.value = [];
  Object.keys(grades).forEach(key => delete grades[key]);
  gradingError.value = null;
};

const formatAssessmentType = (type) => {
  const types = {
    'mslq_motivation_initial': 'MSLQ Motivación (Inicial)',
    'mslq_strategies': 'MSLQ Estrategias',
    'prior_knowledge': 'Conocimiento Previo',
    'custom': 'Personalizado'
  };
  return types[type] || type;
};

const formatDate = (date) => {
  if (!date) return 'N/A';
  return new Date(date).toLocaleString('es-MX', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const recalculateGradingStatus = async () => {
  recalculating.value = true;
  try {
    const response = await axios.post(
      `/api/courses/${courseId.value}/recalculate-grading`
    );
    alert(response.data.message);
    await loadCoursePendingGrading();
  } catch (error) {
    console.error('Error al recalcular estados:', error);
    alert('Error al recalcular estados de calificación');
  } finally {
    recalculating.value = false;
  }
};

onMounted(() => {
  loadCoursePendingGrading();
});
</script>
