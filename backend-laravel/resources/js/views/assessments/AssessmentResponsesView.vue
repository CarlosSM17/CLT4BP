<template>
  <AppLayout>
    <div class="container mx-auto">
      <div class="flex items-center mb-8">
        <router-link :to="`/instructor/courses/${route.params.courseId}/assessments`" class="btn btn-ghost btn-circle mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </router-link>
        <div>
          <h1 class="text-4xl font-bold">Respuestas de Evaluación</h1>
          <p class="text-gray-600">{{ assessment?.title }}</p>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-8">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <!-- Estadísticas -->
      <div v-else-if="stats" class="mb-8">
        <div class="stats shadow w-full">
          <div class="stat">
            <div class="stat-title">Total Respuestas</div>
            <div class="stat-value text-primary">{{ stats.total }}</div>
          </div>

          <div class="stat">
            <div class="stat-title">Completadas</div>
            <div class="stat-value text-success">{{ stats.completed }}</div>
            <div class="stat-desc">{{ completionPercentage }}%</div>
          </div>

          <div class="stat">
            <div class="stat-title">Promedio Calificación</div>
            <div class="stat-value text-secondary">{{ stats.average_score?.toFixed(1) || 0 }}%</div>
          </div>

          <div class="stat">
            <div class="stat-title">Tiempo Promedio</div>
            <div class="stat-value text-info text-2xl">{{ formatTime(stats.average_time) }}</div>
          </div>
        </div>
      </div>

      <!-- Lista de respuestas -->
      <div v-if="responses && responses.length > 0" class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title mb-4">Respuestas de Estudiantes</h2>

          <div class="overflow-x-auto">
            <table class="table table-zebra">
              <thead>
                <tr>
                  <th>Estudiante</th>
                  <th>Email</th>
                  <th>Estado</th>
                  <th>Calificación</th>
                  <th>Tiempo</th>
                  <th>Fecha Completado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="response in responses" :key="response.id">
                  <td>{{ response.student?.name }}</td>
                  <td>{{ response.student?.email }}</td>
                  <td>
                    <span class="badge" :class="response.completed_at ? 'badge-success' : 'badge-warning'">
                      {{ response.completed_at ? 'Completada' : 'En progreso' }}
                    </span>
                  </td>
                  <td>
                    <span v-if="response.score !== null" class="font-bold">
                      {{ response.score.toFixed(1) }}%
                    </span>
                    <span v-else class="text-gray-500">-</span>
                  </td>
                  <td>{{ formatTime(response.time_spent) }}</td>
                  <td>{{ formatDate(response.completed_at) }}</td>
                  <td>
                    <button
                      @click="viewResponse(response)"
                      class="btn btn-sm btn-info"
                    >
                      Ver Detalles
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-16">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 mx-auto text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="text-xl font-bold mt-4">No hay respuestas</h3>
        <p class="text-gray-600 mt-2">Ningún estudiante ha respondido esta evaluación aún</p>
      </div>
    </div>

    <!-- Modal de detalles -->
    <dialog ref="detailsModal" class="modal">
      <div class="modal-box max-w-4xl">
        <h3 class="font-bold text-lg mb-4">Respuestas de {{ selectedResponse?.student?.name }}</h3>

        <div v-if="selectedResponse && assessment" class="space-y-4">
          <div v-for="(question, index) in assessment.questions" :key="question.id" class="card bg-base-200">
            <div class="card-body">
              <h4 class="font-bold">Pregunta {{ index + 1 }}</h4>
              <p class="mb-2">{{ question.question }}</p>

              <div class="bg-base-100 p-4 rounded">
                <p class="font-semibold text-sm text-gray-600 mb-1">Respuesta:</p>
                <p v-if="question.type === 'multiple_choice'">
                  {{ question.options[selectedResponse.responses[question.id]] || 'Sin respuesta' }}
                </p>
                <p v-else>
                  {{ selectedResponse.responses[question.id] || 'Sin respuesta' }}
                </p>

                <!-- Mostrar si es correcta (si tiene respuesta correcta definida) -->
                <div v-if="question.correct_answer !== undefined && question.correct_answer !== ''" class="mt-2">
                  <span
                    class="badge"
                    :class="selectedResponse.responses[question.id] == question.correct_answer ? 'badge-success' : 'badge-error'"
                  >
                    {{ selectedResponse.responses[question.id] == question.correct_answer ? 'Correcta' : 'Incorrecta' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-action">
          <button @click="closeDetailsModal" class="btn">Cerrar</button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>close</button>
      </form>
    </dialog>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAssessmentStore } from '../../stores/assessments';
import AppLayout from '../../components/layout/AppLayout.vue';

const route = useRoute();
const assessmentStore = useAssessmentStore();

const assessment = ref(null);
const responses = ref([]);
const stats = ref(null);
const loading = ref(true);
const selectedResponse = ref(null);
const detailsModal = ref(null);

const completionPercentage = computed(() => {
  if (!stats.value || stats.value.total === 0) return 0;
  return ((stats.value.completed / stats.value.total) * 100).toFixed(1);
});

const formatTime = (seconds) => {
  if (!seconds) return '-';
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}m ${secs}s`;
};

const formatDate = (date) => {
  if (!date) return '-';
  return new Date(date).toLocaleString('es-MX', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const viewResponse = (response) => {
  selectedResponse.value = response;
  detailsModal.value.showModal();
};

const closeDetailsModal = () => {
  detailsModal.value.close();
  selectedResponse.value = null;
};

onMounted(async () => {
  try {
    loading.value = true;

    // Cargar evaluación
    assessment.value = await assessmentStore.fetchAssessment(route.params.courseId, route.params.assessmentId);

    // Cargar respuestas
    const data = await assessmentStore.getAssessmentResponses(route.params.courseId, route.params.assessmentId);
    responses.value = data.responses;
    stats.value = data.stats;
  } catch (error) {
    console.error('Error al cargar respuestas:', error);
  } finally {
    loading.value = false;
  }
});
</script>
