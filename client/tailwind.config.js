/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        cream: {
          50: '#FFFDF7',
          100: '#FFF9E8',
          200: '#FFF3D1',
          300: '#FFE8A8',
          400: '#FFDA7A',
          500: '#F5C842',
        },
        profit: '#16A34A',
        loss: '#DC2626',
        bid: {
          DEFAULT: '#16A34A',
          light: '#BBF7D0',
        },
        ask: {
          DEFAULT: '#DC2626',
          light: '#FECACA',
        },
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
