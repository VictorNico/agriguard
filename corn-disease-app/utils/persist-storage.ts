import { Capacitor } from '@capacitor/core'

// Version synchrone pour pinia-plugin-persistedstate
export const capacitorStorageSync = {
    getItem(key: string): string | null {
        try {
            // Pour Pinia, on utilise seulement localStorage (synchrone)
            // et on gère Capacitor séparément
            return localStorage.getItem(key)
        } catch (error) {
            console.error('Erreur getItem:', error)
            return null
        }
    },

    setItem(key: string, value: string): void {

        try {
            // Sauvegarder dans localStorage (synchrone)
            localStorage.setItem(key, value)

            // Sauvegarder dans Capacitor en arrière-plan (asynchrone)
            if (Capacitor.isNativePlatform()) {
                import('@capacitor/preferences').then(({ Preferences }) => {
                    Preferences.set({ key, value }).catch(console.error)
                })
            }
        } catch (error) {
            console.error('Erreur setItem:', error)
        }
    },

    removeItem(key: string): void {
        try {
            localStorage.removeItem(key)

            // Supprimer aussi de Capacitor en arrière-plan
            if (Capacitor.isNativePlatform()) {
                import('@capacitor/preferences').then(({ Preferences }) => {
                    Preferences.remove({ key }).catch(console.error)
                })
            }
        } catch (error) {
            console.error('Erreur removeItem:', error)
        }
    }
}

// Version asynchrone pour usage manuel
export const capacitorStorageAsync = {
    async getItem(key: string): Promise<string | null> {
        try {
            if (Capacitor.isNativePlatform()) {
                const { Preferences } = await import('@capacitor/preferences')
                const { value } = await Preferences.get({ key })
                return value
            } else {
                return localStorage.getItem(key)
            }
        } catch (error) {
            console.error('Erreur getItem:', error)
            return null
        }
    },

    async setItem(key: string, value: string): Promise<void> {
        try {
            if (Capacitor.isNativePlatform()) {
                const { Preferences } = await import('@capacitor/preferences')
                await Preferences.set({ key, value })
                // Aussi sauvegarder dans localStorage pour la cohérence
                localStorage.setItem(key, value)
            } else {
                localStorage.setItem(key, value)
            }
        } catch (error) {
            console.error('Erreur setItem:', error)
        }
    },

    async removeItem(key: string): Promise<void> {
        try {
            if (Capacitor.isNativePlatform()) {
                const { Preferences } = await import('@capacitor/preferences')
                await Preferences.remove({ key })
                localStorage.removeItem(key)
            } else {
                localStorage.removeItem(key)
            }
        } catch (error) {
            console.error('Erreur removeItem:', error)
        }
    }
}

// Helper pour synchroniser localStorage vers Capacitor au démarrage
export const syncStorageToCapacitor = async () => {
    if (Capacitor.isNativePlatform()) {
        try {
            const { Preferences } = await import('@capacitor/preferences')

            // Parcourir localStorage et synchroniser avec Capacitor
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i)
                if (key) {
                    const value = localStorage.getItem(key)
                    if (value) {
                        await Preferences.set({ key, value })
                    }
                }
            }
        } catch (error) {
            console.error('Erreur lors de la synchronisation:', error)
        }
    }
}

// Helper pour synchroniser Capacitor vers localStorage au démarrage
export const syncCapacitorToStorage = async () => {
    if (Capacitor.isNativePlatform()) {
        try {
            const { Preferences } = await import('@capacitor/preferences')

            // Obtenir toutes les clés de Capacitor
            const { keys } = await Preferences.keys()

            // Synchroniser chaque clé
            for (const key of keys) {
                const { value } = await Preferences.get({ key })
                if (value) {
                    localStorage.setItem(key, value)
                }
            }
        } catch (error) {
            console.error('Erreur lors de la synchronisation:', error)
        }
    }
}
