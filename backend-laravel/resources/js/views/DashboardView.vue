<template>
  <AppLayout>
    <div class='container mx-auto'>
      <h1 class='text-4xl font-bold mb-8'>
        Bienvenido, {{ authStore.user?.name }}
      </h1>

      <div class='grid grid-cols-1 md:grid-cols-3 gap-6'>
        <!-- Card de perfil -->
        <div class='card bg-base-100 shadow-xl'>
          <div class='card-body'>
            <h2 class='card-title'>Tu Perfil</h2>
            <div class='space-y-2'>
              <p><strong>Rol:</strong> {{ roleLabel }}</p>
              <p><strong>Email:</strong> {{ authStore.user?.email }}</p>
              <p v-if='authStore.user?.last_login'>
                <strong>Último acceso:</strong><br/>
                {{ formatDate(authStore.user.last_login) }}
              </p>
            </div>
            <div class='card-actions justify-end'>
              <router-link to='/profile' class='btn btn-primary btn-sm'>
                Ver Perfil
              </router-link>
            </div>
          </div>
        </div>

        <!-- Cards específicas por rol -->
        <div v-if='authStore.user?.role === "admin"' class='card bg-primary text-primary-content shadow-xl'>
          <div class='card-body'>
            <h2 class='card-title'>Panel de Administración</h2>
            <p>Gestiona usuarios e instructores del sistema</p>
            <div class='card-actions justify-end'>
              <router-link to='/admin/users' class='btn btn-secondary btn-sm'>
                Ver Usuarios
              </router-link>
            </div>
          </div>
        </div>

        <div v-if='authStore.user?.role === "instructor"' class='card bg-secondary text-secondary-content shadow-xl'>
          <div class='card-body'>
            <h2 class='card-title'>Mis Cursos</h2>
            <p>Crea y gestiona cursos, estudiantes y evaluaciones</p>
            <div class='card-actions justify-end mt-4'>
              <router-link to='/instructor/courses' class='btn btn-primary btn-sm'>
                Ver Cursos
              </router-link>
            </div>
          </div>
        </div>

        <div v-if='authStore.user?.role === "student"' class='card bg-accent text-accent-content shadow-xl'>
          <div class='card-body'>
            <h2 class='card-title'>Mis Cursos</h2>
            <p>Accede a tus cursos inscritos y evaluaciones</p>
            <div class='card-actions justify-end mt-4'>
              <router-link to='/student/courses' class='btn btn-primary btn-sm'>
                Ver Mis Cursos
              </router-link>
            </div>
          </div>
        </div>

        <!-- Info del Sprint
        <div class='card bg-base-100 shadow-xl'>
          <div class='card-body'>
            <h2 class='card-title'>Estado del Proyecto</h2>
            <div class='space-y-2'>
              <div class='flex justify-between items-center'>
                <span>Sprint 1 - Fundamentos:</span>
                <div class='badge badge-success'>✓ Completado</div>
              </div>
              <div class='flex justify-between items-center'>
                <span>Sprint 2 - Cursos:</span>
                <div class='badge badge-success'>✓ Completado</div>
              </div>
              <div class='flex justify-between items-center'>
                <span>Sprint 3 - Evaluaciones:</span>
                <div class='badge badge-success'>✓ Completado</div>
              </div>
              <div class='flex justify-between items-center'>
                <span>Frontend Vue.js:</span>
                <div class='badge badge-success'>✓ Operativo</div>
              </div>
            </div>
          </div>
        </div>-->
      </div>

      <!-- Stats -->
      <div class='stats shadow mt-8 w-full'>
        <div class='stat'>
          <div class='stat-figure text-primary'>
            <svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' class='inline-block w-8 h-8 stroke-current'>
              <path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'></path>
            </svg>
          </div>
          <div class='stat-title'>Estado</div>
          <div class='stat-value text-primary'>Activo</div>
          <div class='stat-desc'>Sistema funcionando</div>
        </div>
        <!--
        <div class='stat'>
          <div class='stat-figure text-secondary'>
            <svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' class='inline-block w-8 h-8 stroke-current'>
              <path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M13 10V3L4 14h7v7l9-11h-7z'></path>
            </svg>
          </div>
          <div class='stat-title'>Sprint Actual</div>
          <div class='stat-value text-secondary'>3</div>
          <div class='stat-desc'>Evaluaciones completadas</div>
        </div>-->

        <div class='stat'>
          <div class='stat-title'>Tu Rol</div>
          <div class='stat-value text-sm'>{{ roleLabel }}</div>
          <div class='stat-desc'>{{ authStore.user?.email }}</div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import AppLayout from '../components/layout/AppLayout.vue';

const authStore = useAuthStore();

const roleLabel = computed(() => {
  const roles = {
    admin: 'Administrador',
    instructor: 'Instructor',
    student: 'Estudiante',
  };
  return roles[authStore.user?.role] || '';
});

const formatDate = (date) => {
  return new Date(date).toLocaleString('es-MX', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

onMounted(async () => {
  // Si no hay usuario, obtenerlo
  if (!authStore.user && authStore.token) {
    try {
      await authStore.fetchUser();
    } catch (error) {
      console.error('Error fetching user:', error);
    }
  }
});
</script>
