// services/PermissionManager.ts
import { Capacitor } from '@capacitor/core';
import { Camera } from '@capacitor/camera';
import { Geolocation } from '@capacitor/geolocation';
import { Filesystem } from '@capacitor/filesystem';
import { Device } from '@capacitor/device';

export interface PermissionConfig {
    timeout?: number;
    retryCount?: number;
    retryDelay?: number;
    showExplanation?: boolean;
}

export class PermissionManager {
    private static instance: PermissionManager;
    private defaultConfig: PermissionConfig = {
        timeout: 30000,
        retryCount: 2, // Réduit pour éviter la frustration
        retryDelay: 1500,
        showExplanation: true
    };

    static getInstance(): PermissionManager {
        if (!PermissionManager.instance) {
            PermissionManager.instance = new PermissionManager();
        }
        return PermissionManager.instance;
    }

    /**
     * Demande une permission avec gestion spécifique Android
     */
    async requestPermission(
        permissionType: 'camera' | 'location' | 'storage',
        config: PermissionConfig = {}
    ): Promise<boolean> {
        const finalConfig = { ...this.defaultConfig, ...config };

        // Vérifier si déjà accordée
        const isAlreadyGranted = await this.checkPermission(permissionType);
        if (isAlreadyGranted) {
            console.log(`✅ Permission ${permissionType} déjà accordée`);
            return true;
        }

        // Obtenir les infos de l'appareil
        const deviceInfo = await Device.getInfo();
        const isAndroid = deviceInfo.platform === 'android';
        const androidVersion = parseInt(deviceInfo.osVersion.split('.')[0]);

        for (let attempt = 1; attempt <= finalConfig.retryCount!; attempt++) {
            try {
                console.log(`🔐 Tentative ${attempt}/${finalConfig.retryCount} pour ${permissionType}`);

                if (finalConfig.showExplanation && attempt === 1) {
                    await this.showPermissionExplanation(permissionType);
                }

                const result = await this.requestSinglePermission(
                    permissionType,
                    finalConfig.timeout!,
                    isAndroid,
                    androidVersion
                );

                if (result) {
                    console.log(`✅ Permission ${permissionType} accordée`);
                    return true;
                }

                // Si refusée définitivement, ne pas réessayer
                if (attempt === 1) {
                    const currentStatus = await this.getPermissionStatus(permissionType);
                    if (currentStatus === 'denied') {
                        console.log(`❌ Permission ${permissionType} refusée définitivement`);
                        return false;
                    }
                }

                if (attempt < finalConfig.retryCount!) {
                    console.log(`⏳ Attente ${finalConfig.retryDelay}ms avant nouvelle tentative...`);
                    await this.delay(finalConfig.retryDelay!);
                }

            } catch (error) {
                console.error(`❌ Erreur tentative ${attempt}:`, error);

                if (attempt === finalConfig.retryCount!) {
                    return false;
                }

                await this.delay(finalConfig.retryDelay!);
            }
        }

        return false;
    }

    /**
     * Demande une permission avec timeout
     */
    private async requestSinglePermission(
        permissionType: 'camera' | 'location' | 'storage',
        timeout: number,
        isAndroid: boolean,
        androidVersion: number
    ): Promise<boolean> {
        return new Promise(async (resolve, reject) => {
            const timeoutId = setTimeout(() => {
                reject(new Error(`Timeout de ${timeout}ms atteint pour ${permissionType}`));
            }, timeout);

            try {
                let granted = false;

                switch (permissionType) {
                    case 'camera':
                        const cameraStatus = await Camera.requestPermissions();
                        granted = cameraStatus.camera === 'granted';
                        break;

                    case 'location':
                        const locationStatus = await Geolocation.requestPermissions();
                        granted = locationStatus.location === 'granted';
                        break;

                    case 'storage':
                        // Gestion spécifique Android pour le stockage
                        if (isAndroid) {
                            if (androidVersion >= 13) {
                                // Android 13+: Permissions granulaires
                                const storageStatus = await Filesystem.requestPermissions();
                                granted = storageStatus.publicStorage === 'granted';
                            } else if (androidVersion >= 11) {
                                // Android 11-12: MANAGE_EXTERNAL_STORAGE
                                const storageStatus = await Filesystem.requestPermissions();
                                granted = storageStatus.publicStorage === 'granted';
                            } else {
                                // Android < 11: Permissions classiques
                                const storageStatus = await Filesystem.requestPermissions();
                                granted = storageStatus.publicStorage === 'granted';
                            }
                        } else {
                            // iOS
                            const storageStatus = await Filesystem.requestPermissions();
                            granted = storageStatus.publicStorage === 'granted';
                        }
                        break;
                }

                clearTimeout(timeoutId);
                resolve(granted);

            } catch (error) {
                clearTimeout(timeoutId);
                reject(error);
            }
        });
    }

