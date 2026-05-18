import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  ArrowRightIcon,
  LockClosedIcon,
  DocumentTextIcon,
  CurrencyDollarIcon,
  AcademicCapIcon,
  ShieldCheckIcon,
  MapPinIcon,
} from '@heroicons/react/24/outline'
import {
  DocumentMagnifyingGlassIcon,
  AdjustmentsHorizontalIcon,
  LightBulbIcon,
  MusicalNoteIcon,
  LanguageIcon,
  UserGroupIcon,
  Squares2X2Icon,
  SparklesIcon,
} from '@heroicons/react/24/solid'

const COLAB_URL =
  'https://colab.research.google.com/github/getcommunityone/c1_gemma_4_good/blob/main/scripts/colab/run_in_colab.ipynb#scrollTo=VSC-9f203009'
const GITHUB_URL = 'https://github.com/getcommunityone/c1_gemma_4_good'

const fadeUp = {
  initial: { opacity: 0, y: 24 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: '-60px' },
  transition: { duration: 0.5 },
}

function Section({
  id,
  children,
  className = '',
}: {
  id?: string
  children: ReactNode
  className?: string
}) {
  return (
    <section id={id} className={`relative px-4 py-16 sm:py-20 ${className}`}>
      <motion.div className="mx-auto max-w-6xl" {...fadeUp}>
        {children}
      </motion.div>
    </section>
  )
}

function CivicCard({
  children,
  className = '',
  locked = false,
}: {
  children: ReactNode
  className?: string
  locked?: boolean
}) {
  return (
    <motion.div
      className={[
        'relative overflow-hidden rounded-xl border bg-white p-6 shadow-lg',
        locked ? 'border-amber-200/40 bg-slate-50/95' : 'border-white/20',
        className,
      ].join(' ')}
      whileHover={locked ? undefined : { y: -2, boxShadow: '0 12px 40px rgba(0,0,0,0.25)' }}
    >
      {locked && (
        <motion.div
          className="absolute inset-0 z-10 flex flex-col items-center justify-center gap-2 bg-slate-900/75 backdrop-blur-[2px]"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <LockClosedIcon className="h-10 w-10 text-amber-400" />
          <span className="text-xs font-semibold uppercase tracking-widest text-amber-200">Locked</span>
        </motion.div>
      )}
      {children}
    </motion.div>
  )
}

const DEMO_TILES = [
  { icon: DocumentMagnifyingGlassIcon, title: 'Scanned PDF OCR', desc: 'Demo 1 — visual recovery of dark-data PDFs' },
  { icon: AdjustmentsHorizontalIcon, title: 'Token-budget routing', desc: 'Demo 2 — HIGH for tables, LOW for body text' },
  { icon: LightBulbIcon, title: 'Policy deconstruction', desc: 'Demo 3 — reasoning + structured JSON' },
  { icon: MusicalNoteIcon, title: 'Audio drift detection', desc: 'Demo 4 — agenda vs. vote shifts' },
  { icon: LanguageIcon, title: 'Multilingual transcripts', desc: 'Demo 4a — plain speech in any language' },
  { icon: UserGroupIcon, title: 'Representation audits', desc: 'Demo 5 — contact-photo enrichment' },
  { icon: Squares2X2Icon, title: 'Cross-jurisdiction clusters', desc: 'Demo 6 — EmbeddingGemma similarity' },
  { icon: ShieldCheckIcon, title: 'ShieldGemma safety review', desc: 'Final pass before publication' },
]

const GEMMA_FEATURES = [
  { title: 'Native multimodality', desc: 'PDFs and audio as bytes — no separate OCR/ASR stack.' },
  { title: 'Long context', desc: '15-minute chunks + drift pass for hours-long meetings.' },
  { title: 'Strict JSON', desc: 'Schema-valid outputs from policy_analysis_v1.md.' },
  { title: 'Thinking mode', desc: 'Visible chain-of-reasoning for resident audit.' },
  { title: 'Edge / cloud routing', desc: 'E2B on edge; 26B/31B for heavy PDFs and audio.' },
  { title: 'Open-weight fallback', desc: 'Full pipeline offline on one L4 via Hugging Face.' },
  { title: 'ShieldGemma safety', desc: 'Hallucination & stereotype checks on every output.' },
  { title: 'EmbeddingGemma clustering', desc: 'Cross-town policy similarity at scale.' },
]

