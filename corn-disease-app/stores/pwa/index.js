// stores/installPrompt.ts
import { defineStore } from 'pinia'

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
        key:'pwa',
        paths: ['dismissed','showPrompt']
    }
})
