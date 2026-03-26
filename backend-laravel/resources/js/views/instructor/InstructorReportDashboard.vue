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
            <h1 class="text-3xl font-bold">Reportes y Dashboard</h1>
            <p class="text-gray-600 mt-1">Análisis del grupo y comparaciones de aprendizaje</p>
          </div>
        </div>
        <router-link :to="`/instructor/courses/${courseId}/data-collection`" class="btn btn-ghost btn-sm">
          Recolección de Datos
        </router-link>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-16">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <!-- Sin perfil grupal -->
      <div v-else-if="!data.group_profile" class="alert alert-warning shadow-lg">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div>
          <h3 class="font-bold">No hay perfil grupal generado</h3>
          <p class="text-sm">Genera los perfiles individuales de los estudiantes y luego el perfil grupal.</p>
        </div>
        <router-link :to="`/instructor/courses/${courseId}/profiles`" class="btn btn-sm">
          Ir a Perfiles
        </router-link>
      </div>

      <!-- Contenido principal -->
      <div v-else>
        <!-- Tabs -->
        <div class="tabs tabs-boxed mb-6">
          <button class="tab" :class="{ 'tab-active': activeTab === 'group' }" @click="switchTab('group')">
            Perfil Grupal
          </button>
          <button class="tab" :class="{ 'tab-active': activeTab === 'prepost' }" @click="switchTab('prepost')">
            Comparación Pre/Post
          </button>
          <button class="tab" :class="{ 'tab-active': activeTab === 'individual' }" @click="switchTab('individual')">
            Perfiles Individuales
          </button>
        </div>

        <!-- TAB 1: PERFIL GRUPAL -->
        <div v-show="activeTab === 'group'">
          <!-- Stats generales -->
          <div class="stats shadow w-full mb-6">
            <div class="stat">
              <div class="stat-title">Estudiantes en el Perfil</div>
              <div class="stat-value text-primary">{{ data.group_profile.student_count }}</div>
            </div>
            <div class="stat">
              <div class="stat-title">Motivación Predominante</div>
              <div class="stat-value text-sm capitalize">
                <span class="badge badge-lg" :class="levelBadgeClass(data.group_profile.group_summary?.predominant_motivation)">
                  {{ data.group_profile.group_summary?.predominant_motivation || 'N/A' }}
                </span>
              </div>
            </div>
            <div class="stat">
              <div class="stat-title">Estrategias Predominantes</div>
              <div class="stat-value text-sm">
                <span class="badge badge-lg" :class="levelBadgeClass(data.group_profile.group_summary?.predominant_strategies)">
                  {{ data.group_profile.group_summary?.predominant_strategies || 'N/A' }}
                </span>
              </div>
            </div>
            <div class="stat">
              <div class="stat-title">Conocimiento Previo</div>
              <div class="stat-value text-sm">
                <span class="badge badge-lg" :class="levelBadgeClass(data.group_profile.group_summary?.predominant_knowledge)">
                  {{ data.group_profile.group_summary?.predominant_knowledge || 'N/A' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Descripción del grupo -->
          <div v-if="data.group_profile.group_summary?.group_characteristics" class="alert alert-info mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span>{{ data.group_profile.group_summary.group_characteristics }}</span>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <!-- Radar MSLQ -->
            <div class="card bg-base-100 shadow-xl">
              <div class="card-body">
                <h2 class="card-title text-lg">Perfil MSLQ del Grupo</h2>
                <p class="text-xs text-gray-500 mb-2">Promedio de las 15 dimensiones (escala 1-7)</p>
                <div class="relative" style="height: 320px;">
                  <canvas ref="radarGroupRef"></canvas>
                </div>
              </div>
            </div>

            <!-- Distribución de niveles -->
            <div class="card bg-base-100 shadow-xl">
              <div class="card-body">
                <h2 class="card-title text-lg">Distribución del Grupo</h2>
                <p class="text-xs text-gray-500 mb-2">Por dimensión (alto / medio / bajo)</p>
                <div class="grid grid-cols-1 gap-4">
                  <div>
                    <p class="text-sm font-medium mb-1">Motivación</p>
                    <div class="relative" style="height: 80px;">
                      <canvas ref="donutMotRef"></canvas>
                    </div>
                  </div>
                  <div>
                    <p class="text-sm font-medium mb-1">Estrategias</p>
                    <div class="relative" style="height: 80px;">
                      <canvas ref="donutStrRef"></canvas>
                    </div>
                  </div>
                  <div>
                    <p class="text-sm font-medium mb-1">Conocimiento Previo</p>
                    <div class="relative" style="height: 80px;">
                      <canvas ref="donutKnwRef"></canvas>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Conocimiento previo inicial -->
            <div class="card bg-base-100 shadow-xl">
              <div class="card-body">
                <h2 class="card-title text-lg">Conocimiento Previo (Promedio del Grupo)</h2>
                <div class="relative" style="height: 220px;">
                  <canvas ref="knowledgeRef"></canvas>
                </div>
              </div>
            </div>

            <!-- Carga Cognitiva -->
            <div class="card bg-base-100 shadow-xl">
              <div class="card-body">
                <h2 class="card-title text-lg">Carga Cognitiva</h2>
                <div v-if="data.cognitive_load?.available">
                  <p class="text-xs text-gray-500 mb-2">{{ data.cognitive_load.respondents }} respuestas (escala 0-10)</p>
                  <div class="relative" style="height: 200px;">
                    <canvas ref="cltRef"></canvas>
                  </div>
                </div>
                <div v-else class="flex items-center justify-center h-40 text-gray-400">
                  <div class="text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-2 opacity-30" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    <p class="text-sm">Sin datos de Escala de Carga Cognitiva</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- CIS / IMMS -->
            <div class="card bg-base-100 shadow-xl lg:col-span-2">
              <div class="card-body">
                <h2 class="card-title text-lg">Motivación e Interés (CIS / IMMS)</h2>
                <div v-if="data.course_interest?.available || data.imms?.available">
                  <div class="relative" style="height: 220px;">
                    <canvas ref="arcsRef"></canvas>
                  </div>
                </div>
                <div v-else class="flex items-center justify-center h-24 text-gray-400">
                  <p class="text-sm">Sin datos de CIS o IMMS aún</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Recomendaciones del grupo -->
          <div v-if="data.group_profile.teaching_recommendations?.length" class="card bg-base-100 shadow-xl mt-6">
            <div class="card-body">
              <h2 class="card-title text-lg">Recomendaciones Pedagógicas del Grupo</h2>
              <ul class="list-disc list-inside space-y-1">
                <li v-for="(rec, i) in data.group_profile.teaching_recommendations" :key="i" class="text-sm">
                  {{ rec }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- TAB 2: COMPARACIÓN PRE/POST -->
        <div v-show="activeTab === 'prepost'">
          <!-- Stats de cambio -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div v-for="(key, label) in prePostLabels" :key="key" class="stat bg-base-100 shadow rounded-lg">
              <div class="stat-title">{{ label }}</div>
              <template v-if="data.pre_post?.[key]?.available">
                <div class="stat-value text-sm">
                  {{ data.pre_post[key].initial_avg?.toFixed(1) }}
                  <span class="text-base-content/40">→</span>
                  {{ data.pre_post[key].final_avg?.toFixed(1) }}
                </div>
                <div class="stat-desc" :class="data.pre_post[key].change >= 0 ? 'text-success' : 'text-error'">
                  {{ data.pre_post[key].change >= 0 ? '↑' : '↓' }}
                  {{ Math.abs(data.pre_post[key].change).toFixed(1) }} puntos
                  ({{ data.pre_post[key].students }} estudiantes)
                </div>
              </template>
              <div v-else class="stat-desc text-gray-400">Sin datos suficientes</div>
            </div>
          </div>

          <!-- Gráfico comparativo -->
          <div class="card bg-base-100 shadow-xl mb-6">
            <div class="card-body">
              <h2 class="card-title text-lg">Comparación Pre/Post — Conocimiento</h2>
              <div v-if="hasPrePostKnowledge" class="relative" style="height: 300px;">
                <canvas ref="prePostKnwRef"></canvas>
              </div>
              <div v-else class="flex items-center justify-center h-40 text-gray-400">
                <p class="text-sm">No hay datos pre/post de conocimiento disponibles</p>
              </div>
            </div>
          </div>

          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title text-lg">Comparación Pre/Post — Motivación MSLQ</h2>
              <div v-if="data.pre_post?.mslq_motivation?.available" class="relative" style="height: 200px;">
                <canvas ref="prePostMotRef"></canvas>
              </div>
              <div v-else class="flex items-center justify-center h-32 text-gray-400">
                <p class="text-sm">No hay datos pre/post de motivación disponibles</p>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB 3: PERFILES INDIVIDUALES -->
        <div v-show="activeTab === 'individual'">
          <div v-if="data.student_profiles?.length === 0" class="alert alert-info">
            <p>No hay perfiles individuales generados aún.</p>
          </div>
          <div v-else class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title text-lg">Resumen por Estudiante</h2>
              <div class="overflow-x-auto">
                <table class="table table-zebra">
                  <thead>
                    <tr>
                      <th>Estudiante</th>
                      <th>Motivación</th>
                      <th>Estrategias</th>
                      <th>Conocimiento Previo</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="sp in data.student_profiles" :key="sp.student_id" class="hover cursor-pointer" @click="openStudentModal(sp)">
                      <td class="font-medium">{{ sp.name }}</td>
                      <td><span class="badge" :class="levelBadgeClass(sp.overall_motivation)">{{ sp.overall_motivation || 'N/A' }}</span></td>
                      <td><span class="badge" :class="levelBadgeClass(sp.overall_strategies)">{{ sp.overall_strategies || 'N/A' }}</span></td>
                      <td><span class="badge" :class="levelBadgeClass(sp.prior_knowledge)">{{ sp.prior_knowledge || 'N/A' }}</span></td>
                      <td>
                        <button class="btn btn-xs btn-ghost" @click.stop="openStudentModal(sp)">Ver detalle</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal: Perfil individual -->
    <dialog ref="studentModalRef" class="modal">
      <div class="modal-box max-w-2xl">
        <h3 class="font-bold text-lg mb-4" v-if="selectedStudent">
          {{ selectedStudent.name }}
          <span class="badge ml-2" :class="levelBadgeClass(selectedStudent.overall_motivation)">
            Mot: {{ selectedStudent.overall_motivation || 'N/A' }}
          </span>
          <span class="badge ml-1" :class="levelBadgeClass(selectedStudent.overall_strategies)">
            Est: {{ selectedStudent.overall_strategies || 'N/A' }}
          </span>
        </h3>

        <div v-if="selectedStudent">
          <div class="relative mb-4" style="height: 260px;">
            <canvas ref="radarStudentRef"></canvas>
          </div>

          <div class="overflow-x-auto max-h-60">
            <table class="table table-xs">
              <thead>
                <tr><th>Dimensión MSLQ</th><th>Promedio</th><th>Nivel</th></tr>
              </thead>
              <tbody>
                <tr v-for="(val, dim) in selectedStudent.mslq_scores" :key="dim">
                  <td>{{ mslqLabels[dim] || dim }}</td>
                  <td>{{ val.average?.toFixed(2) }}</td>
                  <td><span class="badge badge-xs" :class="levelBadgeClass(val.level)">{{ val.level }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="modal-action">
          <form method="dialog">
            <button class="btn" @click="closeStudentModal">Cerrar</button>
          </form>
        </div>
      </div>
    </dialog>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { Chart, registerables } from 'chart.js';
import AppLayout from '../../components/layout/AppLayout.vue';
import api from '../../services/api';

Chart.register(...registerables);

const route = useRoute();
const courseId = computed(() => parseInt(route.params.courseId));

const loading = ref(true);
const data = ref({});
const activeTab = ref('group');
const selectedStudent = ref(null);

// Canvas refs
const radarGroupRef = ref(null);
const donutMotRef   = ref(null);
const donutStrRef   = ref(null);
const donutKnwRef   = ref(null);
const knowledgeRef  = ref(null);
const cltRef        = ref(null);
const arcsRef       = ref(null);
const prePostKnwRef = ref(null);
const prePostMotRef = ref(null);
const radarStudentRef = ref(null);
const studentModalRef = ref(null);

// Chart instances
let charts = {};

const LEVEL_COLORS = {
  alto:  '#22c55e',
  medio: '#eab308',
  bajo:  '#ef4444',
};

const mslqLabels = {
  intrinsic_goal_orientation:      'Orientación Intrínseca',
  extrinsic_goal_orientation:      'Orientación Extrínseca',
  task_value:                      'Valor de la Tarea',
  control_beliefs:                 'Creencias de Control',
  self_efficacy:                   'Autoeficacia',
  test_anxiety:                    'Ansiedad ante Pruebas',
  rehearsal:                       'Repaso',
  elaboration:                     'Elaboración',
  organization:                    'Organización',
  critical_thinking:               'Pensamiento Crítico',
  metacognitive_self_regulation:   'Autorregulación Metacognitiva',
  time_management:                 'Gestión del Tiempo',
  effort_regulation:               'Regulación del Esfuerzo',
  peer_learning:                   'Aprendizaje entre Pares',
  help_seeking:                    'Búsqueda de Ayuda',
};

const cltLabels = {
  intrinsic_load:  'Carga Intrínseca',
  extraneous_load: 'Carga Extrínseca',
  germane_load:    'Carga Germana',
};

const arcsLabels = {
  attention:    'Atención',
  relevance:    'Relevancia',
  confidence:   'Confianza',
  satisfaction: 'Satisfacción',
};

const prePostLabels = {
  recall:          'Recall',
  comprehension:   'Comprensión',
  mslq_motivation: 'Motivación MSLQ',
};

const hasPrePostKnowledge = computed(() =>
  data.value.pre_post?.recall?.available || data.value.pre_post?.comprehension?.available
);

const levelBadgeClass = (level) => {
  if (level === 'alto')  return 'badge-success';
  if (level === 'medio') return 'badge-warning';
  if (level === 'bajo')  return 'badge-error';
  return 'badge-ghost';
};

const destroyChart = (key) => {
  if (charts[key]) {
    charts[key].destroy();
    delete charts[key];
  }
};

const destroyAll = () => {
  Object.keys(charts).forEach(k => { charts[k]?.destroy(); });
  charts = {};
};

// ── Chart initializers ──────────────────────────────────────────────────────

const initGroupCharts = async () => {
  await nextTick();
  const gp = data.value.group_profile;
  if (!gp) return;

  // Radar MSLQ
  const mslqKeys = Object.keys(mslqLabels);
  const mslqAvg  = gp.mslq_averages ?? {};
  destroyChart('radarGroup');
  if (radarGroupRef.value) {
    charts.radarGroup = new Chart(radarGroupRef.value, {
      type: 'radar',
      data: {
        labels: mslqKeys.map(k => mslqLabels[k]),
        datasets: [{
          label: 'Promedio del Grupo',
          data: mslqKeys.map(k => mslqAvg[k]?.average ?? 0),
          backgroundColor: 'rgba(99,102,241,0.2)',
          borderColor: '#6366f1',
          pointBackgroundColor: '#6366f1',
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { r: { min: 0, max: 7, ticks: { stepSize: 1 } } },
        plugins: { legend: { display: false } },
      },
    });
  }

  // Donuts distribución
  const dist = gp.distribution ?? {};
  const donutConfigs = [
    { ref: donutMotRef, key: 'motivation_levels',  chart: 'donutMot' },
    { ref: donutStrRef, key: 'strategies_levels',  chart: 'donutStr' },
    { ref: donutKnwRef, key: 'knowledge_levels',   chart: 'donutKnw' },
  ];
  for (const cfg of donutConfigs) {
    destroyChart(cfg.chart);
    const levels = dist[cfg.key] ?? {};
    if (cfg.ref.value) {
      charts[cfg.chart] = new Chart(cfg.ref.value, {
        type: 'doughnut',
        data: {
          labels: ['Alto', 'Medio', 'Bajo'],
          datasets: [{
            data: [levels.alto ?? 0, levels.medio ?? 0, levels.bajo ?? 0],
            backgroundColor: [LEVEL_COLORS.alto, LEVEL_COLORS.medio, LEVEL_COLORS.bajo],
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'right', labels: { boxWidth: 12, font: { size: 11 } } } },
        },
      });
    }
  }

  // Conocimiento previo
  const ka = gp.knowledge_averages ?? {};
  destroyChart('knowledge');
  if (knowledgeRef.value) {
    charts.knowledge = new Chart(knowledgeRef.value, {
      type: 'bar',
      data: {
        labels: ['Recall', 'Comprensión'],
        datasets: [{
          label: 'Promedio del Grupo (%)',
          data: [ka.recall?.average ?? 0, ka.comprehension?.average ?? 0],
          backgroundColor: ['rgba(99,102,241,0.7)', 'rgba(16,185,129,0.7)'],
          borderColor:     ['#6366f1', '#10b981'],
          borderWidth: 1,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { min: 0, max: 100, ticks: { callback: v => v + '%' } } },
        plugins: { legend: { display: false } },
      },
    });
  }

  // Carga cognitiva
  destroyChart('clt');
  if (data.value.cognitive_load?.available && cltRef.value) {
    const cl  = data.value.cognitive_load;
    const dims = Object.keys(cltLabels);
    charts.clt = new Chart(cltRef.value, {
      type: 'bar',
      data: {
        labels: dims.map(d => cltLabels[d]),
        datasets: [{
          label: 'Promedio (0-10)',
          data: dims.map(d => cl.dimensions?.[d] ?? 0),
          backgroundColor: ['rgba(239,68,68,0.7)', 'rgba(234,179,8,0.7)', 'rgba(34,197,94,0.7)'],
          borderWidth: 1,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { min: 0, max: 10 } },
        plugins: { legend: { display: false } },
      },
    });
  }

  // CIS / IMMS
  destroyChart('arcs');
  const hasCis  = data.value.course_interest?.available;
  const hasImms = data.value.imms?.available;
  if ((hasCis || hasImms) && arcsRef.value) {
    const arcsDims = Object.keys(arcsLabels);
    const datasets = [];
    if (hasCis) {
      datasets.push({
        label: 'Course Interest Survey (CIS)',
        data: arcsDims.map(d => data.value.course_interest.dimensions?.[d] ?? 0),
        backgroundColor: 'rgba(99,102,241,0.7)',
      });
    }
    if (hasImms) {
      datasets.push({
        label: 'IMMS',
        data: arcsDims.map(d => data.value.imms.dimensions?.[d] ?? 0),
        backgroundColor: 'rgba(16,185,129,0.7)',
      });
    }
    charts.arcs = new Chart(arcsRef.value, {
      type: 'bar',
      data: { labels: arcsDims.map(d => arcsLabels[d]), datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { min: 1, max: 5 } },
      },
    });
  }
};

const initPrePostCharts = async () => {
  await nextTick();
  const pp = data.value.pre_post ?? {};

  // Conocimiento pre/post
  destroyChart('prePostKnw');
  const datasets = [];
  const knwLabels = [];
  if (pp.recall?.available) {
    knwLabels.push('Recall');
  }
  if (pp.comprehension?.available) {
    knwLabels.push('Comprensión');
  }

  if (knwLabels.length && prePostKnwRef.value) {
    const initialData = [];
    const finalData   = [];
    if (pp.recall?.available)        { initialData.push(pp.recall.initial_avg);       finalData.push(pp.recall.final_avg); }
    if (pp.comprehension?.available) { initialData.push(pp.comprehension.initial_avg); finalData.push(pp.comprehension.final_avg); }

    charts.prePostKnw = new Chart(prePostKnwRef.value, {
      type: 'bar',
      data: {
        labels: knwLabels,
        datasets: [
          { label: 'Inicial', data: initialData, backgroundColor: 'rgba(99,102,241,0.7)' },
          { label: 'Final',   data: finalData,   backgroundColor: 'rgba(34,197,94,0.7)' },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { min: 0, max: 100, ticks: { callback: v => v + '%' } } },
      },
    });
  }

  // Motivación pre/post
  destroyChart('prePostMot');
  if (pp.mslq_motivation?.available && prePostMotRef.value) {
    charts.prePostMot = new Chart(prePostMotRef.value, {
      type: 'bar',
      data: {
        labels: ['Motivación MSLQ (pre/post)'],
        datasets: [
          { label: 'Inicial', data: [pp.mslq_motivation.initial_avg], backgroundColor: 'rgba(99,102,241,0.7)' },
          { label: 'Final',   data: [pp.mslq_motivation.final_avg],   backgroundColor: 'rgba(34,197,94,0.7)' },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { min: 1, max: 7 } },
      },
    });
  }
};

const initStudentRadar = async (sp) => {
  await nextTick();
  destroyChart('radarStudent');
  if (!radarStudentRef.value) return;
  const mslqKeys = Object.keys(mslqLabels);
  const scores   = sp.mslq_scores ?? {};
  const gpAvg    = data.value.group_profile?.mslq_averages ?? {};

  charts.radarStudent = new Chart(radarStudentRef.value, {
    type: 'radar',
    data: {
      labels: mslqKeys.map(k => mslqLabels[k]),
      datasets: [
        {
          label: sp.name,
          data: mslqKeys.map(k => scores[k]?.average ?? 0),
          backgroundColor: 'rgba(99,102,241,0.2)',
          borderColor: '#6366f1',
          pointBackgroundColor: '#6366f1',
        },
        {
          label: 'Promedio del Grupo',
          data: mslqKeys.map(k => gpAvg[k]?.average ?? 0),
          backgroundColor: 'rgba(156,163,175,0.15)',
          borderColor: '#9ca3af',
          borderDash: [4, 4],
          pointBackgroundColor: '#9ca3af',
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { r: { min: 0, max: 7, ticks: { stepSize: 1 } } },
    },
  });
};

// ── Navegación y carga ──────────────────────────────────────────────────────

const switchTab = async (tab) => {
  activeTab.value = tab;
  if (tab === 'group')   initGroupCharts();
  if (tab === 'prepost') initPrePostCharts();
};

const openStudentModal = async (sp) => {
  selectedStudent.value = sp;
  studentModalRef.value?.showModal();
  await initStudentRadar(sp);
};

const closeStudentModal = () => {
  destroyChart('radarStudent');
  selectedStudent.value = null;
};

const loadData = async () => {
  try {
    loading.value = true;
    const res = await api.get(`/courses/${courseId.value}/reports/instructor`);
    data.value = res.data;
  } catch (err) {
    console.error('Error al cargar reportes:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadData();
  if (data.value.group_profile) {
    initGroupCharts();
  }
});

onUnmounted(() => {
  destroyAll();
});
</script>
