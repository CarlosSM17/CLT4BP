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
            <h1 class="text-3xl font-bold">Efectos CLT</h1>
            <p class="text-gray-600 mt-1">Selecciona los efectos de Teoría de Carga Cognitiva para aplicar en el material instruccional</p>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-8">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <!-- Error: No hay perfil grupal -->
      <div v-else-if="!hasGroupProfile" class="alert alert-warning shadow-lg">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div>
          <h3 class="font-bold">Se requiere perfil grupal</h3>
          <div class="text-sm">
            Para obtener recomendaciones de efectos CLT, primero debes generar el perfil grupal del curso.
          </div>
        </div>
        <router-link :to="`/instructor/courses/${courseId}/profiles`" class="btn btn-sm">
          Ir a Perfiles
        </router-link>
      </div>

      <!-- Contenido principal -->
      <div v-else class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <!-- Estado actual de selección -->
          <div v-if="currentSelection && !editing" class="mb-6">
            <div class="alert alert-success">
              <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <h3 class="font-bold">Efectos CLT Seleccionados</h3>
                <div class="text-sm">
                  Tienes <span class="font-semibold">{{ currentSelection.selected_effects.length }}</span> efectos seleccionados para este curso.
                </div>
              </div>
              <button class="btn btn-sm btn-outline" @click="editing = true">
                Modificar Selección
              </button>
            </div>

            <!-- Lista de efectos seleccionados -->
            <div class="mt-4">
              <h4 class="font-semibold mb-2">Efectos seleccionados:</h4>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="effectId in currentSelection.selected_effects"
                  :key="effectId"
                  class="badge badge-lg badge-primary"
                >
                  {{ getEffectName(effectId) }}
                </span>
              </div>
            </div>

            <!-- Notas -->
            <div v-if="currentSelection.notes" class="mt-4">
              <h4 class="font-semibold mb-2">Notas:</h4>
              <p class="text-gray-600 bg-base-200 p-3 rounded">{{ currentSelection.notes }}</p>
            </div>

            <!-- Botón para continuar a materiales -->
            <div class="mt-6">
              <router-link
                :to="`/instructor/courses/${courseId}/materials`"
                class="btn btn-primary"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
                Continuar a Generación de Material
              </router-link>
            </div>
          </div>

          <!-- Selector de efectos CLT -->
          <CltEffectsSelector
            v-if="!currentSelection || editing"
            :courseId="courseId"
            :initialSelection="currentSelection?.selected_effects || []"
            :initialNotes="currentSelection?.notes || ''"
            @saved="handleSaved"
            @cancel="handleCancel"
          />
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AppLayout from '../../components/layout/AppLayout.vue';
import CltEffectsSelector from '../../components/clt/CltEffectsSelector.vue';
import { useCltEffectsStore } from '../../stores/cltEffects';
import api from '../../services/api';

const route = useRoute();
const router = useRouter();
const cltStore = useCltEffectsStore();

const courseId = computed(() => parseInt(route.params.courseId));
const loading = ref(true);
const editing = ref(false);
const currentSelection = ref(null);
const hasGroupProfile = ref(false);
const availableEffects = ref([]);

const getEffectName = (effectId) => {
  const effect = availableEffects.value.find(e => e.id === effectId);
  return effect?.name || effectId;
};

const handleSaved = async (data) => {
  currentSelection.value = data;
  editing.value = false;

  // Recargar la selección desde el servidor
  try {
    currentSelection.value = await cltStore.fetchSelection(courseId.value);
  } catch (error) {
    console.error('Error al recargar selección:', error);
  }
};

const handleCancel = () => {
  if (currentSelection.value) {
    editing.value = false;
  } else {
    router.push(`/instructor/courses/${courseId.value}`);
  }
};

const loadData = async () => {
  try {
    loading.value = true;

    // Verificar si existe perfil grupal
    try {
      await api.get(`/courses/${courseId.value}/profiles/group`);
      hasGroupProfile.value = true;
    } catch (error) {
      if (error.response?.status === 404) {
        hasGroupProfile.value = false;
        return;
      }
      hasGroupProfile.value = true; // Asumir que existe si hay otro error
    }

    // Cargar efectos disponibles
    const effectsData = await cltStore.fetchAvailableEffects();
    availableEffects.value = effectsData.effects || [];

    // Cargar selección actual si existe
    try {
      currentSelection.value = await cltStore.fetchSelection(courseId.value);
    } catch (error) {
      // No hay selección previa, es normal
      currentSelection.value = null;
    }

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
