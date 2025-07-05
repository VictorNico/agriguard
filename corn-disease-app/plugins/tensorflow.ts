// plugins/tensorflow.client.ts
import * as tf from '@tensorflow/tfjs'
import '@tensorflow/tfjs-backend-webgl'
import '@tensorflow/tfjs-backend-cpu'

export default defineNuxtPlugin(async () => {

    console.log('Initialisation TensorFlow.js...')

    try {
        // Attendre que TensorFlow soit prêt
        await tf.ready()

        // Définir le backend (WebGL pour de meilleures performances)
        await tf.setBackend('webgl')

        console.log('TensorFlow.js initialisé avec succès')
        console.log('Backend utilisé:', tf.getBackend())
        console.log('Version TensorFlow.js:', tf.version)

        // Informations sur les capacités
        console.log('WebGL supporté:', tf.ENV.get('WEBGL_SUPPORTED'))
        console.log('WebGL version:', tf.ENV.get('WEBGL_VERSION'))

    } catch (error) {
        console.error('Erreur initialisation TensorFlow.js:', error)

        // Fallback sur CPU si WebGL échoue
        try {
            await tf.setBackend('cpu')
            console.log('Fallback: utilisation du backend CPU')
        } catch (cpuError) {
            console.error('Erreur backend CPU:', cpuError)
        }
    }

    // Fournir TensorFlow globalement
    return {
        provide: {
            tensorflow: {
                ready: tf.ready,
                version: tf.version,
                backend: tf.getBackend(),
                tf
            }
        }
    }
})