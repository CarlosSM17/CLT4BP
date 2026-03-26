<!-- src/components/profiles/GroupProfileView.vue -->
<template>
  <div class="group-profile-view">
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-2xl">
          Perfil Grupal del Curso
          <div class="badge badge-lg badge-primary">
            {{ groupProfile.student_count }} estudiantes
          </div>
        </h2>

        <!-- Resumen del grupo -->
        <div class="alert alert-info mt-4">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <span>{{ groupProfile.profile_data.group_summary.group_characteristics }}</span>
        </div>

        <!-- Niveles predominantes -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          <div class="stat bg-base-200 rounded-lg">
            <div class="stat-title">Motivación Predominante</div>
            <div class="stat-value text-2xl" :class="getLevelClass(groupProfile.profile_data.group_summary.predominant_motivation)">
              {{ groupProfile.profile_data.group_summary.predominant_motivation }}
            </div>
          </div>

          <div class="stat bg-base-200 rounded-lg">
            <div class="stat-title">Estrategias Predominantes</div>
            <div class="stat-value text-2xl" :class="getLevelClass(groupProfile.profile_data.group_summary.predominant_strategies)">
              {{ groupProfile.profile_data.group_summary.predominant_strategies }}
            </div>
          </div>

          <div class="stat bg-base-200 rounded-lg">
            <div class="stat-title">Conocimiento Predominante</div>
            <div class="stat-value text-2xl" :class="getLevelClass(groupProfile.profile_data.group_summary.predominant_knowledge)">
              {{ groupProfile.profile_data.group_summary.predominant_knowledge }}
            </div>
          </div>
        </div>

        <!-- Gráficos de distribución -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          <div>
            <h3 class="font-semibold mb-3 text-center">Distribución de Motivación</h3>
            <DistributionChart :data="groupProfile.profile_data.distribution.motivation_levels" />
          </div>

          <div>
            <h3 class="font-semibold mb-3 text-center">Distribución de Estrategias</h3>
            <DistributionChart :data="groupProfile.profile_data.distribution.strategies_levels" />
          </div>

          <div>
            <h3 class="font-semibold mb-3 text-center">Distribución de Conocimiento</h3>
            <DistributionChart :data="groupProfile.profile_data.distribution.knowledge_levels" />
          </div>
        </div>

        <!-- Promedios MSLQ -->
        <div class="mt-6">
          <h3 class="font-semibold text-lg mb-3">Promedios MSLQ del Grupo</h3>
          <ProfileRadarChart :data="getRadarData()" title="Perfil Grupal" />
        </div>

        <!-- Recomendaciones pedagógicas -->
        <div class="mt-6">
          <h3 class="font-semibold text-lg mb-3">Recomendaciones Pedagógicas</h3>
          <div class="alert alert-success">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <ul class="list-disc list-inside">
              <li v-for="(rec, index) in groupProfile.profile_data.teaching_recommendations" :key="index" class="mb-1">
                {{ rec }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import ProfileRadarChart from './ProfileRadarChart.vue';
import DistributionChart from './DistributionChart.vue';

const props = defineProps({
  groupProfile: {
    type: Object,
    required: true
  }
});

const getLevelClass = (level) => {
  switch(level?.toLowerCase()) {
    case 'alto': return 'text-success';
    case 'medio': return 'text-warning';
    case 'bajo': return 'text-error';
    default: return 'text-base-content';
  }
};

const getRadarData = () => {
  const mslqAverages = props.groupProfile.profile_data.mslq_averages;

  const labels = [
    'Autoeficacia',
    'Valor de Tarea',
    'Elaboración',
    'Organización',
    'Pensamiento Crítico',
    'Autorregulación',
    'Gestión del Tiempo',
    'Aprendizaje entre Pares'
  ];

  const values = [
    mslqAverages.self_efficacy?.average || 0,
    mslqAverages.task_value?.average || 0,
    mslqAverages.elaboration?.average || 0,
    mslqAverages.organization?.average || 0,
    mslqAverages.critical_thinking?.average || 0,
    mslqAverages.metacognitive_self_regulation?.average || 0,
    mslqAverages.time_management?.average || 0,
    mslqAverages.peer_learning?.average || 0
  ];

  return { labels, values };
};
</script>
