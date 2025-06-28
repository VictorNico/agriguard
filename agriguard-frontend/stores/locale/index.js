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
    //     {
    //     // Enable cache
    //     enabled: true,
    //     storage: sessionStorage,
    //     // strategies: [
    //     //     // {
    //     //     //     key: 'cookieLanguage', // The default key is the ID of the above store. You can customize the key
    //     //     //     storage: 'cookie', // Default cookie
    //     //     //     // paths: ['cookieLanguage'], // You can select multiple
    //     //     // },
    //     //     {
    //     //         key: 'localStorageLanguage', // The default key is the ID of the above store. You can customize the key
    //     //         storage: localStorage, // Default cookie
    //     //         // paths: ['localStorageLanguage'], // You can select multiple
    //     //     },
    //     //     {
    //     //         key: 'sessionStorageLanguage', // The default key is the ID of the above store. You can customize the key
    //     //         storage: sessionStorage, // Default cookie
    //     //         // paths: ['sessionStorageLanguage'], // You can select multiple
    //     //     }
    //     // ]
    // },
});
