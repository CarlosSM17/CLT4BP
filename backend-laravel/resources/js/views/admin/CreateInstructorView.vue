<template>
  <AppLayout>
    <div class='container mx-auto max-w-2xl'>
      <div class='flex items-center mb-8'>
        <router-link to='/admin/users' class='btn btn-ghost btn-circle mr-4'>
          <svg xmlns='http://www.w3.org/2000/svg' class='h-6 w-6' fill='none' viewBox='0 0 24 24' stroke='currentColor'>
            <path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15 19l-7-7 7-7' />
          </svg>
        </router-link>
        <h1 class='text-4xl font-bold'>Crear Nuevo Instructor</h1>
      </div>

      <div class='card bg-base-100 shadow-xl'>
        <div class='card-body'>
          <form @submit.prevent='handleSubmit'>
            <div v-if='error' class='alert alert-error mb-4'>
              <svg xmlns='http://www.w3.org/2000/svg' class='stroke-current shrink-0 h-6 w-6' fill='none' viewBox='0 0 24 24'>
                <path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z' />
              </svg>
              <span>{{ error }}</span>
            </div>

            <div v-if='success' class='alert alert-success mb-4'>
              <svg xmlns='http://www.w3.org/2000/svg' class='stroke-current shrink-0 h-6 w-6' fill='none' viewBox='0 0 24 24'>
                <path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' />
              </svg>
              <span>{{ success }}</span>
            </div>

            <div class='form-control'>
              <label class='label'>
                <span class='label-text font-bold'>Nombre Completo *</span>
              </label>
              <input
                v-model='form.name'
                type='text'
                placeholder='Ej: Juan Pérez García'
                class='input input-bordered'
                required
              />
              <label class='label'>
                <span class='label-text-alt'>Nombre completo del instructor</span>
              </label>
            </div>

            <div class='form-control'>
              <label class='label'>
                <span class='label-text font-bold'>Email *</span>
              </label>
              <input
                v-model='form.email'
                type='email'
                placeholder='instructor@ejemplo.com'
                class='input input-bordered'
                required
              />
              <label class='label'>
                <span class='label-text-alt'>Email institucional del instructor</span>
              </label>
            </div>

            <div class='form-control'>
              <label class='label'>
                <span class='label-text font-bold'>Contraseña *</span>
              </label>
              <input
                v-model='form.password'
                type='password'
                placeholder='••••••••'
                class='input input-bordered'
                required
                minlength='8'
              />
              <label class='label'>
                <span class='label-text-alt'>Mínimo 8 caracteres</span>
              </label>
            </div>

            <div class='form-control'>
              <label class='label'>
                <span class='label-text font-bold'>Confirmar Contraseña *</span>
              </label>
              <input
                v-model='form.password_confirmation'
                type='password'
                placeholder='••••••••'
                class='input input-bordered'
                required
              />
            </div>

            <div class='alert alert-info mt-6'>
              <svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' class='stroke-current shrink-0 w-6 h-6'>
                <path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'></path>
              </svg>
              <div>
                <h3 class='font-bold'>Información</h3>
                <div class='text-xs'>
                  El instructor podrá crear cursos, asignar estudiantes y generar material instruccional con IA.
                </div>
              </div>
            </div>

            <div class='divider'></div>

            <div class='card-actions justify-end'>
              <router-link to='/admin/users' class='btn btn-outline'>
                Cancelar
              </router-link>
              <button
                type='submit'
                class='btn btn-primary'
                :disabled='loading'
              >
                <span v-if='loading' class='loading loading-spinner'></span>
                <span v-else>Crear Instructor</span>
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Información adicional -->
      <div class='card bg-base-100 shadow-xl mt-6'>
        <div class='card-body'>
          <h2 class='card-title'>Permisos del Instructor</h2>
          <ul class='list-disc list-inside space-y-2'>
            <li>Crear y editar cursos</li>
            <li>Asignar estudiantes a cursos</li>
            <li>Configurar evaluaciones y cuestionarios</li>
            <li>Generar material instruccional con IA</li>
            <li>Activar/desactivar contenidos</li>
            <li>Consultar reportes y análisis</li>
          </ul>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import AppLayout from '../../components/layout/AppLayout.vue';
import axios from 'axios';

const router = useRouter();

const form = ref({
  name: '',
  email: '',
  password: '',
  password_confirmation: '',
});

const loading = ref(false);
const error = ref(null);
const success = ref(null);

const handleSubmit = async () => {
  error.value = null;
  success.value = null;

  // Validar que las contraseñas coincidan
  if (form.value.password !== form.value.password_confirmation) {
    error.value = 'Las contraseñas no coinciden';
    return;
  }

  try {
    loading.value = true;

    const response = await axios.post('/api/users/instructors', form.value);

    success.value = `Instructor ${response.data.user.name} creado exitosamente`;

    // Limpiar formulario
    form.value = {
      name: '',
      email: '',
      password: '',
      password_confirmation: '',
    };

    // Redirigir después de 2 segundos
    setTimeout(() => {
      router.push('/admin/users');
    }, 2000);

  } catch (err) {
    if (err.response?.data?.errors) {
      // Mostrar errores de validación
      const errors = Object.values(err.response.data.errors).flat();
      error.value = errors.join(', ');
    } else {
      error.value = err.response?.data?.message || 'Error al crear instructor';
    }
  } finally {
    loading.value = false;
  }
};
</script>
