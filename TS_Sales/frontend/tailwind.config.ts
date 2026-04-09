import type { Config } from 'tailwindcss'

const config: Config = {
    content: [
        './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
        './src/components/**/*.{js,ts,jsx,tsx,mdx}',
        './src/modules/**/*.{js,ts,jsx,tsx,mdx}',
        './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    theme: {
        extend: {
            colors: {
                'primary': {
                    50: '#fafaf8',
                    100: '#f4f3ee',
                    200: '#e8e5da',
                    300: '#dcccac',
                    400: '#c9b896',
                    500: '#99ad7a',
                    600: '#7a8c61',
                    700: '#546b41',
                    800: '#3d4d2e',
                    900: '#28331f',
                },
                'secondary': {
                    50: '#f9f8f5',
                    100: '#fff8ec',
                    200: '#ffefd8',
                    300: '#ffe6c4',
                    400: '#f5d9aa',
                    500: '#dcccac',
                    600: '#c4b494',
                    700: '#99ad7a',
                    800: '#7a8c61',
                    900: '#546b41',
                },
                'accent': {
                    light: '#fff8ec',
                    DEFAULT: '#dcccac',
                    dark: '#99ad7a',
                },
            },
        },
    },
    plugins: [],
}
export default config
