<template>
  <AppLayout>
    <div class='container mx-auto max-w-2xl'>
      <h1 class='text-4xl font-bold mb-8'>Mi Perfil</h1>

      <div class='card bg-base-100 shadow-xl'>
        <div class='card-body'>
          <div class='flex items-center gap-4 mb-6'>
            <div class='avatar placeholder'>
              <div class='bg-primary text-primary-content rounded-full w-24'>
                <span class='text-3xl'>{{ userInitials }}</span>
              </div>
            </div>
            <div>
              <h2 class='text-2xl font-bold'>{{ authStore.user?.name }}</h2>
              <p class='text-gray-600'>{{ roleLabel }}</p>
            </div>
          </div>

          <div class='divider'></div>

          <div class='grid grid-cols-1 md:grid-cols-2 gap-4'>
            <div>
              <label class='label'>
                <span class='label-text font-bold'>Email</span>
              </label>
              <input
                type='email'
                :value='authStore.user?.email'
                class='input input-bordered w-full'
                disabled
              />
            </div>

            <div>
              <label class='label'>
                <span class='label-text font-bold'>Rol</span>
              </label>
              <input
                type='text'
                :value='roleLabel'
                class='input input-bordered w-full'
                disabled
              />
            </div>

            <div class='md:col-span-2'>
              <label class='label'>
                <span class='label-text font-bold'>Nombre Completo</span>
              </label>
              <input
                v-model='profileForm.name'
                type='text'
                class='input input-bordered w-full'
                placeholder='Tu nombre'
              />
            </div>

            <div class='md:col-span-2'>
              <label class='label'>
                <span class='label-text font-bold'>Último acceso</span>
              </label>
              <input
                type='text'
                :value='formatDate(authStore.user?.last_login)'
                class='input input-bordered w-full'
                disabled
              />
            </div>
          </div>

          <div class='divider'>Cambiar Contraseña</div>

          <div class='grid grid-cols-1 gap-4'>
            <div>
              <label class='label'>
                <span class='label-text font-bold'>Nueva Contraseña</span>
              </label>
              <input
                v-model='passwordForm.password'
                type='password'
                class='input input-bordered w-full'
                placeholder='••••••••'
                minlength='8'
              />
            </div>

            <div>
              <label class='label'>
                <span class='label-text font-bold'>Confirmar Contraseña</span>
              </label>
              <input
                v-model='passwordForm.password_confirmation'
                type='password'
                class='input input-bordered w-full'
                placeholder='••••••••'
              />
            </div>
          </div>

          <div v-if='message' class='alert' :class='messageType'>
            <span>{{ message }}</span>
          </div>

          <div class='card-actions justify-end mt-6'>
            <button
              @click='updateProfile'
              class='btn btn-primary'
              :disabled='loading'
            >
              <span v-if='loading' class='loading loading-spinner'></span>
              <span v-else>Guardar Cambios</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import AppLayout from '../components/layout/AppLayout.vue';
import axios from 'axios';

const authStore = useAuthStore();

const profileForm = ref({
  name: '',
});

const passwordForm = ref({
  password: '',
  password_confirmation: '',
});

const loading = ref(false);
const message = ref(null);
const messageType = ref('alert-success');

const userInitials = computed(() => {
  if (!authStore.user) return '?';
  return authStore.user.name.split(' ').map(n => n[0]).join('').toUpperCase();
});

const roleLabel = computed(() => {
  const roles = {
    admin: 'Administrador',
    instructor: 'Instructor',
    student: 'Estudiante',
  };
  return roles[authStore.user?.role] || '';
});

const formatDate = (date) => {
  if (!date) return 'N/A';
  return new Date(date).toLocaleString('es-MX', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const updateProfile = async () => {
  try {
    loading.value = true;
    message.value = null;

    const updateData = {};

    if (profileForm.value.name !== authStore.user?.name) {
      updateData.name = profileForm.value.name;
    }

    if (passwordForm.value.password) {
      if (passwordForm.value.password !== passwordForm.value.password_confirmation) {
        messageType.value = 'alert-error';
        message.value = 'Las contraseñas no coinciden';
        return;
      }
      updateData.password = passwordForm.value.password;
      updateData.password_confirmation = passwordForm.value.password_confirmation;
    }

    if (Object.keys(updateData).length === 0) {
      messageType.value = 'alert-warning';
      message.value = 'No hay cambios para guardar';
      return;
    }

    await axios.put(`/api/users/${authStore.user.id}`, updateData);

    // Actualizar usuario en el store
    if (updateData.name) {
      authStore.user.name = updateData.name;
    }

    // Limpiar formulario de contraseña
    passwordForm.value.password = '';
    passwordForm.value.password_confirmation = '';

    messageType.value = 'alert-success';
    message.value = 'Perfil actualizado exitosamente';
  } catch (error) {
    messageType.value = 'alert-error';
    message.value = error.response?.data?.message || 'Error al actualizar perfil';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  if (authStore.user) {
    profileForm.value.name = authStore.user.name;
  }
});
</script>
