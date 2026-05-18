import { Link, Outlet, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { HomeIcon, MapIcon, Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'

const nav = [
  { name: 'Home', href: '/', icon: HomeIcon, exact: true },
  { name: 'Data explorer', href: '/data-explorer', icon: MapIcon },
]

export default function HackathonLayout() {
  const { pathname } = useLocation()
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <div className="flex min-h-screen flex-col bg-slate-200">
      <header className="border-b border-slate-300 bg-white shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center gap-4 px-4 py-3">
          <Link to="/" className="shrink-0 text-lg font-bold text-primary-600">
            Gemma 4 Good
          </Link>
          <div className="flex-1" />
          <button
            type="button"
            className="ml-auto rounded-lg p-2 text-slate-600 hover:bg-slate-100 sm:hidden"
            onClick={() => setMobileOpen((o) => !o)}
            aria-label="Menu"
          >
            {mobileOpen ? <XMarkIcon className="h-6 w-6" /> : <Bars3Icon className="h-6 w-6" />}
          </button>
          <nav className="hidden gap-1 sm:flex">
            {nav.map((item) => {
              const active =
                item.exact ? pathname === item.href : pathname.startsWith(item.href)
              return (
                <Link
                  key={item.href}
                  to={item.href}
                  className={[
                    'rounded-lg px-3 py-2 text-sm font-medium',
                    active ? 'bg-teal-50 text-teal-800' : 'text-slate-600 hover:bg-slate-100',
                  ].join(' ')}
                >
                  {item.name}
                </Link>
              )
            })}
          </nav>
        </div>
        {mobileOpen && (
          <nav className="border-t border-slate-200 px-4 py-2 sm:hidden">
            {nav.map((item) => (
              <Link
                key={item.href}
                to={item.href}
                className="block rounded-lg px-3 py-2 text-sm font-medium text-slate-700"
                onClick={() => setMobileOpen(false)}
              >
                {item.name}
              </Link>
            ))}
          </nav>
        )}
      </header>
      <main className="flex flex-1 flex-col">
        <Outlet />
      </main>
    </div>
  )
}

