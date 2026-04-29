import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Shield, Menu, X, User, LogOut, ChevronDown, LayoutDashboard } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../services/authContext'

const baseNavLinks = [
  { label: 'Product', href: '#product' },
  { label: 'Features', href: '#features' },
  { label: 'Pricing', href: '#pricing' },
]

export default function Navbar({ currentRoute, isAuthenticated, setIsAuthenticated }) {
  const navLinks = [
    ...baseNavLinks,
    isAuthenticated ? { label: 'Profile', href: '#profile' } : { label: 'Sign In', href: '#login' }
  ]
  const [scrolled, setScrolled] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const [profileOpen, setProfileOpen] = useState(false)
  const profileRef = useRef(null)
  const { isAuthenticated, user, logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // Close profile dropdown on outside click
  useEffect(() => {
    const handleClick = (e) => {
      if (profileRef.current && !profileRef.current.contains(e.target)) {
        setProfileOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  const getInitials = (name) => {
    if (!name) return 'U'
    return name
      .split(' ')
      .map((w) => w[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }

  return (
    <motion.nav
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled
          ? 'bg-midnight/80 backdrop-blur-xl border-b border-border/50 shadow-lg shadow-black/20'
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 lg:h-[72px]">
          {/* Logo */}
          <a href="#home" className="flex items-center gap-2.5 group">
            <div className="relative">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-electric to-violet flex items-center justify-center shadow-lg shadow-electric/20 group-hover:shadow-electric/40 transition-shadow duration-300">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <div className="absolute inset-0 rounded-lg bg-gradient-to-br from-electric to-violet opacity-0 group-hover:opacity-40 blur-xl transition-opacity duration-500" />
            </div>
            <span className="text-lg font-bold tracking-tight text-text-primary">
              Code<span className="text-electric">Guard</span>
            </span>
          </a>

          {/* Desktop Links */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="px-4 py-2 text-sm font-medium text-text-secondary hover:text-text-primary transition-colors duration-200 rounded-lg hover:bg-surface/50"
              >
                {link.label}
              </a>
            ))}
            {!isAuthenticated && (
              <a
                href="#login"
                className="px-4 py-2 text-sm font-medium text-text-secondary hover:text-text-primary transition-colors duration-200 rounded-lg hover:bg-surface/50"
              >
                Sign In
              </a>
            )}
          </div>

          {/* CTA / User Profile */}
          <div className="hidden md:flex items-center gap-3">
            {isAuthenticated && user ? (
              <div className="relative" ref={profileRef}>
                <button
                  onClick={() => setProfileOpen(!profileOpen)}
                  className="flex items-center gap-2.5 px-3 py-2 rounded-xl hover:bg-surface/60 transition-all duration-200 cursor-pointer group"
                >
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-electric to-violet flex items-center justify-center text-xs font-bold text-white shadow-md shadow-electric/15">
                    {getInitials(user.full_name)}
                  </div>
                  <div className="text-left hidden lg:block">
                    <p className="text-sm font-medium text-text-primary leading-tight">
                      {user.full_name || 'Kullanıcı'}
                    </p>
                    <p className="text-[11px] text-text-muted leading-tight">{user.email}</p>
                  </div>
                  <ChevronDown
                    className={`w-3.5 h-3.5 text-text-muted transition-transform duration-200 ${
                      profileOpen ? 'rotate-180' : ''
                    }`}
                  />
                </button>

                {/* Dropdown */}
                <AnimatePresence>
                  {profileOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: 8, scale: 0.96 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: 8, scale: 0.96 }}
                      transition={{ duration: 0.2 }}
                      className="absolute right-0 mt-2 w-56 glass rounded-xl border border-border/50 shadow-xl shadow-black/30 overflow-hidden"
                    >
                      <div className="px-4 py-3 border-b border-border/30">
                        <p className="text-sm font-medium text-text-primary">{user.full_name || 'Kullanıcı'}</p>
                        <p className="text-xs text-text-muted truncate">{user.email}</p>
                      </div>
                      <div className="py-1.5">
                        <button
                          onClick={() => {
                            navigate('/dashboard')
                            setProfileOpen(false)
                          }}
                          className="flex items-center gap-2.5 px-4 py-2.5 text-sm text-text-secondary hover:text-text-primary hover:bg-surface/50 transition-colors w-full cursor-pointer"
                        >
                          <LayoutDashboard className="w-4 h-4" />
                          Dashboard
                        </button>
                        <button
                          onClick={() => {
                            logout()
                            setProfileOpen(false)
                            navigate('/')
                          }}
                          className="flex items-center gap-2.5 px-4 py-2.5 text-sm text-rose hover:bg-rose/5 transition-colors w-full cursor-pointer"
                        >
                          <LogOut className="w-4 h-4" />
                          Çıkış Yap
                        </button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ) : (
              <a
                href="#pricing"
                className="shimmer-btn px-5 py-2.5 text-sm font-semibold bg-electric hover:bg-electric-glow text-white rounded-lg transition-all duration-300 shadow-lg shadow-electric/25 hover:shadow-electric/40"
              >
                Get Started
              </a>
            )}
          </div>

          {/* Mobile Toggle */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 text-text-secondary hover:text-text-primary transition-colors"
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="md:hidden bg-midnight-light/95 backdrop-blur-xl border-b border-border/50 overflow-hidden"
          >
            <div className="px-6 py-4 space-y-1">
              {navLinks.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  onClick={() => setMobileOpen(false)}
                  className="block px-4 py-3 text-sm font-medium text-text-secondary hover:text-text-primary hover:bg-surface/50 rounded-lg transition-colors"
                >
                  {link.label}
                </a>
              ))}

              {isAuthenticated && user ? (
                <>
                  <div className="pt-3 border-t border-border/50">
                    <div className="flex items-center gap-3 px-4 py-3">
                      <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-electric to-violet flex items-center justify-center text-xs font-bold text-white">
                        {getInitials(user.full_name)}
                      </div>
                      <div>
                        <p className="text-sm font-medium text-text-primary">{user.full_name || 'Kullanıcı'}</p>
                        <p className="text-xs text-text-muted">{user.email}</p>
                      </div>
                    </div>
                    <button
                      onClick={() => {
                        logout()
                        setMobileOpen(false)
                      }}
                      className="flex items-center gap-2.5 px-4 py-3 text-sm text-rose w-full rounded-lg hover:bg-rose/5 transition-colors cursor-pointer"
                    >
                      <LogOut className="w-4 h-4" />
                      Çıkış Yap
                    </button>
                  </div>
                </>
              ) : (
                <>
                  <a
                    href="#login"
                    onClick={() => setMobileOpen(false)}
                    className="block px-4 py-3 text-sm font-medium text-text-secondary hover:text-text-primary hover:bg-surface/50 rounded-lg transition-colors"
                  >
                    Sign In
                  </a>
                  <div className="pt-3 border-t border-border/50">
                    <a
                      href="#pricing"
                      className="block w-full text-center px-5 py-3 text-sm font-semibold bg-electric text-white rounded-lg"
                    >
                      Get Started
                    </a>
                  </div>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  )
}
