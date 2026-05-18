import { useQuery } from '@tanstack/react-query'
import { ArrowLeftIcon, CalendarIcon, MapPinIcon } from '@heroicons/react/24/outline'
import { useMemo } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import MarkdownRenderer from '../components/MarkdownRenderer'
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

export default function MeetingSummaryPage() {
  const navigate = useNavigate()
  const { meetingId: routeMeetingId } = useParams<{ meetingId: string }>()

  const { data: indexData, isLoading: isIndexLoading, isError: isIndexError } = useQuery({
    queryKey: ['gemma-demo-index'],
    queryFn: async (): Promise<GemmaDemoIndex> => {
      const res = await fetch(dataUrl('data/gemma-demo/index.json'))
      if (!res.ok) throw new Error(String(res.status))
      return res.json()
    },
  })

  const meeting = useMemo(
    () => indexData?.meetings.find((m) => meetingId(m) === routeMeetingId) || null,
    [indexData, routeMeetingId]
  )

  const {
    data: summaryContent,
    isLoading: isSummaryLoading,
    isError: isSummaryError,
  } = useQuery({
    queryKey: ['meeting-summary-content', meeting?.summary_path],
    queryFn: async (): Promise<string> => {
      const summaryPath = meeting?.summary_path
      if (!summaryPath) throw new Error('missing summary path')
      const res = await fetch(summaryPath)
      if (!res.ok) throw new Error(String(res.status))
      return res.text()
    },
    enabled: Boolean(meeting?.summary_path),
  })

  return (
    <div className="min-h-full bg-gradient-to-b from-slate-100 via-slate-100 to-slate-200 p-4 sm:p-6">
      <div className="mx-auto max-w-5xl space-y-4">
        <div className="sticky top-2 z-20 rounded-2xl border border-slate-200 bg-white/95 p-3 shadow-sm backdrop-blur">
          <button
            type="button"
            onClick={() => navigate('/data-explorer/meetings')}
            className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
          >
            <ArrowLeftIcon className="h-4 w-4" />
            Back to meetings
          </button>
        </div>

        {isIndexLoading && <p className="rounded-xl bg-white p-4 text-slate-500 shadow-sm">Loading meeting…</p>}
        {isIndexError && <p className="rounded-xl bg-white p-4 text-red-700 shadow-sm">Failed to load meetings index.</p>}
        {!isIndexLoading && !meeting && !isIndexError && (
          <p className="rounded-xl bg-white p-4 text-slate-500 shadow-sm">Meeting not found.</p>
        )}

        {meeting && (
          <>
            <section className="overflow-hidden rounded-3xl bg-gradient-to-r from-teal-700 via-teal-600 to-cyan-600 p-6 text-white shadow-md">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal-100">Meeting Summary</p>
              <h1 className="mt-2 text-3xl font-bold leading-tight">{meeting.jurisdiction_label}</h1>
              <div className="mt-3 flex flex-wrap gap-4 text-sm text-teal-50">
                <span className="inline-flex items-center gap-1.5">
                  <CalendarIcon className="h-4 w-4" />
                  {meeting.meeting_date}
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <MapPinIcon className="h-4 w-4" />
                  {meeting.jurisdiction_root}
                </span>
              </div>
              {meeting.categories && meeting.categories.length > 0 && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {meeting.categories.map((category) => (
                    <span
                      key={`${meeting.jurisdiction_root}-${meeting.meeting_date}-${category}`}
                      className="rounded-full bg-white/20 px-3 py-1 text-xs font-semibold ring-1 ring-white/35"
                    >
                      {category}
                    </span>
                  ))}
                </div>
              )}
            </section>

            <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7">
              {isSummaryLoading && <p className="text-slate-500">Loading summary…</p>}
              {isSummaryError && <p className="text-red-700">Failed to load summary markdown.</p>}
              {summaryContent && <MarkdownRenderer content={summaryContent} />}
            </section>
          </>
        )}
      </div>
    </div>
  )
}
