// stores/installPrompt.ts
import { defineStore } from 'pinia'
import { capacitorStorage } from '~/utils/persist-storage.js' // utilise ton système hybride

export const useInstallPromptStore = defineStore('installPrompt', {
    state: () => ({
        showPrompt: false,
        dismissed: false,
    }),
    actions: {
        show() {
            this.showPrompt = true
        },
        hide() {
            this.showPrompt = false
        },
        dismiss() {
            this.showPrompt = false
            this.dismissed = true
        }
    },
    persist: {
        storage: capacitorStorage,
        paths: ['dismissed','showPrompt']
    }
})
