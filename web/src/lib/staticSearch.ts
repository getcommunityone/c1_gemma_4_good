import { dataUrl } from './dataUrl'

export type SearchResultType = 'jurisdiction' | 'meeting' | 'topic'

export interface StaticSearchResult {
  type: SearchResultType
  title: string
  subtitle: string
  description: string
  url: string
  score: number
  metadata: Record<string, string>
}

export interface StaticSearchIndex {
  generated_at: string
  items: StaticSearchResult[]
}

let cache: StaticSearchIndex | null = null

export async function loadSearchIndex(): Promise<StaticSearchIndex> {
  if (cache) return cache
  const res = await fetch(dataUrl('data/search-index.json'))
  if (!res.ok) throw new Error(`search-index.json: ${res.status}`)
  cache = (await res.json()) as StaticSearchIndex
  return cache
}

function tokenize(q: string): string[] {
  return q
    .toLowerCase()
    .split(/\s+/)
    .map((t) => t.trim())
    .filter((t) => t.length >= 2)
}

/** Client-side search — no backend. */
export function searchIndex(items: StaticSearchResult[], query: string, limit = 50): StaticSearchResult[] {
  const tokens = tokenize(query)
  if (!tokens.length) return items.slice(0, limit)

  const scored: StaticSearchResult[] = []
  for (const item of items) {
    const hay = `${item.title} ${item.subtitle} ${item.description}`.toLowerCase()
    let hits = 0
    for (const t of tokens) {
      if (hay.includes(t)) hits += 1
    }
    if (hits > 0) {
      scored.push({ ...item, score: hits / tokens.length })
    }
  }
  scored.sort((a, b) => b.score - a.score)
  return scored.slice(0, limit)
}
