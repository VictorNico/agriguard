import {useAuthStore} from "~/stores/auth/index.js";
export const apiRequest = async(endpoint, options = {}) =>{
    const config = useRuntimeConfig()
    const authStore = useAuthStore()
    const baseURL = config.public.apiBase || '/api'

    const defaultOptions = {
        headers: {
            ...options.headers
        }
    }

    // Ajouter le token d'autorisation si disponible
    if (authStore?.state?.tokens?.access_token) {
        defaultOptions.headers.Authorization = `Bearer ${this.tokens.access_token}`
    }

    const response = await fetch(`${baseURL}${endpoint}`, {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    })

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.message || errorData.error || `HTTP ${response.status}`)
    }

    return response.json()
}