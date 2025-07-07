// capacitor.config.ts
import type { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'com.digitalfarmers.agriguard',
  appName: 'AgriGuard',
  webDir: 'dist',
  ...(process.env.NODE_ENV === 'development' ? {
    server: {
      url: 'http://192.168.171.160:3000', // CORRIGÉ: port manquant
      cleartext: true
    }
  } : {
    server: {
      androidScheme: 'https'
    }
  }),
  ios: {
    contentInset: 'automatic',
    allowsLinkPreview: false
  },
  android: {
    allowMixedContent: true,
    captureInput: true,
    webContentsDebuggingEnabled: true
  },
  plugins: {
    // SUPPRIMÉ: Configuration Permissions inexistante dans Capacitor
    Camera: {
      permissions: ['camera', 'photos']
    },
    Geolocation: {
      permissions: ['location']
    },
    Filesystem: {
      permissions: ['storage']
    },
    SplashScreen: {
      launchShowDuration: 3000,
      launchAutoHide: false,
      androidSplashResourceName: 'splash',
      androidScaleType: 'CENTER_CROP',
      showSpinner: true,
      androidSpinnerStyle: 'large',
      spinnerColor: '#ffffff',
      splashFullScreen: true,
      splashImmersive: true
    },
    StatusBar: {
      style: 'default'
    }
  }
}

export default config