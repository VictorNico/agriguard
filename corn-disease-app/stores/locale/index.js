// stores/locale.ts
import { defineStore } from 'pinia'

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
        key:'locale',
        paths: ['language'] // facultatif ici, mais utile si tu as d'autres props
    }
})
