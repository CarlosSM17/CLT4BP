<!-- src/views/instructor/ProfilesDashboard.vue -->
<template>
  <div class="profiles-dashboard container mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Perfiles de Estudiantes</h1>

      <div class="flex gap-2">
        <button
          class="btn btn-primary"
          @click="regenerateAllProfiles"
          :disabled="loading"
        >
          <svg v-if="loading" class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ loading ? 'Generando...' : 'Regenerar Todos los Perfiles' }}
        </button>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs tabs-boxed mb-6">
      <a
        class="tab"
        :class="{ 'tab-active': activeTab === 'group' }"
        @click="activeTab = 'group'"
      >
        Perfil Grupal
      </a>
      <a
        class="tab"
        :class="{ 'tab-active': activeTab === 'individual' }"
        @click="activeTab = 'individual'"
      >
        Perfiles Individuales
      </a>
    </div>

    <!-- Contenido -->
    <div v-if="activeTab === 'group'">
      <GroupProfileView
        v-if="groupProfile"
        :groupProfile="groupProfile"
      />
      <div v-else class="alert alert-warning">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
        <span>No hay perfil grupal generado. Genera los perfiles individuales primero.</span>
      </div>
    </div>

    <div v-else>
      <!-- Filtros y búsqueda -->
      <div class="mb-4 flex gap-4">
        <input
          type="text"
          placeholder="Buscar por nombre..."
          class="input input-bordered flex-1"
          v-model="searchQuery"
        />

        <select class="select select-bordered" v-model="filterLevel">
          <option value="">Todos los niveles</option>
          <option value="alto">Alto</option>
          <option value="medio">Medio</option>
          <option value="bajo">Bajo</option>
        </select>
      </div>

      <!-- Lista de perfiles -->
      <div class="grid grid-cols-1 gap-6">
        <StudentProfileCard
          v-for="profile in filteredProfiles"
          :key="profile.id"
          :profile="profile.profile_data"
          @view-details="viewProfileDetails"
        />
      </div>

      <div v-if="filteredProfiles.length === 0" class="alert alert-info mt-6">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        <span>No se encontraron perfiles que coincidan con los filtros.</span>
      </div>
    </div>

    <!-- Modal de detalles -->
    <ProfileDetailsModal
      v-if="selectedProfile"
      :profile="selectedProfile"
      @close="selectedProfile = null"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import GroupProfileView from '@/components/profiles/GroupProfileView.vue';
import StudentProfileCard from '@/components/profiles/StudentProfileCard.vue';
import ProfileDetailsModal from '@/components/profiles/ProfileDetailsModal.vue';
import { useProfilesStore } from '@/stores/profiles';

const route = useRoute();
const profilesStore = useProfilesStore();

const courseId = computed(() => route.params.courseId);
const activeTab = ref('group');
const loading = ref(false);
const searchQuery = ref('');
const filterLevel = ref('');
const selectedProfile = ref(null);

const studentProfiles = ref([]);
const groupProfile = ref(null);

const filteredProfiles = computed(() => {
  let profiles = studentProfiles.value;

  // Filtrar por búsqueda
  if (searchQuery.value) {
    profiles = profiles.filter(p =>
      p.profile_data.student_info.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }

  // Filtrar por nivel
  if (filterLevel.value) {
    profiles = profiles.filter(p =>
      p.profile_data.profile_summary.overall_motivation === filterLevel.value ||
      p.profile_data.profile_summary.overall_strategies === filterLevel.value ||
      p.profile_data.profile_summary.prior_knowledge === filterLevel.value
    );
  }

  return profiles;
});

const loadProfiles = async () => {
  try {
    loading.value = true;

    // Cargar perfiles individuales
    studentProfiles.value = await profilesStore.fetchCourseProfiles(courseId.value);

    // Cargar perfil grupal
    try {
      groupProfile.value = await profilesStore.fetchGroupProfile(courseId.value);
    } catch (error) {
      console.log('No hay perfil grupal generado aún');
    }
  } catch (error) {
    console.error('Error al cargar perfiles:', error);
  } finally {
    loading.value = false;
  }
};

const regenerateAllProfiles = async () => {
  if (!confirm('¿Estás seguro de que deseas regenerar todos los perfiles? Esto sobrescribirá los perfiles existentes.')) {
    return;
  }

  try {
    loading.value = true;
    await profilesStore.regenerateAllProfiles(courseId.value);
    await loadProfiles();
    alert('Perfiles regenerados exitosamente');
  } catch (error) {
    console.error('Error al regenerar perfiles:', error);
    alert('Error al regenerar perfiles. Por favor intenta nuevamente.');
  } finally {
    loading.value = false;
  }
};

const viewProfileDetails = (profile) => {
  selectedProfile.value = profile;
};

onMounted(() => {
  loadProfiles();
});
</script>
