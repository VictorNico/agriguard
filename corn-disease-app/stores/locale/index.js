// stores/locale.ts
import { defineStore } from 'pinia'
import { capacitorStorage } from '~/plugins/persist-storage'

export const useLocaleStore = defineStore('locale', {
    state: () => ({
        language: 'fr' // langue par défaut
    }),
    actions: {
        setLanguage(lang: string) {
            this.language = lang
        }
    },
    persist: {
        storage: capacitorStorage,
        paths: ['language'] // facultatif ici, mais utile si tu as d'autres props
    }
})
