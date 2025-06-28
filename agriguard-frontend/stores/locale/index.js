import { defineStore } from 'pinia';

export const useLocaleStore = defineStore('locale', {
    state: () => ({
        language: 'fr', // Langue par défaut
    }),
    actions: {
        setLanguage(lang) {
            this.language = lang;
        },
    },
    persist: true,
});
