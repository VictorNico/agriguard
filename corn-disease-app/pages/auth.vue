<!-- pages/auth.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-blue-50 px-4 py-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Header -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 p-1 bg-white/90 rounded-full flex items-center justify-center flex items-center justify-center bg-green-600 rounded-full">
          <!--              <svg class="w-6 h-6 text-green-800" fill="currentColor" viewBox="0 0 24 24">-->
          <!--                <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z"/>-->
          <!--              </svg>-->
          <a href="/" class="h-full flex items-center">
            <img
                src="/logo.png"
                alt="Logo"
                class="h-full w-auto max-h-full object-contain"
            />
          </a>
        </div>
        <h2 class="mt-6 text-3xl font-bold text-gray-900">
          {{ isLogin ? t('auth.welcome_back') : t('auth.create_account') }}
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          {{ isLogin ? t('auth.login_subtitle') : t('auth.register_subtitle') }}
        </p>
      </div>

      <!-- Form -->
      <div class="bg-white py-8 px-6 shadow-xl rounded-lg space-y-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Nom et Prénom (uniquement pour l'inscription) -->
          <div v-if="!isLogin" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label for="firstName" class="block text-sm font-medium text-gray-700">
                {{ t('auth.first_name') }}
              </label>
              <input
                  id="firstName"
                  v-model="form.firstName"
                  type="text"
                  required
                  :class="[
                  'mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm',
                  errors.firstName ? 'border-red-300' : 'border-gray-300'
                ]"
                  :placeholder="t('auth.first_name_placeholder')"
              />
              <p v-if="errors.firstName" class="mt-1 text-sm text-red-600">
                {{ errors.firstName }}
              </p>
            </div>

            <div>
              <label for="lastName" class="block text-sm font-medium text-gray-700">
                {{ t('auth.last_name') }}
              </label>
              <input
                  id="lastName"
                  v-model="form.lastName"
                  type="text"
                  required
                  :class="[
                  'mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm',
                  errors.lastName ? 'border-red-300' : 'border-gray-300'
                ]"
                  :placeholder="t('auth.last_name_placeholder')"
              />
              <p v-if="errors.lastName" class="mt-1 text-sm text-red-600">
                {{ errors.lastName }}
              </p>
            </div>
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              {{ t('auth.email') }}
            </label>
            <input
                id="email"
                v-model="form.email"
                type="email"
                required
                :class="[
                'mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm',
                errors.email ? 'border-red-300' : 'border-gray-300'
              ]"
                :placeholder="t('auth.email_placeholder')"
            />
            <p v-if="errors.email" class="mt-1 text-sm text-red-600">
              {{ errors.email }}
            </p>
          </div>

          <!-- Mot de passe -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              {{ t('auth.password') }}
            </label>
            <div class="mt-1 relative">
              <input
                  id="password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  :class="[
                  'block w-full px-3 py-2 pr-10 border rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm',
                  errors.password ? 'border-red-300' : 'border-gray-300'
                ]"
                  :placeholder="t('auth.password_placeholder')"
              />
              <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <Icon
                    :name="showPassword ? 'ph:eye-slash' : 'ph:eye'"
                    class="h-4 w-4 text-gray-400"
                />
              </button>
            </div>
            <p v-if="errors.password" class="mt-1 text-sm text-red-600">
              {{ errors.password }}
            </p>
          </div>

          <!-- Confirmation du mot de passe (uniquement pour l'inscription) -->
          <div v-if="!isLogin">
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">
              {{ t('auth.confirm_password') }}
            </label>
            <div class="mt-1 relative">
              <input
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  required
                  :class="[
                  'block w-full px-3 py-2 pr-10 border rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm',
                  errors.confirmPassword ? 'border-red-300' : 'border-gray-300'
                ]"
                  :placeholder="t('auth.confirm_password_placeholder')"
              />
              <button
                  type="button"
                  @click="showConfirmPassword = !showConfirmPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <Icon
                    :name="showConfirmPassword ? 'ph:eye-slash' : 'ph:eye'"
                    class="h-4 w-4 text-gray-400"
                />
              </button>
            </div>
            <p v-if="errors.confirmPassword" class="mt-1 text-sm text-red-600">
              {{ errors.confirmPassword }}
            </p>
          </div>

          <!-- Informations supplémentaires (uniquement pour l'inscription) -->
          <div v-if="!isLogin" class="space-y-4">
            <div>
              <label for="phone" class="block text-sm font-medium text-gray-700">
                {{ t('auth.phone') }} ({{ t('auth.optional') }})
              </label>
              <input
                  id="phone"
                  v-model="form.phone"
                  type="tel"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                  :placeholder="t('auth.phone_placeholder')"
              />
            </div>

            <div>
              <label for="region" class="block text-sm font-medium text-gray-700">
                {{ t('auth.region') }} ({{ t('auth.optional') }})
              </label>
              <select
                  id="region"
                  v-model="form.region"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              >
                <option value="">{{ t('auth.select_region') }}</option>
                <option value="Adamawa">Adamawa</option>
                <option value="Centre">Centre</option>
                <option value="East">East</option>
                <option value="Far North">Far North</option>
                <option value="Littoral">Littoral</option>
                <option value="North">North</option>
                <option value="Northwest">Northwest</option>
                <option value="South">South</option>
                <option value="Southwest">Southwest</option>
                <option value="West">West</option>
              </select>
            </div>
          </div>

          <!-- Se souvenir de moi / Mot de passe oublié -->
          <div v-if="isLogin" class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                  id="remember"
                  v-model="form.remember"
                  type="checkbox"
                  class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
              <label for="remember" class="ml-2 block text-sm text-gray-900">
                {{ t('auth.remember_me') }}
              </label>
            </div>
            <button
                type="button"
                @click="handleForgotPassword"
                class="text-sm text-green-600 hover:text-green-500"
            >
              {{ t('auth.forgot_password') }}
            </button>
          </div>

          <!-- Accepter les conditions (uniquement pour l'inscription) -->
          <div v-if="!isLogin" class="flex items-center">
            <input
                id="acceptTerms"
                v-model="form.acceptTerms"
                type="checkbox"
                required
                class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
            />
            <label for="acceptTerms" class="ml-2 block text-sm text-gray-900">
              {{ t('auth.accept_terms_start') }}
              <a href="#" class="text-green-600 hover:text-green-500">
                {{ t('auth.terms_of_service') }}
              </a>
              {{ t('auth.and') }}
              <a href="#" class="text-green-600 hover:text-green-500">
                {{ t('auth.privacy_policy') }}
              </a>
            </label>
          </div>

          <!-- Bouton de soumission -->
          <button
              type="submit"
              :disabled="loading"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Icon
                v-if="loading"
                name="ph:circle-notch"
                class="animate-spin h-4 w-4 mr-2"
            />
            {{ loading ? t('auth.processing') : (isLogin ? t('auth.login') : t('auth.register')) }}
          </button>
        </form>

        <!-- Divider -->
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300" />
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">{{ t('auth.or') }}</span>
          </div>
        </div>

        <!-- Toggle entre login et register -->
        <div class="text-center">
          <button
              type="button"
              @click="toggleMode"
              class="text-green-600 hover:text-green-500 font-medium"
          >
            {{ isLogin ? t('auth.no_account') : t('auth.have_account') }}
          </button>
        </div>
      </div>

      <!-- Alert pour les erreurs -->
      <div
          v-if="alert.show"
          :class="[
          'rounded-md p-4',
          alert.type === 'error' ? 'bg-red-50 border border-red-200' : 'bg-green-50 border border-green-200'
        ]"
      >
        <div class="flex">
          <Icon
              :name="alert.type === 'error' ? 'ph:warning-circle' : 'ph:check-circle'"
              :class="[
              'h-5 w-5',
              alert.type === 'error' ? 'text-red-400' : 'text-green-400'
            ]"
          />
          <div class="ml-3">
            <p :class="[
              'text-sm font-medium',
              alert.type === 'error' ? 'text-red-800' : 'text-green-800'
            ]">
              {{ alert.message }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth'

// Meta
definePageMeta({
  // layout: 'auth',
  middleware: 'guest'
})

// Composables
const { t } = useI18n()
const { $i18n } = useNuxtApp()
const authStore = useAuthStore()

// State
const isLogin = ref(true)
const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)

