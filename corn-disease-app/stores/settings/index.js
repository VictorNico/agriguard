// ~/stores/settings.ts
import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', {
    state: () => ({
        theme: {
            color: '#4A90E2',
            fontSize: '16px',
        },
        notifications: {
            enabled: true,
        },
    }),
    actions: {
        updateTheme(data) {
            this.theme = { ...this.theme, ...data };
        },
        toggleNotifications(enabled) {
            this.notifications.enabled = enabled;
        },
        async syncSettingsWithBackend() {
            // Remplacez l'URL par votre endpoint backend réel
            const response = await fetch('https://api.example.com/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.$state),
            });
            if (!response.ok) throw new Error('Failed to sync settings');
        },
    },
    persist: true,
});
