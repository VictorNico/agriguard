export default defineNuxtPlugin(() => {
    // Détecter si l'app est installée
    const isStandalone = () => {
        return window.matchMedia('(display-mode: standalone)').matches ||
            (window.navigator as any).standalone ||
            document.referrer.includes('android-app://')
    }

    // Log pour debug
    console.log('PWA Plugin loaded')
    console.log('Is PWA installed?', isStandalone())

    // Écouter les mises à jour du service worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            console.log('Service Worker updated')
            // Vous pouvez afficher une notification ici
        })
    }

    // Ajouter des méthodes globales
    return {
        provide: {
            pwa: {
                isInstalled: isStandalone,
                isOnline: () => navigator.onLine,
            }
        }
    }
})