// Form data
const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  phone: '',
  region: '',
  remember: false,
  acceptTerms: false
})

// Errors
const errors = ref({})

// Alert
const alert = ref({
  show: false,
  type: 'error',
  message: ''
})

// Methods
const validateForm = () => {
  errors.value = {}

  if (!isLogin.value) {
    if (!form.value.firstName.trim()) {
      errors.value.firstName = t('auth.errors.first_name_required')
    }

    if (!form.value.lastName.trim()) {
      errors.value.lastName = t('auth.errors.last_name_required')
    }

    if (form.value.password !== form.value.confirmPassword) {
      errors.value.confirmPassword = t('auth.errors.password_mismatch')
    }
  }

  if (!form.value.email.trim()) {
    errors.value.email = t('auth.errors.email_required')
  } else if (!/\S+@\S+\.\S+/.test(form.value.email)) {
    errors.value.email = t('auth.errors.email_invalid')
  }

  if (!form.value.password.trim()) {
    errors.value.password = t('auth.errors.password_required')
  } else if (form.value.password.length < 8) {
    errors.value.password = t('auth.errors.password_min_length')
  }

  return Object.keys(errors.value).length === 0
}

const showAlert = (type, message) => {
  alert.value = {
    show: true,
    type,
    message
  }

  setTimeout(() => {
    alert.value.show = false
  }, 5000)
}