export default function HackathonHome() {
  return (
    <motion.div
      className="min-h-screen bg-civic-navy font-sans text-white"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      {/* Ambient layers */}
      <div className="pointer-events-none fixed inset-0 bg-civic-grid bg-[length:48px_48px] opacity-80" aria-hidden />
      <motion.div
        className="pointer-events-none fixed inset-0 bg-doc-texture"
        aria-hidden
        animate={{ opacity: [0.6, 0.85, 0.6] }}
        transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
      />

      {/* Top nav */}
      <header className="relative z-20 border-b border-white/10 bg-civic-navy/90 backdrop-blur-md">
        <motion.div
          className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-4"
          initial={{ y: -12, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
        >
          <Link to="/" className="flex items-center gap-2">
            <img src={`${import.meta.env.BASE_URL}communityone_logo.svg`} alt="" className="h-9 w-9" />
            <span className="font-display text-lg font-semibold text-white">CommunityOne</span>
          </Link>
          <nav className="hidden items-center gap-6 text-sm text-slate-300 sm:flex">
            <a href="#problem" className="hover:text-civic-gold-light">
              Problem
            </a>
            <a href="#pipeline" className="hover:text-civic-gold-light">
              Pipeline
            </a>
            <a href="#demos" className="hover:text-civic-gold-light">
              Demos
            </a>
            <a href="#gemma" className="hover:text-civic-gold-light">
              Gemma 4
            </a>
          </nav>
          <div className="flex shrink-0 items-center gap-2">
            <Link
              to="/data-explorer/"
              className="hidden rounded-lg bg-civic-gold px-3 py-2 text-sm font-semibold text-civic-navy hover:bg-civic-gold-light sm:inline-block"
            >
              Web demo
            </Link>
            <a
              href={COLAB_URL}
              target="_blank"
              rel="noreferrer"
              className="rounded-lg bg-civic-gold px-3 py-2 text-sm font-semibold text-civic-navy hover:bg-civic-gold-light"
            >
              Notebook
            </a>
          </div>
        </motion.div>
      </header>

      {/* 1. Hero */}
      <section className="relative overflow-hidden px-4 pb-20 pt-16 sm:pb-28 sm:pt-24">
        <motion.div
          className="mx-auto max-w-4xl text-center"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
        >
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-civic-gold">
            Gemma 4 Good · Digital Equity & Inclusivity
          </p>
          <h1 className="mt-4 font-display text-4xl font-bold leading-tight text-white sm:text-6xl lg:text-7xl">
            Defying Gravity for{' '}
            <span className="bg-gradient-to-r from-civic-gold-light via-civic-gold to-amber-500 bg-clip-text text-transparent">
              Local Democracy
            </span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-slate-300 sm:text-xl">
            Free public intelligence for every local government — meetings, money, legislation, and impact in
            one searchable view.
          </p>
          <motion.div
            className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.35 }}
          >
            <Link
              to="/data-explorer/"
              className="inline-flex items-center gap-2 rounded-xl bg-civic-gold px-8 py-3.5 text-base font-semibold text-civic-navy shadow-lg shadow-amber-900/30 transition hover:bg-civic-gold-light"
            >
              Try web demo
              <ArrowRightIcon className="h-5 w-5" />
            </Link>
            <a
              href={COLAB_URL}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 rounded-xl border-2 border-civic-gold/60 bg-transparent px-8 py-3.5 text-base font-semibold text-civic-gold-light transition hover:border-civic-gold hover:bg-white/5"
            >
              Run notebook
              <ArrowRightIcon className="h-5 w-5" />
            </a>
          </motion.div>
          <p className="mt-8 text-sm text-slate-500">
            No login · Static demo over Tuscaloosa County, AL & Sweet Grass County, MT
          </p>
          <p className="mt-3 text-sm text-slate-300">
            Published website data:{' '}
            <a
              href="https://huggingface.co/datasets/CommunityOne/one-jurisdiction-mapping-analysis"
              target="_blank"
              rel="noreferrer"
              className="font-semibold text-civic-gold-light underline underline-offset-4 transition hover:text-civic-gold"
            >
              Hugging Face dataset
            </a>
          </p>
          <div className="mx-auto mt-10 max-w-4xl overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-3 shadow-2xl shadow-slate-950/30 backdrop-blur-sm">
            <img
              src={`${import.meta.env.BASE_URL}images/not_there.png`}
              alt="CommunityOne web app preview"
              className="w-full rounded-2xl object-cover"
            />
          </div>
        </motion.div>
      </section>

      {/* 2. Problem */}
      <Section id="problem" className="bg-civic-navy-mid/80">
        <p className="text-center text-sm font-semibold uppercase tracking-widest text-civic-gold">The problem</p>
        <h2 className="mt-2 text-center font-display text-3xl font-bold text-white sm:text-4xl">
          Public data exists. Access doesn&apos;t.
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-slate-400">
          The federal government charges six figures for &quot;public&quot; health data. Meeting minutes sit in
          scanned PDFs. Policy language stays expert-only.
        </p>
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          <CivicCard locked>
            <CurrencyDollarIcon className="h-8 w-8 text-slate-400" />
            <h3 className="mt-4 text-lg font-semibold text-slate-800">Paywalled health data</h3>
            <p className="mt-2 text-sm text-slate-600">
              $500K+ for federal datasets; nonprofit registries behind thousand-dollar subscriptions.
            </p>
          </CivicCard>
          <CivicCard locked>
            <DocumentTextIcon className="h-8 w-8 text-slate-400" />
            <h3 className="mt-4 text-lg font-semibold text-slate-800">Buried meeting PDFs</h3>
            <p className="mt-2 text-sm text-slate-600">
              Agendas and minutes trapped in scans, silos, and county websites — not one search.
            </p>
          </CivicCard>
          <CivicCard locked>
            <AcademicCapIcon className="h-8 w-8 text-slate-400" />
            <h3 className="mt-4 text-lg font-semibold text-slate-800">Expert-only policy language</h3>
            <p className="mt-2 text-sm text-slate-600">
              Frame analysis and fiscal incidence jargon keep residents out of the conversation.
            </p>
          </CivicCard>
        </div>
      </Section>

      {/* 3. Equalizer / Pipeline */}
      <Section id="pipeline">
        <p className="text-center text-sm font-semibold uppercase tracking-widest text-civic-gold">The equalizer</p>
        <h2 className="mt-2 text-center font-display text-3xl font-bold sm:text-4xl">
          CommunityOne turns civic noise into plain-language insight.
        </h2>
        <div className="mt-14 overflow-hidden rounded-3xl border border-white/10 bg-civic-navy-light/60 p-3 shadow-2xl shadow-slate-950/30 sm:p-4">
          <motion.div
            className="overflow-hidden rounded-2xl bg-slate-950/30 p-2"
            initial={{ opacity: 0, y: 18 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <img
              src={`${import.meta.env.BASE_URL}images/cites_that_count.png`}
              alt="CommunityOne pipeline visual showing inputs, Gemma 4 processing, and public dashboard output"
              className="w-full rounded-xl object-cover"
            />
          </motion.div>
        </div>
      </Section>

      {/* 4. Demo cards */}
      <Section id="demos" className="bg-civic-navy-mid/60">
        <p className="text-center text-sm font-semibold uppercase tracking-widest text-civic-gold">Live capabilities</p>
        <h2 className="mt-2 text-center font-display text-3xl font-bold sm:text-4xl">What the pipeline delivers</h2>
        <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {DEMO_TILES.map((tile, i) => (
            <motion.div
              key={tile.title}
              className="rounded-xl border border-white/10 bg-white/95 p-5 text-civic-navy shadow-md"
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              whileHover={{ y: -4 }}
            >
              <tile.icon className="h-8 w-8 text-civic-gold" />
              <h3 className="mt-3 text-sm font-bold leading-snug">{tile.title}</h3>
              <p className="mt-1 text-xs text-slate-600">{tile.desc}</p>
            </motion.div>
          ))}
        </div>
        <p className="mt-8 text-center text-sm text-slate-400">
          Browse outputs in the{' '}
          <Link to="/data-explorer/meetings" className="font-medium text-civic-gold-light underline">
            meetings explorer
          </Link>{' '}
          after running the Colab pipeline.
        </p>
      </Section>

      {/* 5. Jurisdiction comparison */}
      <Section id="jurisdictions">
        <p className="text-center text-sm font-semibold uppercase tracking-widest text-civic-gold">
          Featured jurisdictions
        </p>
        <h2 className="mt-2 text-center font-display text-3xl font-bold sm:text-4xl">Urban county vs. rural county</h2>
        <motion.div
          className="mt-12 grid overflow-hidden rounded-2xl border border-white/15 md:grid-cols-2"
          {...fadeUp}
        >
          <div className="border-b border-white/10 bg-gradient-to-br from-amber-900/20 to-civic-navy-light p-8 md:border-b-0 md:border-r">
            <div className="flex items-center gap-2 text-civic-gold">
              <MapPinIcon className="h-5 w-5" />
              <span className="text-xs font-bold uppercase tracking-wider">Alabama · Urban</span>
            </div>
            <h3 className="mt-3 font-display text-2xl font-bold">Tuscaloosa County</h3>
            <p className="mt-1 text-sm text-slate-400">county_01125 · mid-size urban county</p>
            <ul className="mt-6 space-y-3 text-sm text-slate-300">
              <li>Meeting PDFs + audio on Drive-backed pipeline</li>
              <li>Policy JSON, drift diagrams, human summaries</li>
              <li>ACS context via data explorer map</li>
            </ul>
            <Link
              to="/search?q=tuscaloosa"
              className="mt-6 inline-flex items-center text-sm font-semibold text-civic-gold-light hover:text-civic-gold"
            >
              Search Tuscaloosa <ArrowRightIcon className="ml-1 h-4 w-4" />
            </Link>
          </div>
          <div className="bg-gradient-to-br from-slate-800/40 to-civic-navy-light p-8">
            <div className="flex items-center gap-2 text-civic-gold-light">
              <MapPinIcon className="h-5 w-5" />
              <span className="text-xs font-bold uppercase tracking-wider">Montana · Rural</span>
            </div>
            <h3 className="mt-3 font-display text-2xl font-bold">Big Timber / Sweet Grass</h3>
            <p className="mt-1 text-sm text-slate-400">Sweet Grass County · population ~3,500</p>
            <ul className="mt-6 space-y-3 text-sm text-slate-300">
              <li>Same pipeline — different scale, same schema</li>
              <li>Proves geography-from-folder layout (FIPS from paths)</li>
              <li>Cross-jurisdiction clustering in Demo 6</li>
            </ul>
            <Link
              to="/search?q=montana"
              className="mt-6 inline-flex items-center text-sm font-semibold text-civic-gold-light hover:text-civic-gold"
            >
              Search Montana <ArrowRightIcon className="ml-1 h-4 w-4" />
            </Link>
          </div>
        </motion.div>
      </Section>

      {/* 6. Why Gemma 4 */}
      <Section id="gemma" className="bg-civic-navy-mid/80">
        <p className="text-center text-sm font-semibold uppercase tracking-widest text-civic-gold">Why Gemma 4</p>
        <h2 className="mt-2 text-center font-display text-3xl font-bold sm:text-4xl">
          Eight capabilities, one corpus
        </h2>
        <motion.div
          className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4"
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: '-40px' }}
          variants={{
            hidden: {},
            show: { transition: { staggerChildren: 0.06 } },
          }}
        >
          {GEMMA_FEATURES.map((f) => (
            <motion.div
              key={f.title}
              variants={{
                hidden: { opacity: 0, scale: 0.96 },
                show: { opacity: 1, scale: 1 },
              }}
              className="rounded-xl border border-civic-gold/20 bg-civic-navy-light/80 p-5 backdrop-blur-sm"
            >
              <SparklesIcon className="h-5 w-5 text-civic-gold" />
              <h3 className="mt-2 text-sm font-bold text-civic-gold-light">{f.title}</h3>
              <p className="mt-1 text-xs leading-relaxed text-slate-400">{f.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </Section>

      {/* 7. Privacy */}
      <Section id="privacy">
        <h2 className="text-center font-display text-3xl font-bold sm:text-4xl">Privacy promise</h2>
        <div className="mt-10 grid gap-6 sm:grid-cols-3">
          {[
            { title: 'No login wall', desc: 'Public Colab, public GitHub, CC-BY-4.0 demo.' },
            { title: 'Offline mode available', desc: 'GOVERNANCE_LLM_BACKEND=huggingface on one GPU.' },
            { title: 'Safety review before publishing', desc: 'ShieldGemma on every LLM output.' },
          ].map((badge) => (
            <motion.div
              key={badge.title}
              className="flex flex-col items-center rounded-2xl border-2 border-civic-gold/40 bg-white/95 px-6 py-8 text-center text-civic-navy"
              whileHover={{ scale: 1.02 }}
            >
              <ShieldCheckIcon className="h-10 w-10 text-civic-gold" />
              <h3 className="mt-4 font-bold">{badge.title}</h3>
              <p className="mt-2 text-sm text-slate-600">{badge.desc}</p>
            </motion.div>
          ))}
        </div>
      </Section>

      {/* 8. Closing CTA */}
      <section className="relative px-4 py-24 sm:py-32">
        <motion.div
          className="mx-auto max-w-3xl rounded-3xl border border-civic-gold/30 bg-gradient-to-br from-civic-navy-light to-civic-navy-mid p-10 text-center shadow-2xl sm:p-14"
          {...fadeUp}
        >
          <h2 className="font-display text-3xl font-bold leading-snug text-white sm:text-4xl">
            Size shouldn&apos;t dictate importance.
            <br />
            <span className="text-civic-gold-light">Information shouldn&apos;t be a luxury good.</span>
          </h2>
          <p className="mx-auto mt-6 max-w-xl text-slate-400">
            You and I — defying gravity. Explore the demo or reproduce the full pipeline on your own data.
          </p>
          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link
              to="/data-explorer/"
              className="inline-flex items-center gap-2 rounded-xl bg-civic-gold px-8 py-3.5 font-semibold text-civic-navy hover:bg-civic-gold-light"
            >
              Try web demo
              <ArrowRightIcon className="h-5 w-5" />
            </Link>
            <a
              href={COLAB_URL}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 rounded-xl border border-white/30 px-8 py-3.5 font-semibold text-white hover:bg-white/10"
            >
              Run notebook
            </a>
          </div>
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noreferrer"
            className="mt-8 inline-block text-sm text-slate-500 hover:text-civic-gold"
          >
            View source on GitHub →
          </a>
        </motion.div>
      </section>

      <footer className="border-t border-white/10 px-4 py-8 text-center text-xs text-slate-500">
        CommunityOne · Gemma 4 Good Hackathon ·{' '}
        <Link to="/data-explorer" className="underline hover:text-slate-400">
          Data explorer
        </Link>
        {' · '}
        <Link to="/search" className="underline hover:text-slate-400">
          Search
        </Link>
      </footer>
    </motion.div>
  )
}
