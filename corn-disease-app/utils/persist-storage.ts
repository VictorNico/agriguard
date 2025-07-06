// utils/persist-storage.ts
import { Capacitor } from '@capacitor/core'
import { Preferences } from '@capacitor/preferences'

// 📦 Définir le storage hybride une seule fois
export const capacitorStorage = {
    async getItem(key: string) {
        if (Capacitor.isNativePlatform()) {
            const { value } = await Preferences.get({ key })
            return value
        } else {
            return localStorage.getItem(key)
        }
    },

    async setItem(key: string, value: string) {
        if (Capacitor.isNativePlatform()) {
            await Preferences.set({ key, value })
        } else {
            localStorage.setItem(key, value)
        }
    },

    async removeItem(key: string) {
        if (Capacitor.isNativePlatform()) {
            await Preferences.remove({ key })
        } else {
            localStorage.removeItem(key)
        }
    }
}


