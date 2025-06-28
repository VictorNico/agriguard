const messages = Object.fromEntries(
    Object.entries(
        import.meta.glob('./i18n/locales/*.json', { eager: true })
    ).map(([key, value]) => {
        // Extraire le code de langue depuis './i18n/locales/fr.json'
        const langCode = key.match(/\.\/i18n\/locales\/(.+)\.json/)?.[1]
        return [langCode, (value as any).default]
    })
)
export default defineI18nConfig(() => ({
    legacy: false,
    locale: 'fr',
    fallbackLocale: 'fr',
    locales: [
        {
            code: 'fr',
            iso: 'fr-CM',
            name: 'Français',
            file: 'fr.json'
        },
        {
            code: 'en',
            iso: 'en-CM',
            name: 'English',
            file: 'en.json'
        }
    ],
    defaultLocale: 'fr',
    numberFormats: {
        fr: {
            currency: {
                style: 'currency',
                currency: 'XAF',
                notation: 'standard'
            },
            decimal: {
                style: 'decimal',
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            },
            percent: {
                style: 'percent',
                useGrouping: false
            }
        },
        en: {
            currency: {
                style: 'currency',
                currency: 'XAF',
                notation: 'standard'
            },
            decimal: {
                style: 'decimal',
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            },
            percent: {
                style: 'percent',
                useGrouping: false
            }
        }
    },
    datetimeFormats: {
        fr: {
            short: {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            },
            long: {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                weekday: 'short',
                hour: 'numeric',
                minute: 'numeric'
            }
        },
        en: {
            short: {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            },
            long: {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                weekday: 'short',
                hour: 'numeric',
                minute: 'numeric'
            }
        }
    },
    messages
}))