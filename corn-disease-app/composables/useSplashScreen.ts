// composables/useSplashScreen.ts
import { SplashScreen } from '@capacitor/splash-screen'
import { Capacitor } from '@capacitor/core'

export const useSplashScreen = () => {
    const isShowing = ref(true)
    const progress = ref(0)
    const message = ref('Initialisation...')

    // Afficher le splash screen
    const show = async () => {
        if (Capacitor.isNativePlatform()) {
            try {
                await SplashScreen.show({
                    showDuration: 0, // Durée infinie, contrôle manuel
                    autoHide: false
                })
                isShowing.value = true
            } catch (error) {
                console.error('Erreur affichage splash screen:', error)
            }
        } else {
            // Pour PWA, afficher l'élément web
            isShowing.value = true
        }
    }

    // Masquer le splash screen
    const hide = async () => {
        if (Capacitor.isNativePlatform()) {
            try {
                await SplashScreen.hide()
                isShowing.value = false
            } catch (error) {
                console.error('Erreur masquage splash screen:', error)
            }
        } else {
            // Pour PWA, transition douce
            await new Promise(resolve => setTimeout(resolve, 300))
            isShowing.value = false
        }
    }

    // Mettre à jour le progrès (pour PWA)
    const updateProgress = (newProgress: number, newMessage?: string) => {
        progress.value = newProgress
        if (newMessage) {
            message.value = newMessage
        }

        // Mettre à jour l'UI si c'est une PWA et que les éléments existent
        if (!Capacitor.isNativePlatform() && process.client) {
            nextTick(() => {
                const progressElement = document.querySelector('.splash-progress') as HTMLElement
                const messageElement = document.querySelector('.splash-message') as HTMLElement

                if (progressElement) {
                    progressElement.style.width = `${newProgress}%`
                }
                if (messageElement) {
                    messageElement.textContent = newMessage || message.value
                }
            })
        }
    }

    // Séquence de chargement avec étapes
    const loadingSequence = async () => {
        const steps = [
            { progress: 20, message: 'Initialisation des composants...', delay: 500 },
            { progress: 40, message: 'Chargement du modèle IA...', delay: 1000 },
            { progress: 60, message: 'Configuration de la caméra...', delay: 500 },
            { progress: 80, message: 'Préparation de l\'interface...', delay: 500 },
            { progress: 100, message: 'Prêt !', delay: 300 }
        ]

        for (const step of steps) {
            updateProgress(step.progress, step.message)
            await new Promise(resolve => setTimeout(resolve, step.delay))
        }

        // Attendre un peu avant de masquer
        await new Promise(resolve => setTimeout(resolve, 500))
        await hide()
    }

    return {
        isShowing: readonly(isShowing),
        progress: readonly(progress),
        message: readonly(message),
        show,
        hide,
        updateProgress,
        loadingSequence
    }
}