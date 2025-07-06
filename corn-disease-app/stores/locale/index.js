// stores/locale.ts
import { defineStore } from 'pinia'
import { capacitorStorage } from '~/utils/persist-storage.js'

export const useLocaleStore = defineStore('locale', {
    state: () => ({
        language: 'fr' // langue par défaut
    }),
    actions: {
        setLanguage(lang) {
            this.language = lang
        }
    },
    persist: {
        storage: capacitorStorage,
        paths: ['language'] // facultatif ici, mais utile si tu as d'autres props
    }
})
