import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { dataUrl } from '../lib/dataUrl'
import { MeetingDetail } from '../components/MeetingDetail'

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

export default function MeetingsExplorerPage() {
  const [selectedMeeting, setSelectedMeeting] = useState<GemmaMeetingRow | null>(null)
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
    <div className="space-y-6">
      {/* Meetings List */}
      <div className="rounded-lg bg-white shadow-sm">
        <div className="p-4 border-b border-slate-200">
          <h2 className="text-lg font-semibold text-slate-900">
            Meeting Minutes {meetings.length > 0 && `(${meetings.length})`}
          </h2>
        </div>

        {isLoading && <p className="p-4 text-slate-500">Loading…</p>}
        {isError && <p className="p-4 text-red-700">Missing gemma-demo/index.json</p>}

        {data && meetings.length === 0 && (
          <p className="p-4 text-slate-500">No meetings found.</p>
        )}

        {meetings.length > 0 && (
          <>
            <div className="px-4 pt-3">
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
                          ? 'rounded-full bg-teal-600 px-3 py-1 text-xs font-semibold text-white ring-1 ring-teal-600'
                          : 'rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700 ring-1 ring-slate-200 hover:bg-slate-200'
                      }
                    >
                      {pill.label} ({pill.count})
                    </button>
                  )
                })}
              </div>
            </div>
            <p className="px-4 pt-2 text-xs text-slate-500">Generated {data?.generated_at}</p>
            <ul className="divide-y divide-slate-200">
              {visibleMeetings.map((m) => (
                <li key={`${m.jurisdiction_root}-${m.meeting_date}`} className="p-4 hover:bg-slate-50 transition">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="font-medium text-slate-900">{m.jurisdiction_label}</p>
                      <p className="text-sm text-slate-600">
                        {m.meeting_date} · {m.jurisdiction_root}
                      </p>
                      {m.categories && m.categories.length > 0 && (
                        <div className="mt-2 flex flex-wrap gap-1.5">
                          {m.categories.map((category) => (
                            <span
                              key={`${m.jurisdiction_root}-${m.meeting_date}-${category}`}
                              className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-700"
                            >
                              {category}
                            </span>
                          ))}
                        </div>
                      )}
                      {m.notes && <p className="mt-1 text-sm text-amber-800">{m.notes}</p>}
                    </div>
                    <div className="ml-4 flex flex-wrap gap-2 justify-end">
                      {m.summary_path && (
                        <button
                          onClick={() => setSelectedMeeting(m)}
                          className="px-3 py-1 rounded-lg bg-teal-100 text-teal-700 hover:bg-teal-200 text-sm font-medium transition"
                        >
                          View Summary
                        </button>
                      )}
                      {m.policy_json_path && (
                        <a
                          href={m.policy_json_path}
                          target="_blank"
                          rel="noreferrer"
                          className="px-3 py-1 rounded-lg bg-blue-100 text-blue-700 hover:bg-blue-200 text-sm font-medium transition inline-block"
                        >
                          Policy JSON
                        </a>
                      )}
                    </div>
                  </div>
                </li>
              ))}
            </ul>
            {visibleMeetings.length === 0 && (
              <p className="p-4 text-sm text-slate-500">No meetings match this category.</p>
            )}
          </>
        )}
      </div>

      {/* Meeting Detail Modal */}
      {selectedMeeting && (
        <MeetingDetail
          summaryPath={selectedMeeting.summary_path || ''}
          jurisdiction={selectedMeeting.jurisdiction_label}
          meetingDate={selectedMeeting.meeting_date}
          onBack={() => setSelectedMeeting(null)}
        />
      )}
    </div>
  )
}
