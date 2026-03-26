<!-- src/components/clt/CltEffectsSelector.vue -->
<template>
  <div class="clt-effects-selector">
    <!-- Header con recomendaciones -->
    <div class="alert alert-info mb-6" v-if="recommendations">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      <div>
        <h3 class="font-bold">Recomendaciones basadas en el perfil grupal</h3>
        <div class="text-sm mt-1">{{ recommendations.reasoning }}</div>
        <div class="mt-2">
          <button
            class="btn btn-sm btn-outline"
            @click="applyRecommendations"
          >
            Aplicar Efectos Recomendados
          </button>
        </div>
      </div>
    </div>

    <!-- Tabs por categoría -->
    <div class="tabs tabs-boxed mb-6">
      <a
        class="tab"
        :class="{ 'tab-active': activeCategory === 'new_knowledge' }"
        @click="activeCategory = 'new_knowledge'"
      >
        Nuevo Conocimiento ({{ newKnowledgeEffects.length }})
      </a>
      <a
        class="tab"
        :class="{ 'tab-active': activeCategory === 'prior_knowledge' }"
        @click="activeCategory = 'prior_knowledge'"
      >
        Conocimiento Previo ({{ priorKnowledgeEffects.length }})
      </a>
      <a
        class="tab"
        :class="{ 'tab-active': activeCategory === 'all' }"
        @click="activeCategory = 'all'"
      >
        Todos ({{ effects.length }})
      </a>
    </div>

    <!-- Contador de seleccionados -->
    <div class="flex justify-between items-center mb-4">
      <div class="text-sm">
        <span class="font-semibold">{{ selectedCount }}</span> efectos seleccionados
      </div>

      <div class="flex gap-2">
        <button
          class="btn btn-sm btn-ghost"
          @click="selectAll"
          v-if="filteredEffects.length > selectedInCategory"
        >
          Seleccionar Todos
        </button>
        <button
          class="btn btn-sm btn-ghost"
          @click="deselectAll"
          v-if="selectedInCategory > 0"
        >
          Deseleccionar Todos
        </button>
      </div>
    </div>

    <!-- Grid de efectos -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <CltEffectCard
        v-for="effect in filteredEffects"
        :key="effect.id"
        :effect="effect"
        :selected="isSelected(effect.id)"
        @toggle="toggleEffect(effect.id)"
      />
    </div>

    <!-- Notas adicionales -->
    <div class="mt-6">
      <label class="label">
        <span class="label-text font-semibold">Notas Adicionales (opcional)</span>
      </label>
      <textarea
        class="textarea textarea-bordered w-full"
        rows="3"
        v-model="notes"
        placeholder="Agrega notas o consideraciones especiales sobre la aplicación de estos efectos..."
      ></textarea>
    </div>

    <!-- Botones de acción -->
    <div class="flex justify-end gap-2 mt-6">
      <button
        class="btn btn-ghost"
        @click="$emit('cancel')"
      >
        Cancelar
      </button>
      <button
        class="btn btn-primary"
        @click="saveSelection"
        :disabled="selectedCount === 0 || saving"
      >
        <svg v-if="saving" class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        {{ saving ? 'Guardando...' : 'Guardar Selección' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import CltEffectCard from './CltEffectCard.vue';
import { useCltEffectsStore } from '@/stores/cltEffects';

const props = defineProps({
  courseId: {
    type: Number,
    required: true
  },
  initialSelection: {
    type: Array,
    default: () => []
  },
  initialNotes: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['saved', 'cancel']);

const cltStore = useCltEffectsStore();
const activeCategory = ref('all');
const selectedEffects = ref([...props.initialSelection]);
const notes = ref(props.initialNotes);
const saving = ref(false);
const effects = ref([]);
const recommendations = ref(null);

const newKnowledgeEffects = computed(() =>
  effects.value.filter(e => e.category === 'new_knowledge')
);

const priorKnowledgeEffects = computed(() =>
  effects.value.filter(e => e.category === 'prior_knowledge')
);

const filteredEffects = computed(() => {
  if (activeCategory.value === 'all') return effects.value;
  return effects.value.filter(e => e.category === activeCategory.value);
});

const selectedCount = computed(() => selectedEffects.value.length);

const selectedInCategory = computed(() => {
  return selectedEffects.value.filter(id => {
    const effect = effects.value.find(e => e.id === id);
    return !effect || activeCategory.value === 'all' || effect.category === activeCategory.value;
  }).length;
});

const isSelected = (effectId) => selectedEffects.value.includes(effectId);

const toggleEffect = (effectId) => {
  const index = selectedEffects.value.indexOf(effectId);
  if (index > -1) {
    selectedEffects.value.splice(index, 1);
  } else {
    selectedEffects.value.push(effectId);
  }
};

const selectAll = () => {
  filteredEffects.value.forEach(effect => {
    if (!isSelected(effect.id)) {
      selectedEffects.value.push(effect.id);
    }
  });
};

const deselectAll = () => {
  const idsToRemove = filteredEffects.value.map(e => e.id);
  selectedEffects.value = selectedEffects.value.filter(
    id => !idsToRemove.includes(id)
  );
};

const applyRecommendations = () => {
  if (recommendations.value) {
    selectedEffects.value = [...recommendations.value.recommended_effects];
  }
};

const saveSelection = async () => {
  if (selectedEffects.value.length === 0) {
    alert('Debes seleccionar al menos un efecto CLT');
    return;
  }

  try {
    saving.value = true;

    await cltStore.saveSelection(props.courseId, {
      selected_effects: selectedEffects.value,
      notes: notes.value
    });

    emit('saved', {
      selected_effects: selectedEffects.value,
      notes: notes.value
    });

  } catch (error) {
    console.error('Error al guardar selección:', error);
    alert('Error al guardar la selección. Por favor intenta nuevamente.');
  } finally {
    saving.value = false;
  }
};

const loadData = async () => {
  try {
    // Cargar efectos disponibles
    const effectsData = await cltStore.fetchAvailableEffects(props.courseId);
    effects.value = effectsData.effects || effectsData;

    // Cargar recomendaciones
    try {
      recommendations.value = await cltStore.fetchRecommendations(props.courseId);
    } catch (error) {
      console.log('No se pudieron cargar recomendaciones:', error);
    }

  } catch (error) {
    console.error('Error al cargar datos:', error);
    alert('Error al cargar los efectos CLT');
  }
};

onMounted(() => {
  loadData();
});
</script>
