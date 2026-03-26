<!-- src/views/instructor/MaterialGenerationTest.vue -->
<template>
  <div class="material-generation-test container mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6">Prueba de Generación de Material con IA</h1>

    <!-- Paso 1: Efectos CLT -->
    <div class="card bg-base-100 shadow-xl mb-6">
      <div class="card-body">
        <h2 class="card-title">
          Paso 1: Preselección de Efectos CLT
          <div v-if="cltSelection" class="badge badge-success">Completado</div>
        </h2>

        <div v-if="!showCltSelector && !cltSelection">
          <p class="mb-4">Antes de generar material, debes seleccionar los efectos CLT que se aplicarán.</p>
          <button class="btn btn-primary" @click="showCltSelector = true">
            Seleccionar Efectos CLT
          </button>
        </div>

        <div v-else-if="!showCltSelector && cltSelection">
          <p class="mb-2">
            <span class="font-semibold">{{ cltSelection.selected_effects.length }}</span> efectos seleccionados
          </p>
          <button class="btn btn-sm btn-outline" @click="showCltSelector = true">
            Modificar Selección
          </button>
        </div>

        <CltEffectsSelector
          v-if="showCltSelector"
          :courseId="courseId"
          :initialSelection="cltSelection?.selected_effects || []"
          :initialNotes="cltSelection?.notes || ''"
          @saved="handleCltSaved"
          @cancel="showCltSelector = false"
        />
      </div>
    </div>

    <!-- Paso 2: Configuración del Material -->
    <div class="card bg-base-100 shadow-xl mb-6" v-if="cltSelection">
      <div class="card-body">
        <h2 class="card-title">Paso 2: Configuración del Material a Generar</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Tipo de Material -->
          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Tipo de Material *</span>
            </label>
            <select class="select select-bordered" v-model="materialConfig.material_type">
              <option value="">Selecciona un tipo</option>
              <option value="example">Ejemplo Real</option>
              <option value="learning_tasks">Tareas de Aprendizaje</option>
              <option value="support_info">Información de Soporte</option>
              <option value="procedural_info">Información Procedimental</option>
              <option value="verbal_protocols">Protocolos Verbales</option>
            </select>
          </div>

          <!-- Tipo de Perfil -->
          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Tipo de Perfil *</span>
            </label>
            <select class="select select-bordered" v-model="materialConfig.profile_type">
              <option value="group">Perfil Grupal</option>
              <option value="individual">Perfil Individual</option>
            </select>
          </div>

          <!-- Estudiante (si es individual) -->
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

          <!-- Tema -->
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

          <!-- Contexto adicional -->
          <div class="form-control md:col-span-2">
            <label class="label">
              <span class="label-text font-semibold">Contexto Adicional (opcional)</span>
            </label>
            <textarea
              class="textarea textarea-bordered"
              rows="3"
              v-model="materialConfig.additional_context"
              placeholder="Información adicional o instrucciones específicas para la generación..."
            ></textarea>
          </div>
        </div>

        <!-- Botón de generación -->
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
{{ generating ? 'Generando Material...' : 'Generar Material con IA' }}
</button>
</div>
</div>
</div>
<!-- Paso 3: Material Generado -->
<div class="card bg-base-100 shadow-xl" v-if="generatedMaterial">
  <div class="card-body">
    <h2 class="card-title">
      Paso 3: Material Generado
      <div class="badge badge-success">Exitoso</div>
    </h2>

    <!-- Información de generación -->
    <div class="alert alert-success mb-4">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <div>
        <div class="font-bold">Material generado exitosamente</div>
        <div class="text-sm">
          Tokens utilizados: {{ generatedMaterial.token_usage?.total_tokens || 'N/A' }}
        </div>
      </div>
    </div>

    <!-- Visualización del contenido -->
    <div class="bg-base-200 p-4 rounded-lg">
      <h3 class="font-semibold mb-2">Contenido Generado:</h3>
      <pre class="whitespace-pre-wrap text-sm">{{ JSON.stringify(generatedMaterial.material.content, null, 2) }}</pre>
    </div>

    <!-- Acciones -->
    <div class="card-actions justify-end mt-4">
      <button class="btn btn-ghost" @click="resetForm">
        Generar Otro Material
      </button>
    </div>
  </div>
</div>
</div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import CltEffectsSelector from '@/components/clt/CltEffectsSelector.vue';
import { useCltEffectsStore } from '@/stores/cltEffects';
import api from '@/services/api';

const route = useRoute();
const cltStore = useCltEffectsStore();

const courseId = computed(() => parseInt(route.params.courseId));

const showCltSelector = ref(false);
const cltSelection = ref(null);
const students = ref([]);
const generating = ref(false);
const generatedMaterial = ref(null);

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

const handleCltSaved = (data) => {
  cltSelection.value = data;
  showCltSelector.value = false;
};

const generateMaterial = async () => {
  if (!canGenerate.value) return;

  try {
    generating.value = true;

    const response = await api.post(`/courses/${courseId.value}/materials/generate`, materialConfig.value);

    generatedMaterial.value = response.data.data;

    alert('Material generado exitosamente');

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

const loadData = async () => {
  try {
    // Cargar selección de efectos CLT
    const selection = await cltStore.fetchSelection(courseId.value);
    cltSelection.value = selection;

    // Cargar lista de estudiantes del curso
    const studentsResponse = await api.get(`/courses/${courseId.value}/students`);
    students.value = studentsResponse.data.data;

  } catch (error) {
    console.error('Error al cargar datos:', error);
  }
};

onMounted(() => {
  loadData();
});
</script>
