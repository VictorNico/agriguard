// https://nuxt.com/docs/api/configuration/nuxt-config
import Aura from '@primevue/themes/aura';
export default defineNuxtConfig({
  devtools: { enabled: true },
  compatibilityDate: '2025-05-15',
  modules: [
    '@nuxtjs/tailwindcss',
    // '@vueuse/nuxt',
    '@nuxt/image',
    '@vite-pwa/nuxt',
    '@nuxtjs/i18n',
    '@nuxt/icon',
    '@primevue/nuxt-module',
    '@pinia/nuxt',
    'pinia-plugin-persistedstate/nuxt'
  ],

  // Configuration PWA
  pwa: {
    registerType: 'autoUpdate',
    client: {
      installPrompt: true,
      // Permettre l'installation en dev
      periodicSyncForUpdates: 20,
    },
    devOptions: {
      enabled: true,
      suppressWarnings: true,
      navigateFallback: '/',
      // disableDevLogs: true,
      type: 'module',
    },
    workbox: {
      navigateFallback: '/',
      globPatterns: [
        '**/*.{js,css,html,png,jpg,jpeg,svg,ico,woff,woff2,ttf,eot}',
        '**/manifest.json'
      ],
      // Exclude payload files since we're in SPA mode
      globIgnores: [
        '**/node_modules/**/*',
        'sw.js',
        'workbox-*.js',
        '**/_payload.json', // Explicitly ignore payload files
        '**/server/**/*'
      ],
      cleanupOutdatedCaches: true,
      runtimeCaching: [
        {
          urlPattern: /^https:\/\/api\./,
          handler: 'CacheFirst',
          options: {
            cacheName: 'api-cache',
            expiration: {
              maxEntries: 100,
              maxAgeSeconds: 60 * 60 * 24 // 24h
            }
          }
        },
        {
          // Cache static assets
          urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp|ico)$/,
          handler: 'CacheFirst',
          options: {
            cacheName: 'images-cache',
            expiration: {
              maxEntries: 60,
              maxAgeSeconds: 60 * 60 * 24 * 30 // 30 days
            }
          }
        },
        {
          // Cache CSS and JS files
          urlPattern: /\.(?:js|css|woff|woff2|ttf|eot)$/,
          handler: 'StaleWhileRevalidate',
          options: {
            cacheName: 'static-resources'
          }
        }
      ]
    },
    manifest: {
      name: 'AgriGuard AI - Protection des cultures',
      short_name: 'AgriGuard AI',
      description: 'Détection IA des ravageurs agricoles au Cameroun',
      theme_color: '#16a34a',
      background_color: '#ffffff',
      display: 'standalone',
      orientation: 'portrait',
      scope: '/',
      start_url: '/',
      lang: 'fr-CM',
      icons: [
        {
          src: '/icon-192x192.png',
          sizes: '192x192',
          type: 'image/png',
        },
        {
          src: '/icon-512x512.png',
          sizes: '512x512',
          type: 'image/png',
        },
        {
          src: '/icon-512x512.png',
          sizes: '512x512',
          type: 'image/png',
          purpose: 'any maskable',
        },
      ],
      screenshots: [
        {
          src: '/screenshot-wide.png',
          sizes: '1280x720',
          type: 'image/png',
          form_factor: 'wide',
          label: 'AgriGuard AI Dashboard'
        },
        {
          src: '/screenshot-mobile.png',
          sizes: '640x1136',
          type: 'image/png',
          form_factor: 'narrow',
          label: 'AgriGuard AI Mobile'
        }
      ]
    },
  },

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

  // Optimisations PWA
  nitro: {
    esbuild: {
      options: {
        target: 'esnext'
      }
    },
    routeRules: {
      '/**': {
        headers: process.env.NODE_ENV === 'development' ? {
          'Content-Security-Policy': "script-src 'self' 'unsafe-inline' 'unsafe-eval'"
        } : {}
      }
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

  css: [
    '~/assets/css/main.css',
    'primeicons/primeicons.css',
    'flag-icons/css/flag-icons.min.css'
  ],

  appConfig: {
    theme: 'light',
    itemsPerPage: 10,
    // Autres paramètres personnalisés
  },

  build: {
    transpile: ['primevue','jwt-decode']
  },

  // Configuration pour PWA
  ssr: false, // Pour PWA optimale
  vite: {
    build: {
      terserOptions: {
        format: {
          comments: false, // Supprime tous les commentaires
        },
      },
      minify: 'terser', // Utilise Terser comme minimiseur
    },
  },
  // Optimisations production
  experimental: {
    payloadExtraction: false
  }
})