<template>
  <AppLayout>
    <div class="container mx-auto max-w-3xl">
      <div class="flex items-center mb-8">
        <router-link to="/instructor/courses" class="btn btn-ghost btn-circle mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </router-link>
        <h1 class="text-4xl font-bold">Crear Nuevo Curso</h1>
      </div>

      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <form @submit.prevent="handleSubmit">
            <div v-if="error" class="alert alert-error mb-4">
              <span>{{ error }}</span>
            </div>

            <!-- Título -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Título del Curso *</span>
              </label>
              <input
                v-model="form.title"
                type="text"
                placeholder="Ej: Programación Básica con Python"
                class="input input-bordered"
                required
              />
            </div>

            <!-- Descripción -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Descripción *</span>
              </label>
              <textarea
                v-model="form.description"
                placeholder="Describe de qué trata el curso..."
                class="textarea textarea-bordered h-24"
                required
              ></textarea>
            </div>

            <!-- Objetivos de Aprendizaje -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Objetivos de Aprendizaje</span>
              </label>
              <div class="space-y-2">
                <div v-for="(objective, index) in form.learning_objectives" :key="index" class="flex gap-2">
                  <input
                    v-model="form.learning_objectives[index]"
                    type="text"
                    placeholder="Objetivo de aprendizaje..."
                    class="input input-bordered flex-1"
                  />
                  <button
                    type="button"
                    @click="removeObjective(index)"
                    class="btn btn-error btn-square"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                <button type="button" @click="addObjective" class="btn btn-outline btn-sm">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Agregar Objetivo
                </button>
              </div>
            </div>

            <!-- Fechas -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="form-control">
                <label class="label">
                  <span class="label-text font-bold">Fecha de Inicio</span>
                </label>
                <input
                  v-model="form.start_date"
                  type="date"
                  class="input input-bordered"
                />
              </div>

              <div class="form-control">
                <label class="label">
                  <span class="label-text font-bold">Fecha de Fin</span>
                </label>
                <input
                  v-model="form.end_date"
                  type="date"
                  class="input input-bordered"
                />
              </div>
            </div>

            <!-- Estado -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Estado Inicial</span>
              </label>
              <select v-model="form.status" class="select select-bordered">
                <option value="draft">Borrador</option>
                <option value="active">Activo</option>
                <option value="inactive">Inactivo</option>
              </select>
            </div>

            <div class="alert alert-info mt-6">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <div>
                <h3 class="font-bold">Información</h3>
                <div class="text-xs">
                  Los cursos en estado "Borrador" no serán visibles para los estudiantes.
                </div>
              </div>
            </div>

            <div class="divider"></div>

            <div class="card-actions justify-end">
              <router-link to="/instructor/courses" class="btn btn-outline">
                Cancelar
              </router-link>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="courseStore.loading"
              >
                <span v-if="courseStore.loading" class="loading loading-spinner"></span>
                <span v-else>Crear Curso</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useCourseStore } from '../../stores/courses';
import AppLayout from '../../components/layout/AppLayout.vue';

const router = useRouter();
const courseStore = useCourseStore();

const form = ref({
  title: '',
  description: '',
  learning_objectives: [''],
  start_date: '',
  end_date: '',
  status: 'draft',
});

const error = ref(null);

const addObjective = () => {
  form.value.learning_objectives.push('');
};

const removeObjective = (index) => {
  form.value.learning_objectives.splice(index, 1);
};

const handleSubmit = async () => {
  error.value = null;

  // Filtrar objetivos vacíos
  const objectives = form.value.learning_objectives.filter(obj => obj.trim() !== '');

  try {
    const courseData = {
      ...form.value,
      learning_objectives: objectives.length > 0 ? objectives : null,
    };

    await courseStore.createCourse(courseData);
    router.push('/instructor/courses');
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al crear el curso';
  }
};
</script>
