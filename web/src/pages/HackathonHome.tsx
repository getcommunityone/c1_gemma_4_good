import { Link } from 'react-router-dom'
import { MagnifyingGlassIcon, MapIcon, ArrowRightIcon } from '@heroicons/react/24/outline'

export default function HackathonHome() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-100 to-slate-200">
      <div className="mx-auto max-w-4xl px-4 py-16 text-center">
        <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">Gemma 4 Good · CommunityOne</p>
        <h1 className="mt-2 font-serif text-4xl font-bold text-slate-900 sm:text-5xl">
          Municipal meeting intelligence
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-lg text-slate-600">
          Explore ACS context for your county, search demo jurisdictions and meetings, and browse Gemma 4 policy
          outputs — static site, no API.
        </p>
        <div className="mt-10 grid gap-4 sm:grid-cols-2">
          <Link
            to="/search"
            className="group flex flex-col items-start rounded-xl border border-slate-300 bg-white p-6 text-left shadow-sm transition hover:border-teal-500 hover:shadow-md"
          >
            <MagnifyingGlassIcon className="h-8 w-8 text-teal-600" />
            <h2 className="mt-3 text-xl font-semibold text-slate-900">Search</h2>
            <p className="mt-1 text-sm text-slate-600">
              Offline search over jurisdictions, meetings, and policy topics (search-index.json).
            </p>
            <span className="mt-4 inline-flex items-center text-sm font-medium text-teal-700">
              Open search <ArrowRightIcon className="ml-1 h-4 w-4" />
            </span>
          </Link>
          <Link
            to="/data-explorer"
            className="group flex flex-col items-start rounded-xl border border-slate-300 bg-white p-6 text-left shadow-sm transition hover:border-teal-500 hover:shadow-md"
          >
            <MapIcon className="h-8 w-8 text-teal-600" />
            <h2 className="mt-3 text-xl font-semibold text-slate-900">Data explorer</h2>
            <p className="mt-1 text-sm text-slate-600">
              ACS map & scorecard, jurisdiction data quality, and Gemma meeting artifacts.
            </p>
            <span className="mt-4 inline-flex items-center text-sm font-medium text-teal-700">
              Explore data <ArrowRightIcon className="ml-1 h-4 w-4" />
            </span>
          </Link>
        </div>
        <p className="mt-12 text-xs text-slate-500">
          Pipeline notebook:{' '}
          <a
            href="https://github.com/getcommunityone/c1_gemma_4_good/blob/main/scripts/colab/02_run_meeting_llm.ipynb"
            className="underline"
            target="_blank"
            rel="noreferrer"
          >
            02_run_meeting_llm.ipynb
          </a>
        </p>
      </div>
    </div>
  )
}
