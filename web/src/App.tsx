import { Routes, Route, Navigate, useParams, useLocation } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import HackathonLayout from './components/HackathonLayout'
import HackathonHome from './pages/HackathonHome'
import StaticSearch from './pages/StaticSearch'
import CensusMapPage from './pages/CensusMapPage'
import DataExplorerLayout from './components/DataExplorerLayout'
import DataExplorerScorecardPage from './pages/DataExplorerScorecardPage'
import JurisdictionMappingQualityPage from './pages/JurisdictionMappingQualityPage'
import MeetingsExplorerPage from './pages/MeetingsExplorerPage'
import MeetingSummaryPage from './pages/MeetingSummaryPage'
import { DATA_EXPLORER_MAP_BASE } from './utils/dataExplorerPaths'

function DataExplorerMapDefaultRedirect() {
  const { data, isError, isPending } = useQuery({
    queryKey: ['data-explorer-map-root-redirect'],
    queryFn: async (): Promise<string> => {
      const rm = await fetch(`${import.meta.env.BASE_URL}data/census-map/manifest.json`)
      if (!rm.ok) throw new Error('manifest')
      const manifest = (await rm.json()) as {
        vintage?: string
        vintages?: string[]
        metrics?: { slug: string }[]
      }
      const mv =
        Array.isArray(manifest.vintages) && manifest.vintages.length > 0
          ? manifest.vintages
          : manifest.vintage
            ? [manifest.vintage]
            : []
      let vintages = mv
      const rt = await fetch(`${import.meta.env.BASE_URL}data/census-map/state_trends.json`)
      if (rt.ok) {
        const t = (await rt.json()) as { vintages?: string[] }
        if (t.vintages?.length) vintages = t.vintages
      }
      const v = vintages.length ? vintages[vintages.length - 1]! : (manifest.vintage ?? '2024')
      const metric = manifest.metrics?.[0]?.slug ?? 'median_household_income'
      return `${DATA_EXPLORER_MAP_BASE}/us/${v}/${metric}`
    },
  })
  if (isPending) return <div className="p-8 text-slate-600">Loading map…</div>
  if (isError) {
    return <Navigate to={`${DATA_EXPLORER_MAP_BASE}/us/2024/median_household_income`} replace />
  }
  return <Navigate to={data!} replace />
}

function CensusCountyAliasRedirect() {
  const { vintage, metric } = useParams<{ vintage: string; metric: string }>()
  const { search } = useLocation()
  const v = vintage ?? '2024'
  const m = metric ?? 'median_household_income'
  return <Navigate to={`${DATA_EXPLORER_MAP_BASE}/us/${v}/${m}${search}`} replace />
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HackathonHome />} />
      <Route path="/" element={<HackathonLayout />}>
        <Route path="search" element={<StaticSearch />} />
        <Route path="data-explorer" element={<DataExplorerLayout />}>
          <Route index element={<DataExplorerMapDefaultRedirect />} />
          <Route path="scorecard" element={<DataExplorerScorecardPage />} />
          <Route path="jurisdiction-quality" element={<JurisdictionMappingQualityPage />} />
          <Route path="meetings" element={<MeetingsExplorerPage />} />
          <Route path="meetings/:meetingId" element={<MeetingSummaryPage />} />
          <Route path="map/us/:vintage/:metric" element={<CensusMapPage />} />
          <Route path="map/state/:stateFips/:vintage/:metric" element={<CensusMapPage />} />
          <Route path="map/place/:stateFips/:vintage/:metric" element={<CensusMapPage />} />
          <Route path="map" element={<DataExplorerMapDefaultRedirect />} />
        </Route>
        <Route path="census-map/county/:vintage/:metric" element={<CensusCountyAliasRedirect />} />
        <Route path="census-map/*" element={<Navigate to="/data-explorer" replace />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
