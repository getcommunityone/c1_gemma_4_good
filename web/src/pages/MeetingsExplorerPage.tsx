import { useQuery } from '@tanstack/react-query'
import { dataUrl } from '../lib/dataUrl'

interface GemmaMeetingRow {
  jurisdiction_label: string
  jurisdiction_root: string
  meeting_date: string
  calendar_year: string
  summary_path: string | null
  policy_json_path: string | null
  notes?: string
}

interface GemmaDemoIndex {
  generated_at: string
  meetings: GemmaMeetingRow[]
}

export default function MeetingsExplorerPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['gemma-demo-index'],
    queryFn: async (): Promise<GemmaDemoIndex> => {
      const res = await fetch(dataUrl('data/gemma-demo/index.json'))
      if (!res.ok) throw new Error(String(res.status))
      return res.json()
    },
  })

  return (
    <div className="rounded-lg bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">Gemma 4 meeting outputs</h2>
      <p className="mt-1 text-sm text-slate-600">
        Static index from the pipeline. Rebuild with{' '}
        <code className="text-xs">python scripts/colab/export/export_web_demo_index.py</code> after §6.
      </p>
      {isLoading && <p className="mt-4 text-slate-500">Loading…</p>}
      {isError && <p className="mt-4 text-red-700">Missing gemma-demo/index.json</p>}
      {data && (
        <>
          <p className="mt-2 text-xs text-slate-500">Generated {data.generated_at}</p>
          <ul className="mt-4 divide-y divide-slate-200">
            {data.meetings.map((m) => (
              <li key={`${m.jurisdiction_root}-${m.meeting_date}`} className="py-4">
                <p className="font-medium text-slate-900">{m.jurisdiction_label}</p>
                <p className="text-sm text-slate-600">
                  {m.meeting_date} · {m.jurisdiction_root}
                </p>
                {m.notes && <p className="mt-1 text-sm text-amber-800">{m.notes}</p>}
                <div className="mt-2 flex flex-wrap gap-3 text-sm">
                  {m.summary_path && (
                    <a className="text-teal-700 underline" href={m.summary_path} target="_blank" rel="noreferrer">
                      Summary
                    </a>
                  )}
                  {m.policy_json_path && (
                    <a className="text-teal-700 underline" href={m.policy_json_path} target="_blank" rel="noreferrer">
                      Policy JSON
                    </a>
                  )}
                  {!m.summary_path && !m.policy_json_path && (
                    <span className="text-slate-500">No exported files linked yet.</span>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  )
}
