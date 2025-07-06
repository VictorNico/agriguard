<!-- pages/index.vue -->
<template>
  <div class="home-page">
    <div class="header">
      <h1>🌽 Corn Disease Detection</h1>
      <p>Détection intelligente des maladies du maïs</p>
    </div>

    <div class="status-section">
      <div class="status-card">
        <h3>État de l'application</h3>
        <div class="status-item">
          <span class="label">Plateforme:</span>
          <span class="value">{{ $capacitor?.platform || 'Web' }}</span>
        </div>
        <div class="status-item">
          <span class="label">TensorFlow.js:</span>
          <span class="value" :class="{ ready: tfReady, loading: !tfReady }">
            {{ tfReady ? 'Prêt' : 'Chargement...' }}
          </span>
        </div>
        <div class="status-item">
          <span class="label">Caméra:</span>
          <span class="value" :class="{ ready: cameraReady || !isNative.value, loading: !cameraReady && isNative.value }">
            {{ cameraReady  || !isNative ? 'Disponible' : 'Vérification...' }}
          </span>
        </div>
      </div>
    </div>

    <div class="actions">
      <button
          @click="startScan"
          :disabled="!isAppReady && isNative.value"
          class="scan-button"
      >
        {{ isAppReady || !isNative.value ? '📸 Commencer l\'analyse' : '⏳ Préparation...' }}
      </button>

      <button
          v-if="isNative.value"
          @click="showSplashAgain"
          class="test-button"
      >
        🔄 Tester le splash screen
      </button>
    </div>
  </div>
</template>

<script setup>
import { Camera } from '@capacitor/camera'
import * as tf from '@tensorflow/tfjs'
import {Capacitor} from "@capacitor/core";

const { show: showSplash, hide: hideSplash, updateProgress } = useSplashScreen()
// État pour le splash screen web
const isNative = ref(Capacitor.isNativePlatform())
// États réactifs
const tfReady = ref(false)
const cameraReady = ref(false)
const isAppReady = computed(() => tfReady.value && cameraReady.value)

// Initialisation au montage
onMounted(async () => {
  await initializeApp()
})

// Fonction d'initialisation complète
const initializeApp = async () => {
  console.log('Initialisation de l\'application...')

  // Vérifier TensorFlow.js
  try {
    await tf.ready()
    tfReady.value = true
    console.log('TensorFlow.js prêt')
  } catch (error) {
    console.error('Erreur TensorFlow.js:', error)
  }

  // Vérifier la caméra
  if (!isNative.value) {
    cameraReady.value = true
  }
  else{
    try {
      const permissions = await Camera.requestPermissions()
      cameraReady.value = permissions.camera === 'granted'
      console.log('Permissions caméra:', permissions)
    } catch (error) {
      console.error('Erreur permissions caméra:', error)
    }
  }
}

// Démarrer l'analyse
const startScan = async () => {
  if (!isAppReady.value) return

  console.log('Démarrage de l\'analyse...')
  await navigateTo('/analyze')
}

// Tester le splash screen
const showSplashAgain = async () => {
  await showSplash()

  // Simuler un chargement
  const steps = [
    { progress: 25, message: 'Rechargement des composants...', delay: 800 },
    { progress: 50, message: 'Mise à jour du modèle...', delay: 1000 },
    { progress: 75, message: 'Finalisation...', delay: 600 },
    { progress: 100, message: 'Terminé !', delay: 400 }
  ]

  for (const step of steps) {
    updateProgress(step.progress, step.message)
    await new Promise(resolve => setTimeout(resolve, step.delay))
  }

  await hideSplash()
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 2.5rem;
  color: #2E7D32;
  margin: 0 0 1rem 0;
}

.header p {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
}

.status-section {
  max-width: 500px;
  margin: 0 auto 3rem auto;
}

.status-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.status-card h3 {
  margin: 0 0 1.5rem 0;
  color: #333;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.status-item:last-child {
  margin-bottom: 0;
}

.label {
  font-weight: 500;
  color: #666;
}

.value {
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.value.ready {
  background: #d4edda;
  color: #155724;
}

.value.loading {
  background: #fff3cd;
  color: #856404;
}

.actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  max-width: 300px;
  margin: 0 auto;
}

.scan-button {
  width: 100%;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: white;
  background: #4CAF50;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(76, 175, 80, 0.3);
}

.scan-button:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(76, 175, 80, 0.4);
}

.scan-button:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.test-button {
  padding: 0.75rem 1.5rem;
  font-size: 0.9rem;
  color: #666;
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.test-button:hover {
  border-color: #4CAF50;
  color: #4CAF50;
}

/* Responsive */
@media (max-width: 768px) {
  .home-page {
    padding: 1rem;
  }

  .header h1 {
    font-size: 2rem;
  }

  .status-card {
    padding: 1.5rem;
  }
}
</style>