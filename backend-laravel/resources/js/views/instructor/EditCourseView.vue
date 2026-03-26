<template>
  <AppLayout>
    <div class="container mx-auto max-w-3xl">
      <div class="flex items-center mb-8">
        <router-link :to="`/instructor/courses/${route.params.id}`" class="btn btn-ghost btn-circle mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </router-link>
        <h1 class="text-4xl font-bold">Editar Curso</h1>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-8">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <!-- Formulario -->
      <div v-else class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <form @submit.prevent="handleSubmit">
            <div v-if="error" class="alert alert-error mb-4">
              <span>{{ error }}</span>
            </div>

            <div v-if="success" class="alert alert-success mb-4">
              <span>{{ success }}</span>
            </div>

            <!-- Título -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-bold">Título del Curso *</span>
              </label>
              <input
                v-model="form.title"
                type="text"
                placeholder="Título del curso"
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
                placeholder="Descripción del curso"
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
                <span class="label-text font-bold">Estado</span>
              </label>
              <select v-model="form.status" class="select select-bordered">
                <option value="draft">Borrador</option>
                <option value="active">Activo</option>
                <option value="inactive">Inactivo</option>
                <option value="completed">Completado</option>
              </select>
            </div>

            <div class="divider"></div>

            <div class="card-actions justify-end">
              <router-link :to="`/instructor/courses/${route.params.id}`" class="btn btn-outline">
                Cancelar
              </router-link>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="saving"
              >
                <span v-if="saving" class="loading loading-spinner"></span>
                <span v-else>Guardar Cambios</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '../../stores/courses';
import AppLayout from '../../components/layout/AppLayout.vue';

const route = useRoute();
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

const loading = ref(true);
const saving = ref(false);
const error = ref(null);
const success = ref(null);

const addObjective = () => {
  form.value.learning_objectives.push('');
};

const removeObjective = (index) => {
  form.value.learning_objectives.splice(index, 1);
};

const formatDateForInput = (date) => {
  if (!date) return '';
  const d = new Date(date);
  return d.toISOString().split('T')[0];
};

const handleSubmit = async () => {
  error.value = null;
  success.value = null;

  // Filtrar objetivos vacíos
  const objectives = form.value.learning_objectives.filter(obj => obj.trim() !== '');

  try {
    saving.value = true;
    const courseData = {
      ...form.value,
      learning_objectives: objectives.length > 0 ? objectives : null,
    };

    await courseStore.updateCourse(route.params.id, courseData);
    success.value = 'Curso actualizado exitosamente';

    setTimeout(() => {
      router.push(`/instructor/courses/${route.params.id}`);
    }, 1500);
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al actualizar el curso';
  } finally {
    saving.value = false;
  }
};

onMounted(async () => {
  try {
    loading.value = true;
    const course = await courseStore.fetchCourse(route.params.id);

    form.value = {
      title: course.title,
      description: course.description,
      learning_objectives: course.learning_objectives && course.learning_objectives.length > 0
        ? [...course.learning_objectives]
        : [''],
      start_date: formatDateForInput(course.start_date),
      end_date: formatDateForInput(course.end_date),
      status: course.status,
    };
  } catch (error) {
    console.error('Error al cargar curso:', error);
  } finally {
    loading.value = false;
  }
});
</script>
