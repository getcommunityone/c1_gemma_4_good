import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ArrowRightIcon, CalendarIcon, MapPinIcon } from '@heroicons/react/24/outline'
import { useNavigate } from 'react-router-dom'
import { dataUrl } from '../lib/dataUrl'

interface GemmaMeetingRow {
  jurisdiction_label: string
  jurisdiction_root: string
  meeting_date: string
  calendar_year: string
  summary_path: string | null
  policy_json_path: string | null
  notes?: string
  categories?: string[]
}

interface GemmaDemoIndex {
  generated_at: string
  meetings: GemmaMeetingRow[]
}

function meetingId(m: GemmaMeetingRow) {
  return `${m.jurisdiction_root}_${m.meeting_date}`.replace(/\//g, '_')
}

export default function MeetingsExplorerPage() {
  const navigate = useNavigate()
  const [activeCategory, setActiveCategory] = useState<string>('all')

  const { data, isLoading, isError } = useQuery({
    queryKey: ['gemma-demo-index'],
    queryFn: async (): Promise<GemmaDemoIndex> => {
      const res = await fetch(dataUrl('data/gemma-demo/index.json'))
      if (!res.ok) throw new Error(String(res.status))
      return res.json()
    },
  })

  const meetings = data?.meetings || []

  const categoryPills = useMemo(() => {
    const counts = new Map<string, number>()
    meetings.forEach((m) => {
      ;(m.categories || []).forEach((category) => {
        const key = category.trim()
        if (!key) return
        counts.set(key, (counts.get(key) || 0) + 1)
      })
    })

    const categories = Array.from(counts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 6)
      .map(([label, count]) => ({ id: label, label, count }))

    return [{ id: 'all', label: 'All', count: meetings.length }, ...categories]
  }, [meetings])

  const visibleMeetings =
    activeCategory === 'all'
      ? meetings
      : meetings.filter((m) => (m.categories || []).includes(activeCategory))

  return (
    <div className="min-h-full bg-gradient-to-b from-slate-100 via-slate-100 to-slate-200 p-4 sm:p-6">
      <div className="mx-auto max-w-5xl">
        <div className="mb-4 rounded-2xl border border-teal-100 bg-white/90 p-5 shadow-sm">
          <h2 className="text-2xl font-bold text-slate-900">
            Meeting Minutes {meetings.length > 0 && `(${meetings.length})`}
          </h2>
          <p className="mt-1 text-sm text-slate-600">Browse local meeting outcomes and drill into full summaries.</p>
        </div>

        {isLoading && <p className="rounded-xl bg-white p-4 text-slate-500 shadow-sm">Loading…</p>}
        {isError && <p className="rounded-xl bg-white p-4 text-red-700 shadow-sm">Missing gemma-demo/index.json</p>}

        {data && meetings.length === 0 && (
          <p className="rounded-xl bg-white p-4 text-slate-500 shadow-sm">No meetings found.</p>
        )}

        {meetings.length > 0 && (
          <>
            <div className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200">
              <div className="flex flex-wrap items-center gap-2">
                <span className="mr-1 text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Trending Categories
                </span>
                {categoryPills.map((pill) => {
                  const active = activeCategory === pill.id
                  return (
                    <button
                      key={pill.id}
                      type="button"
                      onClick={() => setActiveCategory(pill.id)}
                      className={
                        active
                          ? 'rounded-full bg-teal-600 px-3 py-1.5 text-xs font-semibold text-white ring-1 ring-teal-600'
                          : 'rounded-full bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-700 ring-1 ring-slate-200 transition hover:bg-slate-200'
                      }
                    >
                      {pill.label} ({pill.count})
                    </button>
                  )
                })}
              </div>
            </div>
            <p className="px-1 pt-3 text-xs text-slate-500">Generated {data?.generated_at}</p>
            <ul className="mt-3 space-y-3">
              {visibleMeetings.map((m) => (
                <li key={`${m.jurisdiction_root}-${m.meeting_date}`}>
                  <button
                    type="button"
                    onClick={() => navigate(`/data-explorer/meetings/${meetingId(m)}`)}
                    className="group w-full rounded-2xl bg-white p-5 text-left shadow-sm ring-1 ring-slate-200 transition hover:-translate-y-0.5 hover:shadow-md hover:ring-teal-300 focus:outline-none focus:ring-2 focus:ring-teal-500"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="min-w-0 flex-1">
                        <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-teal-700">Meeting</p>
                        <h3 className="mt-1 text-xl font-semibold text-slate-900 group-hover:text-teal-800">
                          {m.jurisdiction_label}
                        </h3>
                        <div className="mt-2 flex flex-wrap gap-4 text-sm text-slate-600">
                          <span className="inline-flex items-center gap-1.5">
                            <CalendarIcon className="h-4 w-4" />
                            {m.meeting_date}
                          </span>
                          <span className="inline-flex items-center gap-1.5">
                            <MapPinIcon className="h-4 w-4" />
                            {m.jurisdiction_root}
                          </span>
                        </div>
                        {m.categories && m.categories.length > 0 && (
                          <div className="mt-3 flex flex-wrap gap-2">
                            {m.categories.map((category) => (
                              <span
                                key={`${m.jurisdiction_root}-${m.meeting_date}-${category}`}
                                className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-700 ring-1 ring-slate-200"
                              >
                                {category}
                              </span>
                            ))}
                          </div>
                        )}
                        {m.notes && <p className="mt-2 text-sm text-amber-800">{m.notes}</p>}
                      </div>
                      <div className="flex shrink-0 items-center gap-2">
                        <span className="rounded-full bg-teal-50 px-3 py-1 text-xs font-semibold text-teal-700 ring-1 ring-teal-200">
                          Meeting details
                        </span>
                        <ArrowRightIcon className="h-5 w-5 text-slate-400 transition group-hover:translate-x-1 group-hover:text-teal-600" />
                      </div>
                    </div>
                  </button>
                </li>
              ))}
            </ul>
            {visibleMeetings.length === 0 && (
              <p className="mt-3 rounded-xl bg-white p-4 text-sm text-slate-500 shadow-sm">No meetings match this category.</p>
            )}
          </>
        )}
      </div>
    </div>
  )
}
