/** Prefix static JSON paths for GitHub Pages (`base: /c1_gemma_4_good/`). */
export function dataUrl(relativePath: string): string {
  const base = import.meta.env.BASE_URL || '/'
  const clean = relativePath.replace(/^\//, '')
  return `${base}${clean}`
}
