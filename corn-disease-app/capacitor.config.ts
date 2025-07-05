// capacitor.config.ts
import type { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'com.digitalfarmers.agriguard',
  appName: 'AgriGuard',
  webDir: 'dist',
  ...(process.env.NODE_ENV === 'development' ? {
    server: {
      url: 'http://192.168.171.160/:3000',
      cleartext: true
    }} : {server: {
      androidScheme: 'https'
    }}
  ),
  plugins: {
    Camera: {
      permissions: ['camera', 'photos']
    },
    Geolocation: {
      permissions: ['location']
    },
    Filesystem: {
      permissions: ['storage']
    },
    Network: {
      permissions: ['networkState']
    },
    SplashScreen: {
      launchShowDuration: 3000,
      launchAutoHide: false, // Contrôle manuel
      // backgroundColor: '#4CAF50',
      // backgroundColor: undefined,
      androidSplashResourceName: 'splash',
      androidScaleType: 'CENTER_CROP',
      showSpinner: true,
      androidSpinnerStyle: 'large',
      spinnerColor: '#ffffff',
      splashFullScreen: true,
      splashImmersive: true
    },
    StatusBar: {
      style: 'default',
      // backgroundColor: '#4CAF50'
    }
  },
  // Configuration pour le développement
  // server: {
  //   url: 'http://localhost:3000',
  //   cleartext: true
  // }
}

export default config