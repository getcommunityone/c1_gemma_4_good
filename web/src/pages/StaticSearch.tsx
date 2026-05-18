import { useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline'
import { loadSearchIndex, searchIndex, type StaticSearchResult } from '../lib/staticSearch'

const TYPE_LABELS: Record<string, string> = {
  jurisdiction: 'Jurisdiction',
  meeting: 'Meeting',
  topic: 'Topic',
}

export default function StaticSearch() {
  const [params, setParams] = useSearchParams()
  const [draft, setDraft] = useState(() => params.get('q') || '')
  const q = params.get('q') || ''

  const { data, isLoading, isError } = useQuery({
    queryKey: ['static-search-index'],
    queryFn: loadSearchIndex,
  })

  const results = useMemo(() => {
    if (!data?.items) return []
    if (!q.trim()) return data.items.slice(0, 20)
    return searchIndex(data.items, q.trim(), 50)
  }, [data, q])

  const submit = (e: React.FormEvent) => {
    e.preventDefault()
    const next = new URLSearchParams(params)
    if (draft.trim()) next.set('q', draft.trim())
    else next.delete('q')
    setParams(next)
  }

  return (
    <div className="mx-auto max-w-3xl flex-1 px-4 py-8">
      <h1 className="text-2xl font-bold text-slate-900">Search</h1>
      <p className="mt-1 text-sm text-slate-600">
        Runs entirely in the browser over <code className="text-xs">public/data/search-index.json</code>.
      </p>
      <form onSubmit={submit} className="mt-4 flex gap-2">
        <div className="relative flex-1">
          <MagnifyingGlassIcon className="pointer-events-none absolute left-3 top-2.5 h-5 w-5 text-slate-400" />
          <input
            type="search"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder="e.g. Tuscaloosa, fines, 2026-02-18"
            className="w-full rounded-lg border border-slate-300 py-2 pl-10 pr-3 text-sm"
          />
        </div>
        <button
          type="submit"
          className="rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
        >
          Search
        </button>
      </form>

      {isLoading && <p className="mt-6 text-slate-600">Loading index…</p>}
      {isError && <p className="mt-6 text-red-700">Could not load search index.</p>}

      {data && (
        <p className="mt-4 text-xs text-slate-500">
          Index updated {data.generated_at} · {results.length} result{results.length === 1 ? '' : 's'}
          {q ? ` for “${q}”` : ''}
        </p>
      )}

      <ul className="mt-4 space-y-3">
        {results.map((r: StaticSearchResult, i) => (
          <li key={`${r.type}-${r.title}-${i}`} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <span className="text-xs font-medium uppercase text-teal-700">{TYPE_LABELS[r.type] || r.type}</span>
            <h2 className="mt-1 text-lg font-semibold text-slate-900">{r.title}</h2>
            <p className="text-sm text-slate-600">{r.subtitle}</p>
            <p className="mt-1 text-sm text-slate-500">{r.description}</p>
            <Link to={r.url} className="mt-2 inline-block text-sm font-medium text-teal-700 hover:underline">
              View →
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