const handleSubmit = async () => {
  if (!validateForm()) return

  loading.value = true

  try {
    if (isLogin.value) {
      await authStore.login({
        email: form.value.email,
        password: form.value.password
      })

      showAlert('success', t('auth.login_success'))

      // Redirection après connexion
      setTimeout(() => {
        // navigateTo('/dashboard')
        navigateTo('/')
      }, 1000)
    } else {
      await authStore.register({
        email: form.value.email,
        password: form.value.password,
        first_name: form.value.firstName,
        last_name: form.value.lastName,
        phone: form.value.phone,
        region: form.value.region,
        language: $i18n.locale.value,
        country: 'CM'
      })

      showAlert('success', t('auth.register_success'))

      // Redirection après inscription
      setTimeout(() => {
        // navigateTo('/dashboard')
        navigateTo('/')
      }, 1000)
    }
  } catch (error) {
    console.error('Auth error:', error)

    let errorMessage = t('auth.errors.generic')

    if (error.response?.data?.error) {
      errorMessage = error.response.data.error
    } else if (error.message) {
      errorMessage = error.message
    }

    showAlert('error', errorMessage)
  } finally {
    loading.value = false
  }
}

const toggleMode = () => {
  isLogin.value = !isLogin.value
  // Reset form
  form.value = {
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
    region: '',
    remember: false,
    acceptTerms: false
  }
  errors.value = {}
  alert.value.show = false
}

const handleForgotPassword = () => {
  // Implement forgot password logic
  showAlert('info', t('auth.forgot_password_sent'))
}

// Watchers
watch(() => form.value.email, () => {
  if (errors.value.email) {
    delete errors.value.email
  }
})

watch(() => form.value.password, () => {
  if (errors.value.password) {
    delete errors.value.password
  }
})

watch(() => form.value.confirmPassword, () => {
  if (errors.value.confirmPassword) {
    delete errors.value.confirmPassword
  }
})

// Head
useHead({
  title: computed(() => isLogin.value ? t('auth.login_title') : t('auth.register_title')),
  meta: [
    {
      name: 'description',
      content: computed(() => isLogin.value ? t('auth.login_description') : t('auth.register_description'))
    }
  ]
})
</script>

<style scoped>
/* Animations personnalisées */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Styles pour les inputs focus */
input:focus,
select:focus {
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

/* Animation pour le bouton de soumission */
button[type="submit"]:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
}

button[type="submit"] {
  transition: all 0.2s ease;
}
</style>