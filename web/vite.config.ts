import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

/** GitHub Pages project site: https://getcommunityone.github.io/c1_gemma_4_good/ */
const repoBase = process.env.VITE_BASE_PATH ?? '/c1_gemma_4_good/'

export default defineConfig({
  plugins: [react()],
  base: repoBase,
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
})
