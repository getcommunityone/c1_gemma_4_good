import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { MarkdownRenderer } from './MarkdownRenderer'

interface MeetingDetailProps {
  summaryPath: string
  jurisdiction: string
  meetingDate: string
  onBack: () => void
}

export const MeetingDetail: React.FC<MeetingDetailProps> = ({
  summaryPath,
  jurisdiction,
  meetingDate,
  onBack,
}) => {
  const { data: content, isLoading, isError } = useQuery({
    queryKey: ['meeting-summary', summaryPath],
    queryFn: async (): Promise<string> => {
      const res = await fetch(summaryPath)
      if (!res.ok) throw new Error(String(res.status))
      return res.text()
    },
  })

  return (
    <div className="fixed inset-0 z-50 overflow-auto bg-black bg-opacity-50 p-4">
      <div className="mx-auto max-w-3xl bg-white rounded-lg shadow-lg">
        <div className="sticky top-0 border-b border-slate-200 bg-white p-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">{jurisdiction}</h1>
            <p className="text-sm text-slate-600">{meetingDate}</p>
          </div>
          <button
            onClick={onBack}
            className="px-4 py-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-900 font-medium transition"
          >
            ← Back
          </button>
        </div>

        <div className="p-6">
          {isLoading && <p className="text-slate-500">Loading meeting summary…</p>}
          {isError && <p className="text-red-700">Failed to load meeting summary</p>}
          {content && <MarkdownRenderer content={content} />}
        </div>
      </div>
    </div>
  )
}

export default MeetingDetail
