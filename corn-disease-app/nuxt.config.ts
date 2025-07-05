// nuxt.config.ts
import Aura from '@primevue/themes/aura';

export default defineNuxtConfig({
  devtools: { enabled: true },
  compatibilityDate: '2025-07-04',
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@vite-pwa/nuxt',
    '@nuxt/icon',
    // '@vueuse/nuxt',
    '@nuxt/image',
    '@vite-pwa/nuxt',
    '@nuxtjs/i18n',
    '@nuxt/icon',
    '@primevue/nuxt-module',
    '@pinia/nuxt',
    'pinia-plugin-persistedstate/nuxt'
  ],
  // imports: {
  //   autoImport: true
  // },

  // Configuration I18n
  i18n: {

    // strategy: 'prefix_except_default',
    // langDir: 'locales/',
    // lazy: true,
    // detectBrowserLanguage: {
    //   useCookie: true,
    //   cookieKey: 'i18n_redirected',
    //   redirectOn: 'root',
    //   alwaysRedirect: false,
    // },
    bundle:{
      optimizeTranslationDirective:false
    },
    vueI18n: '~/i18n.config.ts'
  },
  // Configuration HTTPS pour localhost (optionnel mais recommandé)


  // Configuration PWA
  pwa: {
    registerType: 'autoUpdate',
    workbox: {
      navigateFallback: '/',
      globPatterns: ['**/*.{js,css,html,png,svg,ico}'],
      maximumFileSizeToCacheInBytes: 5 * 1024 * 1024, // 5MB pour TensorFlow.js
      runtimeCaching: [
        {
          urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
          handler: 'CacheFirst',
          options: {
            cacheName: 'google-fonts-cache',
            expiration: {
              maxEntries: 10,
              maxAgeSeconds: 60 * 60 * 24 * 365 // 1 year
            }
          }
        },
        {
          urlPattern: /^https:\/\/fonts\.gstatic\.com\/.*/i,
          handler: 'CacheFirst',
          options: {
            cacheName: 'gstatic-fonts-cache',
            expiration: {
              maxEntries: 10,
              maxAgeSeconds: 60 * 60 * 24 * 365 // 1 year
            }
          }
        },
        {
          urlPattern: /\/models\/.*/i,
          handler: 'CacheFirst',
          options: {
            cacheName: 'tensorflow-models-cache',
            expiration: {
              maxEntries: 5,
              maxAgeSeconds: 60 * 60 * 24 * 30 // 30 days
            }
          }
        }
      ]
    },
    manifest: {
      name: 'Corn Disease Detection',
      short_name: 'CornDisease',
      description: 'Détection des maladies du maïs par IA',
      theme_color: '#4CAF50',
      background_color: '#ffffff',
      display: 'standalone',
      orientation: 'portrait',
      scope: '/',
      start_url: '/',
      icons: [
        {
          src: 'icon-192x192.png',
          sizes: '192x192',
          type: 'image/png'
        },
        {
          src: 'icon-512x512.png',
          sizes: '512x512',
          type: 'image/png'
        }
      ]
    }
  },

  // Configuration pour TensorFlow.js
  build: {
    transpile: ['@tensorflow/tfjs', 'primevue','jwt-decode']
  },

  // Configuration Vite pour optimiser les bundles
  vite: {
    server: {
      watch: {
        usePolling: true  // ✅ Important pour macOS parfois
      }
    },
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            'tensorflow': ['@tensorflow/tfjs']
          }
        }
      },
      terserOptions: {
        format: {
          comments: false, // Supprime tous les commentaires
        },
      },
      minify: 'terser', // Utilise Terser comme minimiseur
    },
    optimizeDeps: {
      include: ['@tensorflow/tfjs', 'long', 'seedrandom'],
    },
    define: {
      global: 'globalThis'
    },

  },

  // Configuration Capacitor
  ssr: false, // Important pour Capacitor

  // Optimisations
  nitro: {
    preset: 'static'
  },

  // Configuration des assets
  css: [
    '~/assets/css/main.css',
    'primeicons/primeicons.css',
    'flag-icons/css/flag-icons.min.css'
  ],

  // Variables d'environnement
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_URL ?? 'http://localhost:3000',
      serverUrl: process.env.NUXT_PUBLIC_SERVER_URL ?? 'http://localhost:3000',
      supportEmail: process.env.NUXT_PUBLIC_EMAIL_SENDER_SUPPORT ?? 'support@agriguard.ai',
    }
  },

  app: {
    head: {
      title: 'AgriGuard AI - Protection des cultures',
      meta: [
        { name: 'description', content: 'Détection IA des ravageurs agricoles au Cameroun' },
        { name: 'theme-color', content: '#16a34a' },
        { name: 'mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'default' },
        { name: 'apple-mobile-web-app-title', content: 'AgriGuard AI' },
        { name: 'msapplication-TileColor', content: '#16a34a' },
        { name: 'msapplication-config', content: '/browserconfig.xml' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' },
        { rel: 'mask-icon', href: '/safari-pinned-tab.svg', color: '#16a34a' }
      ]
    }
  },

  primevue: {
    options: {
      ripple: true,
      inputVariant: 'filled',
      theme: {
        preset: Aura,
        options: {
          prefix: 'p',
          darkModeSelector: 'light',
          cssLayer: false
        }
      }
    }
  },

  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
    {
      path: '~/components/sections',
      pathPrefix: false,
    }
  ],

  appConfig: {
    theme: 'light',
    itemsPerPage: 10,
    // Autres paramètres personnalisés
  },

  // Configuration des plugins
  // plugins: [
  //   '~/plugins/capacitor.client.ts',
  //   '~/plugins/tensorflow.client.ts'
  // ],

  experimental: {
    payloadExtraction: false
  }
})