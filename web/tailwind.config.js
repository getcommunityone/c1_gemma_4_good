/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#354F52',
          600: '#2e4346',
          700: '#27383a',
        },
      },
    },
  },
  plugins: [],
}
