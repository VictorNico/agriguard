
import { defineStore } from 'pinia';
import { jwtDecode } from "jwt-decode";
import {capacitorStorage} from "~/utils/persist-storage.ts";

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: {},
        isAuthenticated: false,
        token: null,
    }),
    actions: {
        saveToken( token ) {
            this.token = token;
            this.updateUser(jwtDecode(token))
            this.updateAuthState(true)
        },
        updateUser( data ) {
            this.user = {...data};
        },
        updateAuthState( statut ) {
            this.isAuthenticated = statut;
        },
        logout() {
            this.updateUser({})
            this.updateAuthState(false)
            this.token = null;
        },
        ValidateToken() {
            if (this.token === null) {
                this.logout();
                return 2;
            }

            try {
                const decoded = jwtDecode(this.token);
                const currentTime = Math.floor(Date.now() / 1000); // Temps actuel en secondes
                if (decoded.exp && decoded.exp > currentTime) {
                    return 1;
                } else {
                    this.logout();
                    return 0;
                }
            } catch (error) {
                // Si le token est invalide ou corrompu
                // console.error("Invalid token", error);
                this.logout();
                return 0;
            }
        },
    },
    persist: {
        storage: capacitorStorage,
        paths: ['user','isAuthenticated','token'] // facultatif ici, mais utile si tu as d'autres props
    }
});