    /**
     * Vérifie si une permission est déjà accordée
     */
    async checkPermission(permissionType: 'camera' | 'location' | 'storage'): Promise<boolean> {
        try {
            switch (permissionType) {
                case 'camera':
                    const cameraStatus = await Camera.checkPermissions();
                    return cameraStatus.camera === 'granted';

                case 'location':
                    const locationStatus = await Geolocation.checkPermissions();
                    return locationStatus.location === 'granted';

                case 'storage':
                    const storageStatus = await Filesystem.checkPermissions();
                    return storageStatus.publicStorage === 'granted';
            }
        } catch (error) {
            console.error('Erreur vérification permission:', error);
            return false;
        }
    }

    /**
     * Obtient le statut détaillé d'une permission
     */
    private async getPermissionStatus(permissionType: 'camera' | 'location' | 'storage'): Promise<string> {
        try {
            switch (permissionType) {
                case 'camera':
                    const cameraStatus = await Camera.checkPermissions();
                    return cameraStatus.camera;

                case 'location':
                    const locationStatus = await Geolocation.checkPermissions();
                    return locationStatus.location;

                case 'storage':
                    const storageStatus = await Filesystem.checkPermissions();
                    return storageStatus.publicStorage;
            }
        } catch (error) {
            console.error('Erreur statut permission:', error);
            return 'denied';
        }
    }

    /**
     * Demande toutes les permissions nécessaires
     */
    async requestAllPermissions(config: PermissionConfig = {}): Promise<{
        camera: boolean;
        location: boolean;
        storage: boolean;
        allGranted: boolean;
    }> {
        const results = {
            camera: false,
            location: false,
            storage: false,
            allGranted: false
        };

        console.log('🔍 Demande de toutes les permissions...');

        // Demander les permissions une par une avec délai
        try {
            results.camera = await this.requestPermission('camera', config);
            await this.delay(500); // Délai entre les demandes

            results.location = await this.requestPermission('location', config);
            await this.delay(500);

            results.storage = await this.requestPermission('storage', config);
        } catch (error) {
            console.error('❌ Erreur lors de la demande des permissions:', error);
        }

        results.allGranted = results.camera && results.location && results.storage;

        console.log('📋 Résultats permissions:', results);
        return results;
    }

    /**
     * Affiche une explication avant de demander la permission
     */
    private async showPermissionExplanation(permissionType: string): Promise<void> {
        const explanations = {
            camera: 'Cette application a besoin d\'accéder à votre caméra pour prendre des photos des plantes.',
            location: 'Cette application a besoin de votre localisation pour vous fournir des informations météorologiques locales.',
            storage: 'Cette application a besoin d\'accéder à vos fichiers pour sauvegarder vos photos et rapports.'
        };

        console.log(`💬 ${explanations[permissionType as keyof typeof explanations]}`);
        await this.delay(1000);
    }

    /**
     * Utilitaire pour créer un délai
     */
    private delay(ms: number): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Redirige vers les paramètres de l'application
     */
    // async openAppSettings(): Promise<void> {
    //     if (Capacitor.isNativePlatform()) {
    //         try {
    //             const { App } = await import('@capacitor/app');
    //
    //             if (Capacitor.getPlatform() === 'android') {
    //                 // Android: Ouvrir les paramètres spécifiques de l'app
    //                 await App.openUrl({
    //                     url: 'app-settings:'
    //                 });
    //             } else {
    //                 // iOS: Ouvrir les paramètres généraux
    //                 await App.openUrl({
    //                     url: 'app-settings:'
    //                 });
    //             }
    //         } catch (error) {
    //             console.error('Impossible d\'ouvrir les paramètres:', error);
    //         }
    //     }
    // }

    /**
     * Méthode pour diagnostiquer les problèmes de permissions
     */
    async diagnosePermissions(): Promise<void> {
        console.log('🔍 Diagnostic des permissions...');

        const deviceInfo = await Device.getInfo();
        console.log('📱 Appareil:', deviceInfo);

        const permissions = ['camera', 'location', 'storage'] as const;

        for (const permission of permissions) {
            const status = await this.getPermissionStatus(permission);
            console.log(`🔐 ${permission}: ${status}`);
        }
    }
}

// Export d'une instance singleton
export const permissionManager = PermissionManager.getInstance();