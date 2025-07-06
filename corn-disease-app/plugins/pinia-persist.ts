import type { Pinia } from 'pinia'
import { createPersistedState } from 'pinia-plugin-persistedstate'
import { capacitorStorageSync, syncCapacitorToStorage } from '~/utils/persist-storage'

export default defineNuxtPlugin(async (nuxtApp) => {
    // Synchroniser Capacitor vers localStorage au démarrage
    await syncCapacitorToStorage()

    // Configurer le plugin avec le storage synchrone
    const pinia = nuxtApp.$pinia as Pinia
    pinia.use(createPersistedState({
        storage: capacitorStorageSync,
        serializer: {
            serialize: JSON.stringify,
            deserialize: JSON.parse
        }
    }))

})