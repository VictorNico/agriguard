/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./components/**/*.{js,vue,ts}",
        "./layouts/**/*.vue",
        "./pages/**/*.vue",
        "./plugins/**/*.{js,ts}",
        "./app.vue",
        "./error.vue"
    ],
    theme: {
        extend: {
            colors: {
                primary: '#4CAF50',
                secondary: '#2E7D32',
                accent: '#8BC34A',
                danger: '#F44336',
                warning: '#FFC107',
                info: '#2196F3',
                dark: '#263238',
                light: '#ECEFF1'
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
        }
    },
    plugins: [],
}