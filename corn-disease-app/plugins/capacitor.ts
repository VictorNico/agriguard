// plugins/capacitor.client.ts
import { Capacitor } from '@capacitor/core'
import { StatusBar, Style } from '@capacitor/status-bar'
import { SplashScreen } from '@capacitor/splash-screen'

export default defineNuxtPlugin(async () => {
    // Fonction pour masquer le splash screen avec animation
    const hideSplashScreen = async () => {
        try {
            // Attendre que l'application soit prête
            await new Promise(resolve => setTimeout(resolve, 2000))

            // Masquer le splash screen
            await SplashScreen.hide()
            console.log('Splash screen masqué')
        } catch (error) {
            console.error('Erreur lors du masquage du splash screen:', error)
        }
    }

    // Vérifier si on est sur une plateforme native
    if (Capacitor.isNativePlatform()) {
        console.log('Application native détectée')

        // Configuration de la barre de statut
        await StatusBar.setStyle({ style: Style.Default })
        await StatusBar.setBackgroundColor({ color: '#4CAF50' })

        // Masquer le splash screen après initialisation
        await hideSplashScreen()
    } else {
        console.log('Application web/PWA détectée')

        // Pour PWA, créer un splash screen custom
        await createWebSplashScreen()
    }

    // Informations sur la plateforme
    console.log('Plateforme:', Capacitor.getPlatform())
    console.log('Native:', Capacitor.isNativePlatform())

    // Fournir les informations globalement
    return {
        provide: {
            capacitor: {
                isNative: Capacitor.isNativePlatform(),
                platform: Capacitor.getPlatform(),
                hideSplashScreen
            }
        }
    }
})

// Fonction pour créer un splash screen web
const createWebSplashScreen = async () => {
    // Créer l'élément splash screen
    const splashElement = document.createElement('div')
    splashElement.id = 'web-splash-screen'
    splashElement.innerHTML = `
    <div class="splash-content">
      <div class="splash-logo">
<!--        <div class="corn-icon">🌽</div>-->
        <div class="corn-icon h-full flex items-center">
            <img
                src="/logo.png"
                alt="Logo"
                class="h-full w-auto max-h-full object-contain"
            />
        </div>
        <h1>Corn Disease Detection</h1>
      </div>
      <div class="splash-spinner">
        <div class="spinner"></div>
        <p>Chargement de l'IA...</p>
      </div>
    </div>
  `

    // Styles pour le splash screen
    const styles = `
    #web-splash-screen {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(135deg, #ffffff 0%, #2E7D32 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999;
      transition: opacity 0.5s ease-out;
    }
    
    .splash-content {
      text-align: center;
      color: white;
    }
    
    .splash-logo {
      margin-bottom: 2rem;
    }
    
    .corn-icon {
      font-size: 4rem;
      margin-bottom: 1rem;
      animation: bounce 2s infinite;
    }
    
    .splash-logo h1 {
      font-size: 2rem;
      margin: 0;
      font-weight: bold;
    }
    
    .splash-spinner {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1rem;
    }
    
    .spinner {
      width: 40px;
      height: 40px;
      border: 3px solid rgba(255, 255, 255, 0.3);
      border-top: 3px solid white;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    @keyframes bounce {
      0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(-10px); }
      60% { transform: translateY(-5px); }
    }
  `

    // Ajouter les styles
    const styleSheet = document.createElement('style')
    styleSheet.textContent = styles
    document.head.appendChild(styleSheet)

    // Ajouter le splash screen
    document.body.appendChild(splashElement)

    // Masquer après 3 secondes
    setTimeout(() => {
        splashElement.style.opacity = '0'
        setTimeout(() => {
            if (splashElement.parentNode) {
                splashElement.parentNode.removeChild(splashElement)
            }
            if (styleSheet.parentNode) {
                styleSheet.parentNode.removeChild(styleSheet)
            }
        }, 500)
    }, 3000)
}