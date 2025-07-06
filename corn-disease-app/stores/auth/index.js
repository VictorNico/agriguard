// stores/api/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        tokens: null,
        isAuthenticated: false,
        loading: false,
        refreshing: false
    }),

    getters: {
        isLoggedIn: (state) => state.isAuthenticated && state.user !== null && state.tokens !== null,
        userName: (state) => state.user ? `${state.user?.profile?.first_name} ${state.user?.profile?.last_name}` : '',
        userEmail: (state) => state.user?.profile?.email || '',
        userPlan: (state) => state.user?.subscription?.plan || 'free',
        isAdmin: (state) => state.user?.role === 'admin',
        accessToken: (state) => state.tokens?.access_token,
        refreshToken: (state) => state.tokens?.refresh_token
    },

    actions: {
        // Utilitaire pour les requêtes API
        

        // Connexion
        async login(credentials) {
            this.loading = true

            try {
                const response = await this.apiRequest('/api/auth/login', {
                    method: 'POST',
                    body: JSON.stringify(credentials),
                    skipAuth: true
                })

                if (response.success) {
                    this.user = response.user
                    this.tokens = response.tokens
                    this.isAuthenticated = true

                    return response
                } else {
                    throw new Error(response.error || 'Login failed')
                }
            } catch (error) {
                console.error('Login error:', error)
                throw error
            } finally {
                this.loading = false
            }
        },

        // Inscription
        async register(userData) {
            this.loading = true

            try {
                const response = await this.apiRequest('/api/auth/register', {
                    method: 'POST',
                    body: JSON.stringify(userData),
                    skipAuth: true
                })

                if (response.success) {
                    this.user = response.user
                    this.tokens = response.tokens
                    this.isAuthenticated = true

                    return response
                } else {
                    throw new Error(response.error || 'Registration failed')
                }
            } catch (error) {
                console.error('Registration error:', error)
                throw error
            } finally {
                this.loading = false
            }
        },

        // Déconnexion
        async logout() {
            try {
                // Appeler l'API de déconnexion si l'utilisateur est connecté
                if (this.isAuthenticated && this.tokens) {
                    await this.apiRequest('/api/auth/logout', {
                        method: 'POST'
                    })
                }

                // Nettoyer les données locales
                this.user = null
                this.tokens = null
                this.isAuthenticated = false

                // Rediriger vers la page d'accueil en cas de succès
                await navigateTo('/')

            } catch (error) {
                console.error('Logout API error:', error)

                // Afficher un toast d'erreur
                const toast = useToast()
                toast.add({
                    severity: 'error',
                    summary: 'Erreur de déconnexion',
                    detail: error.message || 'Une erreur est survenue lors de la déconnexion',
                    life: 5000
                })

                // // Même en cas d'erreur API, on nettoie les données locales
                // this.user = null
                // this.tokens = null
                // this.isAuthenticated = false
                //
                // // Rediriger quand même vers la page d'accueil
                // await navigateTo('/')
            }
        },

        // Rafraîchir les tokens
        async refreshTokens() {
            if (this.refreshing) return

            this.refreshing = true

            try {
                if (!this.tokens?.refresh_token) {
                    throw new Error('No refresh token available')
                }

                const response = await this.apiRequest('/api/auth/refresh', {
                    method: 'POST',
                    body: JSON.stringify({
                        refresh_token: this.tokens.refresh_token
                    }),
                    skipAuth: true
                })

                if (response.success) {
                    this.tokens = response.tokens
                    return response.tokens
                } else {
                    throw new Error(response.error || 'Token refresh failed')
                }
            } catch (error) {
                console.error('Token refresh error:', error)
                await this.logout()
                throw error
            } finally {
                this.refreshing = false
            }
        },

        // Mettre à jour le profil
        async updateProfile(profileData) {
            this.loading = true

            try {
                const response = await this.apiRequest('/api/auth/profile', {
                    method: 'PUT',
                    body: JSON.stringify(profileData)
                })

                if (response.success) {
                    this.user = response.user
                    return response
                } else {
                    throw new Error(response.error || 'Profile update failed')
                }
            } catch (error) {
                console.error('Profile update error:', error)
                throw error
            } finally {
                this.loading = false
            }
        },

        // Changer le mot de passe
        async changePassword(passwordData) {
            this.loading = true

            try {
                const response = await this.apiRequest('/api/auth/change-password', {
                    method: 'POST',
                    body: JSON.stringify(passwordData)
                })

                if (response.success) {
                    return response
                } else {
                    throw new Error(response.error || 'Password change failed')
                }
            } catch (error) {
                console.error('Password change error:', error)
                throw error
            } finally {
                this.loading = false
            }
        },

        // Supprimer le compte
        async deleteAccount(password) {
            this.loading = true

            try {
                const response = await this.apiRequest('/api/auth/delete-account', {
                    method: 'DELETE',
                    body: JSON.stringify({ password })
                })

                if (response.success) {
                    await this.logout()
                    return response
                } else {
                    throw new Error(response.error || 'Account deletion failed')
                }
            } catch (error) {
                console.error('Account deletion error:', error)
                throw error
            } finally {
                this.loading = false
            }
        },

        // Vérifier si le token est expiré
        isTokenExpired() {
            if (!this.tokens?.access_token) return true

            try {
                const payload = JSON.parse(atob(this.tokens.access_token.split('.')[1]))
                const now = Date.now() / 1000

                return payload.exp < now
            } catch (error) {
                console.error('Error checking token expiration:', error)
                return true
            }
        },

        // Obtenir l'en-tête d'autorisation
        getAuthHeader() {
            return this.tokens?.access_token ? `Bearer ${this.tokens.access_token}` : null
        },

        // Vérifier les permissions
        hasPermission(permission) {
            if (!this.user || !this.user.permissions) return false
            return this.user.permissions.includes(permission)
        },

        // Obtenir les statistiques utilisateur
        async getUserStats() {
            try {
                const response = await this.apiRequest('/api/users/stats', {
                    method: 'GET'
                })

                if (response.success) {
                    return response.stats
                } else {
                    throw new Error(response.error || 'Failed to get user stats')
                }
            } catch (error) {
                console.error('Error getting user stats:', error)
                throw error
            }
        }
    },

    persist: {
        key: 'auth',
        paths: ['user', 'tokens', 'isAuthenticated', 'loading', 'refreshing']
    }
})