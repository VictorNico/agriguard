// composables/useHybridClassifier.js
import { ref, computed, watch } from 'vue'

export const useHybridClassifier = () => {
    // États partagés
    const isOnline = ref(navigator.onLine)
    const isAnalyzing = ref(false)
    const classificationResults = ref(null)
    const errorMessage = ref(null)
    const currentMode = ref('auto') // 'auto', 'online', 'offline'

    // Importer le composable local
    const {
        modelLoaded,
        isLoading: isLoadingModel,
        error: modelError,
        loadModel,
        classify: classifyLocal,
        classifyBatch: classifyBatchLocal,
        getModelInfo
    } = useMaizeClassifier()

    // Configuration
    const config = useRuntimeConfig()
    const { t } = useI18n()

    // Statut de connexion
    const updateOnlineStatus = () => {
        isOnline.value = navigator.onLine
    }

    // Vérifier la connectivité avec le backend
    const checkBackendConnection = async () => {
        try {
            const response = await fetch(`${config.public.apiBase}/api/health`, {
                method: 'HEAD',
                timeout: 5000
            })
            return response.ok
        } catch {
            return false
        }
    }

    // Déterminer le mode de classification
    const classificationMode = computed(() => {
        if (currentMode.value === 'online') return 'online'
        if (currentMode.value === 'offline') return 'offline'

        // Mode auto : online si connecté, offline sinon
        return isOnline.value ? 'online' : 'offline'
    })

    // Statut du service
    const serviceStatus = computed(() => {
        const mode = classificationMode.value

        if (mode === 'online') {
            return {
                mode: 'online',
                available: isOnline.value,
                description: isOnline.value ?
                    'Classification via API backend' :
                    'Backend non disponible',
                icon: 'heroicons:cloud',
                color: isOnline.value ? 'green' : 'red'
            }
        } else {
            return {
                mode: 'offline',
                available: modelLoaded.value,
                description: modelLoaded.value ?
                    'Classification locale (TensorFlow.js)' :
                    'Modèle local non chargé',
                icon: 'heroicons:cpu-chip',
                color: modelLoaded.value ? 'blue' : 'orange'
            }
        }
    })

    // Classification via API backend
    const classifyOnline = async (imageData) => {
        try {
            const response = await fetch(imageData)
            const blob = await response.blob()
            const formData = new FormData()
            formData.append('image', blob, 'image.jpg')

            const apiResponse = await fetch(`${config.public.apiBase}/api/classify`, {
                method: 'POST',
                body: formData
            })

            if (!apiResponse.ok) {
                throw new Error(`HTTP ${apiResponse.status}`)
            }

            const result = await apiResponse.json()

            if (!result.success) {
                throw new Error(result.error || 'Erreur de classification')
            }

            return result

        } catch (error) {
            console.error('Erreur classification online:', error)
            throw error
        }
    }

    // Classification batch via API backend
    const classifyBatchOnline = async (imagesData) => {
        try {
            const formData = new FormData()

            for (let i = 0; i < imagesData.length; i++) {
                const response = await fetch(imagesData[i])
                const blob = await response.blob()
                formData.append('images', blob, `image_${i}.jpg`)
            }

            const apiResponse = await fetch(`${config.public.apiBase}/api/classify/batch`, {
                method: 'POST',
                body: formData
            })

            if (!apiResponse.ok) {
                throw new Error(`HTTP ${apiResponse.status}`)
            }

            const result = await apiResponse.json()

            if (!result.success) {
                throw new Error(result.error || 'Erreur de classification batch')
            }

            return result

        } catch (error) {
            console.error('Erreur classification batch online:', error)
            throw error
        }
    }

    // Classification hybride avec fallback automatique
    const classify = async (imageData) => {
        if (!imageData) {
            throw new Error('Aucune image fournie')
        }

        isAnalyzing.value = true
        errorMessage.value = null

        try {
            const mode = classificationMode.value

            if (mode === 'online') {
                // Tenter d'abord la classification online
                try {
                    const result = await classifyOnline(imageData)
                    return result
                } catch (error) {
                    console.warn('Classification online échouée, fallback vers offline:', error)

                    // Fallback vers le mode offline si le modèle est chargé
                    if (modelLoaded.value) {
                        const blob = await fetch(imageData).then(r => r.blob())
                        return await classifyLocal(blob)
                    } else {
                        throw error
                    }
                }
            } else {
                // Mode offline
                if (!modelLoaded.value) {
                    throw new Error('Modèle local non chargé')
                }

                const blob = await fetch(imageData).then(r => r.blob())
                return await classifyLocal(blob)
            }

        } catch (error) {
            console.error('Erreur classification hybride:', error)
            throw error
        } finally {
            isAnalyzing.value = false
        }
    }

    // Classification batch hybride
    const classifyBatch = async (imagesData) => {
        if (!imagesData || imagesData.length === 0) {
            throw new Error('Aucune image fournie')
        }

        isAnalyzing.value = true
        errorMessage.value = null

        try {
            const mode = classificationMode.value

            if (mode === 'online') {
                // Tenter d'abord la classification online
                try {
                    const result = await classifyBatchOnline(imagesData)
                    return result
                } catch (error) {
                    console.warn('Classification batch online échouée, fallback vers offline:', error)

                    // Fallback vers le mode offline si le modèle est chargé
                    if (modelLoaded.value) {
                        const blobs = []
                        for (const imageUrl of imagesData) {
                            const blob = await fetch(imageUrl).then(r => r.blob())
                            blobs.push(blob)
                        }
                        const results = await classifyBatchLocal(blobs)
                        return {
                            success: true,
                            results: results,
                            timestamp: new Date().toISOString()
                        }
                    } else {
                        throw error
                    }
                }
            } else {
                // Mode offline
                if (!modelLoaded.value) {
                    throw new Error('Modèle local non chargé')
                }

                const blobs = []
                for (const imageUrl of imagesData) {
                    const blob = await fetch(imageUrl).then(r => r.blob())
                    blobs.push(blob)
                }
                const results = await classifyBatchLocal(blobs)
                return {
                    success: true,
                    results: results,
                    timestamp: new Date().toISOString()
                }
            }

        } catch (error) {
            console.error('Erreur classification batch hybride:', error)
            throw error
        } finally {
            isAnalyzing.value = false
        }
    }

    // Initialiser le service
    const initializeService = async () => {
        try {
            // Vérifier la connectivité
            updateOnlineStatus()

            // Toujours essayer de charger le modèle local pour le fallback
            if (process.client && !modelLoaded.value) {
                console.log('Chargement du modèle local pour fallback...')
                await loadModel('/models/model.json')
            }

            // Vérifier la connectivité backend si online
            if (isOnline.value) {
                const backendAvailable = await checkBackendConnection()
                if (!backendAvailable) {
                    console.warn('Backend non disponible, utilisation du mode offline')
                    isOnline.value = false
                }
            }

        } catch (error) {
            console.error('Erreur initialisation service:', error)
            errorMessage.value = 'Erreur lors de l\'initialisation du service'
        }
    }

    // Forcer un mode spécifique
    const setMode = (mode) => {
        if (['auto', 'online', 'offline'].includes(mode)) {
            currentMode.value = mode
        }
    }

    // Gérer les erreurs API
    const handleApiError = (error) => {
        if (error.message.includes('HTTP')) {
            return 'Erreur serveur'
        } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
            return 'Erreur réseau'
        } else {
            return 'Erreur lors de l\'analyse'
        }
    }

    // Watchers pour la connectivité
    if (process.client) {
        window.addEventListener('online', updateOnlineStatus)
        window.addEventListener('offline', updateOnlineStatus)

        // Nettoyer les listeners à la destruction
        onUnmounted(() => {
            window.removeEventListener('online', updateOnlineStatus)
            window.removeEventListener('offline', updateOnlineStatus)
        })
    }

    // Surveiller les changements de connectivité
    watch(isOnline, (newValue) => {
        if (newValue) {
            // Vérifier la connectivité backend quand on revient online
            checkBackendConnection().then(available => {
                if (!available) {
                    isOnline.value = false
                }
            })
        }
    })

    return {
        // États
        isOnline: readonly(isOnline),
        isAnalyzing: readonly(isAnalyzing),
        classificationResults: readonly(classificationResults),
        errorMessage: readonly(errorMessage),
        currentMode: readonly(currentMode),
        classificationMode: readonly(classificationMode),
        serviceStatus: readonly(serviceStatus),

        // États du modèle local
        modelLoaded: readonly(modelLoaded),
        isLoadingModel: readonly(isLoadingModel),
        modelError: readonly(modelError),

        // Méthodes
        classify,
        classifyBatch,
        initializeService,
        setMode,
        checkBackendConnection,
        updateOnlineStatus,
        handleApiError,

        // Méthodes du modèle local
        getModelInfo
    }
}