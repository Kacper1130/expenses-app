// src/routes/_authenticated.tsx
import { createFileRoute, Outlet, redirect } from '@tanstack/react-router'
import { isAuthenticated } from '../utils/authGuards'
import { useAuth } from '../hooks/useAuth'

function AuthenticatedLayout() {
  const { logout } = useAuth()

  return (
      <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <header className="header">
          <div className="logo-row">
            <div className="logo-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--color-accent)" strokeWidth="2.5">
                <rect x="2" y="5" width="20" height="14" rx="2" />
                <path d="M2 10h20M6 15h4" />
              </svg>
            </div>
            <span className="logo-text">NaPół</span>
            <span className="logo-dot">.</span>
          </div>

          <button className="btn-logout" onClick={logout}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" />
            </svg>
            Wyloguj
          </button>
        </header>

        <main style={{ flex: 1 }}>
          <Outlet />
        </main>
      </div>
  )
}

export const Route = createFileRoute('/_authenticated')({
  beforeLoad: () => {
    if (!isAuthenticated()) {
      throw redirect({ to: '/login' })
    }
  },
  component: AuthenticatedLayout,
})