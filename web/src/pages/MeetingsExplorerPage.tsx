import { useState } from 'react'
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
  theme?: string
}

interface GemmaDemoIndex {
  generated_at: string
  meetings: GemmaMeetingRow[]
}

const THEMES = [
  { id: 'governance', label: 'Governance & Admin', color: 'bg-blue-100 text-blue-800' },
  { id: 'infrastructure', label: 'Infrastructure & Capital', color: 'bg-amber-100 text-amber-800' },
  { id: 'education', label: 'Education & Workforce', color: 'bg-green-100 text-green-800' },
]

const TRENDING_TOPICS = [
  'Budget & Finance',
  'Infrastructure',
  'Public Safety',
  'Education',
  'Planning & Zoning',
  'Health & Services',
]

export default function MeetingsExplorerPage() {
  const [selectedTheme, setSelectedTheme] = useState<string | null>(null)
  const [selectedMeeting, setSelectedMeeting] = useState<GemmaMeetingRow | null>(null)
  const [searchQuery, setSearchQuery] = useState('')

  const { data, isLoading, isError } = useQuery({
    queryKey: ['gemma-demo-index'],
    queryFn: async (): Promise<GemmaDemoIndex> => {
      const res = await fetch(dataUrl('data/gemma-demo/index.json'))
      if (!res.ok) throw new Error(String(res.status))
      return res.json()
    },
  })

  const filteredMeetings = (data?.meetings || []).filter((m) => {
    // Apply theme filter
    if (selectedTheme) {
      const themeMap: Record<string, string> = {
        governance: 'Governance',
        infrastructure: 'Infrastructure',
        education: 'Education',
      }
      if (!m.jurisdiction_label?.includes(themeMap[selectedTheme]) && !m.notes?.includes(themeMap[selectedTheme])) {
        return false
      }
    }

    // Apply search filter
    if (searchQuery) {
      const q = searchQuery.toLowerCase()
      return (
        m.jurisdiction_label?.toLowerCase().includes(q) ||
        m.meeting_date?.includes(q) ||
        m.notes?.toLowerCase().includes(q)
      )
    }

    return true
  })

  return (
    <div className="space-y-6">
      {/* Trending Topics */}
      <div className="rounded-lg bg-gradient-to-r from-teal-50 to-blue-50 p-4 shadow-sm border border-teal-100">
        <h3 className="text-sm font-semibold text-slate-900 mb-3">🔥 Trending Topics</h3>
        <div className="flex flex-wrap gap-2">
          {TRENDING_TOPICS.map((topic) => (
            <button
              key={topic}
              className="px-3 py-1 rounded-full text-xs font-medium bg-white border border-teal-200 text-teal-700 hover:bg-teal-50 transition"
              onClick={() => setSearchQuery(topic.toLowerCase())}
            >
              {topic}
            </button>
          ))}
        </div>
      </div>

      {/* Theme Filters */}
      <div className="rounded-lg bg-white p-4 shadow-sm">
        <h3 className="text-sm font-semibold text-slate-900 mb-3">Filter by Theme</h3>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedTheme(null)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
              selectedTheme === null
                ? 'bg-slate-900 text-white'
                : 'bg-slate-100 text-slate-900 hover:bg-slate-200'
            }`}
          >
            All
          </button>
          {THEMES.map((theme) => (
            <button
              key={theme.id}
              onClick={() => setSelectedTheme(theme.id)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                selectedTheme === theme.id
                  ? theme.color
                  : 'bg-slate-100 text-slate-900 hover:bg-slate-200'
              }`}
            >
              {theme.label}
            </button>
          ))}
        </div>
      </div>

      {/* Search */}
      <div className="rounded-lg bg-white p-4 shadow-sm">
        <input
          type="text"
          placeholder="Search meetings by jurisdiction or date…"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-4 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
        />
      </div>

      {/* Meetings List */}
      <div className="rounded-lg bg-white shadow-sm">
        <div className="p-4 border-b border-slate-200">
          <h2 className="text-lg font-semibold text-slate-900">
            Meeting Minutes {filteredMeetings.length > 0 && `(${filteredMeetings.length})`}
          </h2>
          <p className="mt-1 text-sm text-slate-600">
            Static index from the pipeline. Rebuild with{' '}
            <code className="text-xs">python scripts/colab/export/export_web_demo_index.py</code> after §6.
          </p>
        </div>

        {isLoading && <p className="p-4 text-slate-500">Loading…</p>}
        {isError && <p className="p-4 text-red-700">Missing gemma-demo/index.json</p>}

        {data && filteredMeetings.length === 0 && (
          <p className="p-4 text-slate-500">No meetings found. Try adjusting your filters.</p>
        )}

        {filteredMeetings.length > 0 && (
          <>
            <p className="px-4 pt-2 text-xs text-slate-500">Generated {data?.generated_at}</p>
            <ul className="divide-y divide-slate-200">
              {filteredMeetings.map((m) => (
                <li key={`${m.jurisdiction_root}-${m.meeting_date}`} className="p-4 hover:bg-slate-50 transition">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="font-medium text-slate-900">{m.jurisdiction_label}</p>
                      <p className="text-sm text-slate-600">
                        {m.meeting_date} · {m.jurisdiction_root}
                      </p>
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
