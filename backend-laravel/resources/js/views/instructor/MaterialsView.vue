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
            <h1 class="text-3xl font-bold">Material Instruccional con IA</h1>
            <p class="text-gray-600 mt-1">Genera material personalizado usando Claude API</p>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-8">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <!-- Error: No hay efectos CLT seleccionados -->
      <div v-else-if="!cltSelection" class="alert alert-warning shadow-lg">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div>
          <h3 class="font-bold">Se requiere seleccion de efectos CLT</h3>
          <div class="text-sm">
            Antes de generar material, debes seleccionar los efectos CLT que se aplicaran.
          </div>
        </div>
        <router-link :to="`/instructor/courses/${courseId}/clt-effects`" class="btn btn-sm">
          Seleccionar Efectos CLT
        </router-link>
      </div>

      <!-- Contenido principal -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Panel de generacion -->
        <div class="lg:col-span-2">
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title">Generar Nuevo Material</h2>

              <!-- Info de efectos CLT seleccionados -->
              <div class="alert alert-info mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <div>
                  <span class="font-semibold">{{ cltSelection.selected_effects.length }}</span> efectos CLT seleccionados
                  <router-link :to="`/instructor/courses/${courseId}/clt-effects`" class="link link-hover ml-2">
                    (modificar)
                  </router-link>
                </div>
              </div>

              <!-- Formulario de configuracion -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Tipo de Material *</span>
                  </label>
                  <select class="select select-bordered" v-model="materialConfig.material_type">
                    <option value="">Selecciona un tipo</option>
                    <option value="example">Ejemplo Real</option>
                    <option value="learning_tasks">Tareas de Aprendizaje</option>
                    <option value="support_info">Informacion de Soporte</option>
                    <option value="procedural_info">Informacion Procedimental</option>
                    <option value="verbal_protocols">Protocolos Verbales</option>
                  </select>
                  <label class="label">
                    <span class="label-text-alt text-gray-500">
                      {{ getMaterialTypeDescription(materialConfig.material_type) }}
                    </span>
                  </label>
                </div>

                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Tipo de Perfil *</span>
                  </label>
                  <select class="select select-bordered" v-model="materialConfig.profile_type">
                    <option value="group">Perfil Grupal</option>
                    <option value="individual">Perfil Individual</option>
                  </select>
                </div>

                <div class="form-control" v-if="materialConfig.profile_type === 'individual'">
                  <label class="label">
                    <span class="label-text font-semibold">Estudiante *</span>
                  </label>
                  <select class="select select-bordered" v-model="materialConfig.student_id">
                    <option value="">Selecciona un estudiante</option>
                    <option v-for="student in students" :key="student.id" :value="student.id">
                      {{ student.name }}
                    </option>
                  </select>
                </div>

                <div class="form-control" :class="materialConfig.profile_type === 'individual' ? '' : 'md:col-span-2'">
                  <label class="label">
                    <span class="label-text font-semibold">Tema del Material *</span>
                  </label>
                  <input
                    type="text"
                    class="input input-bordered"
                    v-model="materialConfig.topic"
                    placeholder="Ej: Variables y tipos de datos en Python"
                  />
                </div>

                <div class="form-control md:col-span-2">
                  <label class="label">
                    <span class="label-text font-semibold">Contexto Adicional (opcional)</span>
                  </label>
                  <textarea
                    class="textarea textarea-bordered"
                    rows="3"
                    v-model="materialConfig.additional_context"
                    placeholder="Informacion adicional o instrucciones especificas para la generacion..."
                  ></textarea>
                </div>
              </div>

              <div class="card-actions justify-end mt-4">
                <button
                  class="btn btn-primary"
                  @click="generateMaterial"
                  :disabled="!canGenerate || generating"
                >
                  <svg v-if="generating" class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  {{ generating ? 'Generando con IA...' : 'Generar Material' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Material generado -->
          <div class="card bg-base-100 shadow-xl mt-6" v-if="generatedMaterial">
            <div class="card-body">
              <h2 class="card-title">
                Material Generado
                <div class="badge badge-success">Exitoso</div>
              </h2>
              <div class="alert alert-success mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <div class="font-bold">Material generado y guardado exitosamente</div>
                  <div class="text-sm">
                    Tokens utilizados: {{ generatedMaterial.token_usage?.total_tokens || 'N/A' }}
                  </div>
                </div>
              </div>
              <div class="bg-base-200 p-4 rounded-lg max-h-96 overflow-auto">
                <h3 class="font-semibold mb-2">Contenido Generado:</h3>
                <pre class="whitespace-pre-wrap text-sm">{{ JSON.stringify(generatedMaterial.material?.content || generatedMaterial.content, null, 2) }}</pre>
              </div>
              <div class="card-actions justify-end mt-4">
                <button class="btn btn-ghost" @click="resetForm">
                  Generar Otro Material
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Panel lateral: Materiales existentes -->
        <div class="lg:col-span-1">
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title text-lg">Materiales Generados</h2>

              <div v-if="loadingMaterials" class="flex justify-center py-4">
                <span class="loading loading-spinner"></span>
              </div>

              <div v-else-if="materials.length === 0" class="text-gray-500 text-center py-4">
                No hay materiales generados aun
              </div>

              <div v-else class="space-y-3 max-h-[32rem] overflow-auto">
                <div
                  v-for="material in materials"
                  :key="material.id"
                  class="border border-base-300 rounded-lg p-3 hover:bg-base-200 cursor-pointer"
                  @click="viewMaterial(material)"
                >
                  <div class="flex justify-between items-start">
                    <div>
                      <span class="badge badge-sm" :class="getMaterialTypeBadge(material.material_type)">
                        {{ getMaterialTypeLabel(material.material_type) }}
                      </span>
                      <span class="badge badge-sm badge-ghost ml-1">
                        {{ material.target_type === 'group' ? 'Grupal' : 'Individual' }}
                      </span>
                    </div>
                  </div>
                  <!-- Toggle de activacion -->
                  <div class="flex items-center justify-between mt-2">
                    <div class="flex items-center gap-2">
                      <input
                        type="checkbox"
                        class="toggle toggle-sm toggle-success"
                        :checked="material.is_active"
                        @click.stop="toggleMaterialActive(material)"
                      />
                      <span class="text-xs" :class="material.is_active ? 'text-success' : 'text-gray-400'">
                        {{ material.is_active ? 'Activo' : 'Inactivo' }}
                      </span>
                    </div>
                    <span v-if="material.timer_seconds" class="text-xs text-gray-400">
                      {{ Math.round(material.timer_seconds / 60) }} min
                    </span>
                  </div>
                  <p class="text-xs text-gray-500 mt-1">
                    {{ formatDate(material.created_at) }}
                  </p>
                </div>
              </div>

              <button class="btn btn-sm btn-outline mt-4" @click="loadMaterials" v-if="materials.length > 0">
                Actualizar Lista
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal para ver material -->
      <dialog ref="materialModal" class="modal">
        <div class="modal-box max-w-4xl max-h-[85vh]">
          <h3 class="font-bold text-lg" v-if="selectedMaterial">
            {{ getMaterialTypeLabel(selectedMaterial.material_type) }}
            <span class="badge badge-sm ml-2">{{ selectedMaterial.target_type === 'group' ? 'Grupal' : 'Individual' }}</span>
            <span class="badge badge-sm ml-1" :class="selectedMaterial.is_active ? 'badge-success' : 'badge-ghost'">
              {{ selectedMaterial.is_active ? 'Activo' : 'Inactivo' }}
            </span>
          </h3>

          <div class="py-4" v-if="selectedMaterial">
            <!-- Timer config para support_info -->
            <div v-if="selectedMaterial.material_type === 'support_info'" class="p-3 bg-base-200 rounded-lg mb-4">
              <h4 class="font-semibold text-sm mb-2">Timer de Soporte</h4>
              <div class="flex items-center gap-3">
                <input
                  type="number"
                  class="input input-bordered input-sm w-28"
                  v-model.number="timerMinutes"
                  min="1" max="120"
                />
                <span class="text-sm">minutos</span>
                <button class="btn btn-sm btn-outline" @click="updateTimer(selectedMaterial)">
                  Guardar
                </button>
              </div>
              <p class="text-xs text-gray-500 mt-1">
                Actual: {{ selectedMaterial.timer_seconds ? Math.round(selectedMaterial.timer_seconds / 60) + ' min' : 'No configurado' }}
              </p>
            </div>

            <!-- Contenido del material -->
            <div class="bg-base-200 p-4 rounded-lg max-h-[50vh] overflow-auto">
              <pre class="whitespace-pre-wrap text-sm">{{ JSON.stringify(selectedMaterial.content, null, 2) }}</pre>
            </div>

            <!-- Logs de acceso -->
            <div class="mt-4">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-semibold text-sm">Logs de Acceso</h4>
                <button class="btn btn-xs btn-outline" @click="loadAccessLogs(selectedMaterial)">
                  Cargar
                </button>
              </div>
              <div v-if="accessLogs.length > 0" class="max-h-48 overflow-auto">
                <table class="table table-xs">
                  <thead>
                    <tr>
                      <th>Estudiante</th>
                      <th>Inicio</th>
                      <th>Tiempo</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="log in accessLogs" :key="log.id">
                      <td>{{ log.student?.name || 'N/A' }}</td>
                      <td>{{ formatDate(log.started_at) }}</td>
                      <td>{{ log.time_spent_seconds ? Math.round(log.time_spent_seconds / 60) + ' min' : 'En curso' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p v-else class="text-xs text-gray-400">Sin accesos registrados</p>
            </div>
          </div>

          <div class="modal-action">
            <form method="dialog">
              <button class="btn">Cerrar</button>
            </form>
          </div>
        </div>
      </dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import AppLayout from '../../components/layout/AppLayout.vue';
import { useCltEffectsStore } from '../../stores/cltEffects';
import api from '../../services/api';

const route = useRoute();
const cltStore = useCltEffectsStore();

const courseId = computed(() => parseInt(route.params.courseId));
const loading = ref(true);
const loadingMaterials = ref(false);
const generating = ref(false);

const cltSelection = ref(null);
const students = ref([]);
const materials = ref([]);
const generatedMaterial = ref(null);
const selectedMaterial = ref(null);
const materialModal = ref(null);
const timerMinutes = ref(30);
const accessLogs = ref([]);

const materialConfig = ref({
  material_type: '',
  profile_type: 'group',
  student_id: null,
  topic: '',
  additional_context: ''
});

const canGenerate = computed(() => {
  return materialConfig.value.material_type &&
         materialConfig.value.topic &&
         (materialConfig.value.profile_type === 'group' || materialConfig.value.student_id);
});

const getMaterialTypeDescription = (type) => {
  const descriptions = {
    'example': 'Ejemplo real y completo con codigo funcional',
    'learning_tasks': 'Secuencia de tareas con dificultad progresiva',
    'support_info': 'Informacion teorica y conceptual',
    'procedural_info': 'Ejemplos resueltos paso a paso',
    'verbal_protocols': 'Pensamiento en voz alta del experto'
  };
  return descriptions[type] || '';
};

const getMaterialTypeLabel = (type) => {
  const labels = {
    'example': 'Ejemplo',
    'learning_tasks': 'Tareas',
    'support_info': 'Soporte',
    'procedural_info': 'Procedimental',
    'verbal_protocols': 'Protocolo'
  };
  return labels[type] || type;
};

const getMaterialTypeBadge = (type) => {
  const badges = {
    'example': 'badge-primary',
    'learning_tasks': 'badge-secondary',
    'support_info': 'badge-accent',
    'procedural_info': 'badge-info',
    'verbal_protocols': 'badge-warning'
  };
  return badges[type] || 'badge-ghost';
};

const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('es-MX', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const generateMaterial = async () => {
  if (!canGenerate.value) return;
  try {
    generating.value = true;
    const response = await api.post(`/courses/${courseId.value}/materials/generate`, materialConfig.value);
    generatedMaterial.value = response.data.data;
    await loadMaterials();
  } catch (error) {
    console.error('Error al generar material:', error);
    alert('Error al generar material: ' + (error.response?.data?.message || error.message));
  } finally {
    generating.value = false;
  }
};

const resetForm = () => {
  materialConfig.value = {
    material_type: '',
    profile_type: 'group',
    student_id: null,
    topic: '',
    additional_context: ''
  };
  generatedMaterial.value = null;
};

const viewMaterial = (material) => {
  selectedMaterial.value = material;
  accessLogs.value = [];
  timerMinutes.value = material.timer_seconds ? Math.round(material.timer_seconds / 60) : 30;
  materialModal.value?.showModal();
};

const toggleMaterialActive = async (material) => {
  try {
    const response = await api.post(`/courses/${courseId.value}/materials/${material.id}/toggle-active`);
    const index = materials.value.findIndex(m => m.id === material.id);
    if (index !== -1) {
      materials.value[index] = response.data.data;
    }
    if (selectedMaterial.value?.id === material.id) {
      selectedMaterial.value = response.data.data;
    }
  } catch (error) {
    console.error('Error al cambiar estado:', error);
    alert('Error: ' + (error.response?.data?.message || error.message));
  }
};

const updateTimer = async (material) => {
  try {
    await api.put(`/courses/${courseId.value}/materials/${material.id}/timer`, {
      timer_seconds: timerMinutes.value * 60
    });
    material.timer_seconds = timerMinutes.value * 60;
    const index = materials.value.findIndex(m => m.id === material.id);
    if (index !== -1) {
      materials.value[index].timer_seconds = timerMinutes.value * 60;
    }
  } catch (error) {
    console.error('Error al actualizar timer:', error);
    alert('Error: ' + (error.response?.data?.message || error.message));
  }
};

const loadAccessLogs = async (material) => {
  try {
    const response = await api.get(`/courses/${courseId.value}/materials/${material.id}/access-logs`);
    accessLogs.value = response.data.data || [];
  } catch (error) {
    console.error('Error al cargar logs:', error);
  }
};

const loadMaterials = async () => {
  try {
    loadingMaterials.value = true;
    const response = await api.get(`/courses/${courseId.value}/materials`);
    materials.value = response.data.data || [];
  } catch (error) {
    console.error('Error al cargar materiales:', error);
  } finally {
    loadingMaterials.value = false;
  }
};

const loadData = async () => {
  try {
    loading.value = true;
    try {
      cltSelection.value = await cltStore.fetchSelection(courseId.value);
    } catch (error) {
      cltSelection.value = null;
    }
    try {
      const studentsResponse = await api.get(`/courses/${courseId.value}/students`);
      students.value = studentsResponse.data.students || [];
    } catch (error) {
      console.error('Error al cargar estudiantes:', error);
    }
    await loadMaterials();
  } catch (error) {
    console.error('Error al cargar datos:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadData();
});
</script>
