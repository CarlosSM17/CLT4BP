<template>
  <AppLayout>
    <div class="container mx-auto">
      <!-- Header -->
      <div class="flex justify-between items-start mb-8">
        <div class="flex items-center">
          <router-link :to="`/instructor/courses/${courseId}`" class="btn btn-ghost btn-circle mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </router-link>
          <div>
            <h1 class="text-3xl font-bold">Recolección de Datos</h1>
            <p class="text-gray-600 mt-1">Estado de evaluaciones finales y comparación pre/post</p>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-16">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="alert alert-error shadow-lg mb-6">
        <span>{{ error }}</span>
      </div>

      <!-- Content -->
      <div v-else>
        <!-- Tabs -->
        <div class="tabs tabs-boxed mb-6">
          <a class="tab" :class="{ 'tab-active': activeTab === 'completion' }" @click="switchTab('completion')">
            Estado de Completitud
          </a>
          <a class="tab" :class="{ 'tab-active': activeTab === 'prepost' }" @click="switchTab('prepost')">
            Comparación Pre/Post
          </a>
          <a class="tab" :class="{ 'tab-active': activeTab === 'export' }" @click="switchTab('export')">
            Exportar Datos
          </a>
        </div>

        <!-- Tab 1: Completion Status -->
        <div v-if="activeTab === 'completion' && summary">
          <!-- Summary Stats -->
          <div class="stats shadow w-full mb-6">
            <div class="stat">
              <div class="stat-title">Estudiantes</div>
              <div class="stat-value">{{ summary.total_students }}</div>
            </div>
            <div class="stat">
              <div class="stat-title">Tipos de Evaluación</div>
              <div class="stat-value">{{ summary.assessment_types.length }}</div>
            </div>
            <div class="stat">
              <div class="stat-title">Completitud Promedio</div>
              <div class="stat-value text-lg">{{ averageCompletion }}%</div>
            </div>
          </div>

          <!-- Completion Rates -->
          <div class="card bg-base-100 shadow mb-6">
            <div class="card-body">
              <h3 class="card-title text-lg mb-4">Tasa de Completitud por Evaluación</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="type in summary.assessment_types" :key="type" class="flex flex-col gap-1">
                  <div class="flex justify-between text-sm">
                    <span class="font-medium">{{ getTypeLabel(type) }}</span>
                    <span>{{ summary.completion_rates[type] }}%</span>
                  </div>
                  <progress
                    class="progress w-full"
                    :class="getProgressColor(summary.completion_rates[type])"
                    :value="summary.completion_rates[type]"
                    max="100"
                  ></progress>
                </div>
              </div>
            </div>
          </div>

          <!-- Student Matrix -->
          <div class="card bg-base-100 shadow">
            <div class="card-body">
              <h3 class="card-title text-lg mb-4">Matriz de Completitud por Estudiante</h3>
              <div class="overflow-x-auto">
                <table class="table table-sm">
                  <thead>
                    <tr>
                      <th>Estudiante</th>
                      <th v-for="type in summary.assessment_types" :key="type" class="text-center text-xs">
                        {{ getTypeShortLabel(type) }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="student in summary.students" :key="student.id">
                      <td>
                        <button class="link link-primary text-sm" @click="viewStudentDetail(student.id)">
                          {{ student.name }}
                        </button>
                      </td>
                      <td v-for="type in summary.assessment_types" :key="type" class="text-center">
                        <div v-if="student.assessments[type]?.completed" class="tooltip" :data-tip="'Score: ' + (student.assessments[type].score ?? 'N/A')">
                          <span class="badge badge-success badge-sm">
                            {{ student.assessments[type].score !== null ? Math.round(student.assessments[type].score) + '%' : '✓' }}
                          </span>
                        </div>
                        <span v-else class="badge badge-error badge-sm badge-outline">—</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab 2: Pre/Post Comparison -->
        <div v-if="activeTab === 'prepost'">
          <div v-if="loadingPrePost" class="flex justify-center py-8">
            <span class="loading loading-spinner loading-lg"></span>
          </div>
          <div v-else-if="prePostData">
            <div v-for="pair in prePostData.pairs" :key="pair.initial_type" class="card bg-base-100 shadow mb-6">
              <div class="card-body">
                <h3 class="card-title">{{ pair.label }}</h3>

                <!-- Averages -->
                <div v-if="pair.averages.initial !== null" class="stats shadow mb-4">
                  <div class="stat">
                    <div class="stat-title">Promedio Inicial</div>
                    <div class="stat-value text-lg">{{ pair.averages.initial }}</div>
                  </div>
                  <div class="stat">
                    <div class="stat-title">Promedio Final</div>
                    <div class="stat-value text-lg">{{ pair.averages.final }}</div>
                  </div>
                  <div class="stat">
                    <div class="stat-title">Cambio Promedio</div>
                    <div class="stat-value text-lg" :class="pair.averages.change >= 0 ? 'text-success' : 'text-error'">
                      {{ pair.averages.change >= 0 ? '+' : '' }}{{ pair.averages.change }}
                    </div>
                  </div>
                </div>

                <!-- No data message -->
                <div v-if="pair.students.length === 0" class="alert alert-warning">
                  <span>No hay estudiantes con ambas evaluaciones completadas para esta comparación.</span>
                </div>

                <!-- Student comparison table -->
                <div v-else class="overflow-x-auto">
                  <table class="table table-sm">
                    <thead>
                      <tr>
                        <th>Estudiante</th>
                        <th class="text-center">Score Inicial</th>
                        <th class="text-center">Score Final</th>
                        <th class="text-center">Cambio</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="student in pair.students" :key="student.id">
                        <td>{{ student.name }}</td>
                        <td class="text-center">{{ student.initial_score ?? 'N/A' }}</td>
                        <td class="text-center">{{ student.final_score ?? 'N/A' }}</td>
                        <td class="text-center">
                          <span
                            v-if="student.change !== null"
                            class="badge badge-sm"
                            :class="student.change >= 0 ? 'badge-success' : 'badge-error'"
                          >
                            {{ student.change >= 0 ? '+' : '' }}{{ student.change }}
                          </span>
                          <span v-else>—</span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab 3: Export -->
        <div v-if="activeTab === 'export'">
          <div class="card bg-base-100 shadow">
            <div class="card-body">
              <h3 class="card-title mb-4">Exportar Datos del Curso</h3>
              <p class="text-gray-600 mb-6">
                Descarga todos los datos de evaluaciones del curso en formato CSV. Incluye: estudiante, tipo de evaluación, score, tiempo, fecha de completitud y estado de calificación.
              </p>
              <div class="flex gap-4">
                <button class="btn btn-primary" @click="exportCsv" :disabled="exporting">
                  <svg v-if="exporting" class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ exporting ? 'Descargando...' : 'Descargar CSV' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Data preview -->
          <div v-if="summary" class="card bg-base-100 shadow mt-6">
            <div class="card-body">
              <h3 class="card-title text-lg mb-4">Vista Previa de Datos</h3>
              <div class="overflow-x-auto">
                <table class="table table-xs">
                  <thead>
                    <tr>
                      <th>Estudiante</th>
                      <th>Evaluaciones Completadas</th>
                      <th>Score Promedio</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="student in summary.students" :key="student.id">
                      <td>{{ student.name }}</td>
                      <td>
                        {{ getCompletedCount(student) }} / {{ summary.assessment_types.length }}
                      </td>
                      <td>{{ getAverageScore(student) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Student Detail Modal -->
      <dialog ref="studentModal" class="modal">
        <div class="modal-box max-w-3xl">
          <h3 class="font-bold text-lg mb-4">
            Detalle del Estudiante: {{ studentDetail?.student?.name }}
          </h3>

          <div v-if="loadingStudent" class="flex justify-center py-8">
            <span class="loading loading-spinner loading-lg"></span>
          </div>

          <div v-else-if="studentDetail">
            <!-- Assessments -->
            <h4 class="font-semibold mb-2">Evaluaciones</h4>
            <div class="overflow-x-auto mb-4">
              <table class="table table-sm">
                <thead>
                  <tr>
                    <th>Evaluación</th>
                    <th>Estado</th>
                    <th>Score</th>
                    <th>Fecha</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="a in studentDetail.assessments" :key="a.assessment_type">
                    <td>{{ getTypeLabel(a.assessment_type) }}</td>
                    <td>
                      <span class="badge badge-sm" :class="a.completed ? 'badge-success' : 'badge-error'">
                        {{ a.completed ? 'Completado' : 'Pendiente' }}
                      </span>
                    </td>
                    <td>{{ formatScore(a) }}</td>
                    <td>{{ a.completed_at ? formatDate(a.completed_at) : '—' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Material Access -->
            <h4 class="font-semibold mb-2">Acceso a Materiales</h4>
            <div v-if="studentDetail.material_access.length > 0">
              <p class="text-sm text-gray-600 mb-2">
                Tiempo total de estudio: {{ Math.round(studentDetail.total_study_time / 60) }} minutos
              </p>
              <div class="overflow-x-auto">
                <table class="table table-xs">
                  <thead>
                    <tr>
                      <th>Tipo</th>
                      <th>Tema</th>
                      <th>Tiempo</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(access, idx) in studentDetail.material_access" :key="idx">
                      <td>{{ access.material_type }}</td>
                      <td>{{ access.topic || '—' }}</td>
                      <td>{{ access.time_spent_seconds ? Math.round(access.time_spent_seconds / 60) + ' min' : 'En curso' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <p v-else class="text-sm text-gray-400">Sin accesos a materiales registrados.</p>
          </div>

          <div class="modal-action">
            <form method="dialog">
              <button class="btn">Cerrar</button>
            </form>
          </div>
        </div>
        <form method="dialog" class="modal-backdrop">
          <button>close</button>
        </form>
      </dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import AppLayout from '../../components/layout/AppLayout.vue';
import api from '../../services/api';

const route = useRoute();
const courseId = computed(() => parseInt(route.params.courseId));

const loading = ref(true);
const error = ref(null);
const activeTab = ref('completion');

const summary = ref(null);
const prePostData = ref(null);
const loadingPrePost = ref(false);
const exporting = ref(false);

const studentDetail = ref(null);
const loadingStudent = ref(false);
const studentModal = ref(null);

const LIKERT_MAX = {
  mslq_motivation_initial: 7,
  mslq_motivation_final:   7,
  mslq_strategies:         7,
  cognitive_load:          10,
  course_interest:         5,
  imms:                    5,
};

const formatScore = (assessment) => {
  if (assessment.score === null || assessment.score === undefined) return '—';
  if (assessment.score_type === 'likert') {
    const max = LIKERT_MAX[assessment.assessment_type] ?? 10;
    return Number(assessment.score).toFixed(1) + ' / ' + max;
  }
  return Math.round(assessment.score) + '%';
};

const TYPE_LABELS = {
  recall_initial: 'Recuerdo Inicial',
  comprehension_initial: 'Comprensión Inicial',
  mslq_motivation_initial: 'MSLQ Motivación Inicial',
  mslq_strategies: 'MSLQ Estrategias',
  prior_knowledge: 'Conocimiento Previo',
  cognitive_load: 'Carga Cognitiva',
  recall_final: 'Recuerdo Final',
  comprehension_final: 'Comprensión Final',
  mslq_motivation_final: 'MSLQ Motivación Final',
  course_interest: 'Interés en el Curso (CIS)',
  imms: 'IMMS',
};

const TYPE_SHORT_LABELS = {
  recall_initial: 'Rec. Ini.',
  comprehension_initial: 'Comp. Ini.',
  mslq_motivation_initial: 'MSLQ Mot.',
  mslq_strategies: 'MSLQ Est.',
  prior_knowledge: 'Con. Prev.',
  cognitive_load: 'Carga Cog.',
  recall_final: 'Rec. Fin.',
  comprehension_final: 'Comp. Fin.',
  mslq_motivation_final: 'MSLQ Fin.',
  course_interest: 'CIS',
  imms: 'IMMS',
};

const getTypeLabel = (type) => TYPE_LABELS[type] || type;
const getTypeShortLabel = (type) => TYPE_SHORT_LABELS[type] || type;

const getProgressColor = (rate) => {
  if (rate >= 80) return 'progress-success';
  if (rate >= 50) return 'progress-warning';
  return 'progress-error';
};

const averageCompletion = computed(() => {
  if (!summary.value || summary.value.assessment_types.length === 0) return 0;
  const rates = Object.values(summary.value.completion_rates);
  return Math.round(rates.reduce((a, b) => a + b, 0) / rates.length);
});

const getCompletedCount = (student) => {
  return Object.values(student.assessments).filter(a => a.completed).length;
};

const getAverageScore = (student) => {
  const scores = Object.values(student.assessments)
    .filter(a => a.completed && a.score !== null)
    .map(a => a.score);
  if (scores.length === 0) return 'N/A';
  return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) + '%';
};

const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('es-MX', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
};

const switchTab = (tab) => {
  activeTab.value = tab;
  if (tab === 'prepost' && !prePostData.value) {
    loadPrePostComparison();
  }
};

const loadSummary = async () => {
  try {
    loading.value = true;
    error.value = null;
    const response = await api.get(`/courses/${courseId.value}/data-collection/summary`);
    summary.value = response.data;
  } catch (err) {
    error.value = 'Error al cargar datos: ' + (err.response?.data?.message || err.message);
  } finally {
    loading.value = false;
  }
};

const loadPrePostComparison = async () => {
  try {
    loadingPrePost.value = true;
    const response = await api.get(`/courses/${courseId.value}/data-collection/pre-post-comparison`);
    prePostData.value = response.data;
  } catch (err) {
    console.error('Error al cargar comparación:', err);
  } finally {
    loadingPrePost.value = false;
  }
};

const exportCsv = async () => {
  try {
    exporting.value = true;
    const response = await api.get(`/courses/${courseId.value}/data-collection/export`, {
      responseType: 'blob',
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `datos_curso_${courseId.value}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (err) {
    console.error('Error al exportar:', err);
    alert('Error al exportar datos: ' + (err.response?.data?.message || err.message));
  } finally {
    exporting.value = false;
  }
};

const viewStudentDetail = async (studentId) => {
  try {
    loadingStudent.value = true;
    studentDetail.value = null;
    studentModal.value?.showModal();
    const response = await api.get(`/courses/${courseId.value}/data-collection/student/${studentId}`);
    studentDetail.value = response.data;
  } catch (err) {
    console.error('Error al cargar detalle:', err);
  } finally {
    loadingStudent.value = false;
  }
};

onMounted(() => {
  loadSummary();
});
</script>
