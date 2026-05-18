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
        civic: {
          navy: '#0a1628',
          'navy-mid': '#0f2140',
          'navy-light': '#1a2d4a',
          gold: '#d4a84b',
          'gold-light': '#f0d78c',
          cream: '#f8f6f0',
        },
      },
      fontFamily: {
        display: ['"Playfair Display"', 'Georgia', 'serif'],
        sans: ['"DM Sans"', 'Inter', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'civic-grid': `
          linear-gradient(rgba(212, 168, 75, 0.06) 1px, transparent 1px),
          linear-gradient(90deg, rgba(212, 168, 75, 0.06) 1px, transparent 1px)
        `,
        'doc-texture': `
          radial-gradient(ellipse at 20% 0%, rgba(255,255,255,0.04) 0%, transparent 50%),
          radial-gradient(ellipse at 80% 100%, rgba(212,168,75,0.08) 0%, transparent 45%)
        `,
      },
    },
  },
  plugins: [],
}
