import React, { useRef, useState } from 'react'
import { motion, useInView, AnimatePresence } from 'framer-motion'
import { LogIn, UserPlus, Mail, Lock, User, ArrowRight, Eye, EyeOff, Loader2, CheckCircle } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../services/authContext'
import { useToast } from './Toast'

export default function AuthSection({ setIsAuthenticated }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-80px' })
  const [activeTab, setActiveTab] = useState('login')
  const [showPassword, setShowPassword] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Form state
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})

  const { login, register, isAuthenticated, user } = useAuth()
  const toast = useToast()
  const navigate = useNavigate()

  const resetForm = () => {
    setFullName('')
    setEmail('')
    setPassword('')
    setFieldErrors({})
  }

  const switchTab = (tab) => {
    setActiveTab(tab)
    resetForm()
  }

  const validate = () => {
    const errors = {}
    if (!email.trim()) errors.email = 'Email gerekli'
    else if (!/\S+@\S+\.\S+/.test(email)) errors.email = 'Geçerli bir email girin'
    if (!password.trim()) errors.password = 'Şifre gerekli'
    else if (password.length < 6) errors.password = 'Şifre en az 6 karakter olmalı'
    if (activeTab === 'register' && !fullName.trim()) errors.fullName = 'İsim gerekli'
    setFieldErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validate()) return
    setIsSubmitting(true)

    try {
      if (activeTab === 'login') {
        await login(email, password)
        toast.success('Giriş başarılı! Hoş geldiniz.')
      } else {
        await register(email, password, fullName)
        toast.success('Hesap oluşturuldu! Hoş geldiniz.')
      }
      // Redirect to dashboard after successful auth
      setTimeout(() => navigate('/dashboard'), 500)
      resetForm()
    } catch (err) {
      toast.error(err.message || 'Bir hata oluştu')
    } finally {
      setIsSubmitting(false)
    }
  }

  // ── Logged-in state ──────────────────────────
  if (isAuthenticated && user) {
    return (
      <section id="login" className="relative py-20 lg:py-32">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-lg mx-auto"
          >
            <div className="glass rounded-2xl p-8 sm:p-10 text-center glow-blue">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-emerald to-neon-cyan flex items-center justify-center mx-auto mb-5 shadow-lg shadow-emerald/25">
                <CheckCircle className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-text-primary mb-2">Hoş Geldiniz!</h3>
              <p className="text-text-secondary mb-1">{user.full_name || 'Kullanıcı'}</p>
              <p className="text-text-muted text-sm mb-6">{user.email}</p>
              <button
                onClick={() => navigate('/dashboard')}
                className="shimmer-btn inline-flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-semibold bg-electric hover:bg-electric-glow text-white shadow-lg shadow-electric/25 hover:shadow-electric/40 transition-all duration-300 cursor-pointer"
              >
                Dashboard'a Git
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        </div>
      </section>
    )
  }

  // ── Auth Form ────────────────────────────────
  return (
    <section id="login" className="relative py-20 lg:py-32">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          {/* Left — Copy */}
          <motion.div
            ref={ref}
            initial={{ opacity: 0, x: -40 }}
            animate={isInView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.7 }}
          >
            <span className="inline-block px-3 py-1 mb-4 text-xs font-semibold uppercase tracking-wider text-emerald bg-emerald/10 rounded-full border border-emerald/20">
              Join Now
            </span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-text-primary mb-6 leading-tight">
              Start Shipping{' '}
              <span className="bg-gradient-to-r from-emerald to-neon-cyan bg-clip-text text-transparent">
                Better Code
              </span>{' '}
              Today
            </h2>
            <p className="text-lg text-text-secondary leading-relaxed mb-8">
              Create your free account and get instant access to AI-powered code analysis. No credit card required.
            </p>
            <div className="space-y-4">
              {[
                'Free tier with 3 projects included',
                'Instant setup — no configuration needed',
                'Secure authentication with 2FA support',
                'Sync across all your devices',
              ].map((item) => (
                <div key={item} className="flex items-start gap-3">
                  <div className="w-5 h-5 rounded-full bg-emerald/15 flex items-center justify-center shrink-0 mt-0.5">
                    <ArrowRight className="w-3 h-3 text-emerald" />
                  </div>
                  <span className="text-sm text-text-secondary">{item}</span>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Right — Auth Card */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            animate={isInView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.7, delay: 0.2 }}
          >
            <div className="glass rounded-2xl overflow-hidden glow-blue max-w-md mx-auto lg:ml-auto">
              {/* Tabs */}
              <div className="flex border-b border-border/40">
                <button
                  onClick={() => switchTab('login')}
                  className={`flex-1 flex items-center justify-center gap-2 py-4 text-sm font-semibold transition-all duration-300 cursor-pointer ${
                    activeTab === 'login'
                      ? 'text-electric border-b-2 border-electric bg-electric/5'
                      : 'text-text-muted hover:text-text-secondary'
                  }`}
                >
                  <LogIn className="w-4 h-4" />
                  Login
                </button>
                <button
                  onClick={() => switchTab('register')}
                  className={`flex-1 flex items-center justify-center gap-2 py-4 text-sm font-semibold transition-all duration-300 cursor-pointer ${
                    activeTab === 'register'
                      ? 'text-electric border-b-2 border-electric bg-electric/5'
                      : 'text-text-muted hover:text-text-secondary'
                  }`}
                >
                  <UserPlus className="w-4 h-4" />
                  Register
                </button>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="p-6 sm:p-8">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={activeTab}
                    initial={{ opacity: 0, y: 12 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -12 }}
                    transition={{ duration: 0.25 }}
                  >
                    <div className="space-y-4">
                      {/* Name field — only for register */}
                      {activeTab === 'register' && (
                        <div>
                          <label className="block text-xs font-medium text-text-muted mb-1.5 uppercase tracking-wider">
                            Full Name
                          </label>
                          <div className="relative">
                            <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
                            <input
                              id="auth-fullname"
                              type="text"
                              value={fullName}
                              onChange={(e) => setFullName(e.target.value)}
                              placeholder="John Doe"
                              className={`w-full pl-11 pr-4 py-3 rounded-xl bg-midnight-lighter border text-sm text-text-primary placeholder-text-muted outline-none focus:border-electric/50 focus:ring-1 focus:ring-electric/20 transition-all ${
                                fieldErrors.fullName ? 'border-rose/60' : 'border-border/50'
                              }`}
                            />
                          </div>
                          {fieldErrors.fullName && (
                            <p className="text-xs text-rose mt-1.5">{fieldErrors.fullName}</p>
                          )}
                        </div>
                      )}

                      {/* Email */}
                      <div>
                        <label className="block text-xs font-medium text-text-muted mb-1.5 uppercase tracking-wider">
                          Email Address
                        </label>
                        <div className="relative">
                          <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
                          <input
                            id="auth-email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="you@example.com"
                            className={`w-full pl-11 pr-4 py-3 rounded-xl bg-midnight-lighter border text-sm text-text-primary placeholder-text-muted outline-none focus:border-electric/50 focus:ring-1 focus:ring-electric/20 transition-all ${
                              fieldErrors.email ? 'border-rose/60' : 'border-border/50'
                            }`}
                          />
                        </div>
                        {fieldErrors.email && (
                          <p className="text-xs text-rose mt-1.5">{fieldErrors.email}</p>
                        )}
                      </div>

                      {/* Password */}
                      <div>
                        <label className="block text-xs font-medium text-text-muted mb-1.5 uppercase tracking-wider">
                          Password
                        </label>
                        <div className="relative">
                          <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
                          <input
                            id="auth-password"
                            type={showPassword ? 'text' : 'password'}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••"
                            className={`w-full pl-11 pr-11 py-3 rounded-xl bg-midnight-lighter border text-sm text-text-primary placeholder-text-muted outline-none focus:border-electric/50 focus:ring-1 focus:ring-electric/20 transition-all ${
                              fieldErrors.password ? 'border-rose/60' : 'border-border/50'
                            }`}
                          />
                          <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-3.5 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-secondary transition-colors cursor-pointer"
                          >
                            {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                          </button>
                        </div>
                        {fieldErrors.password && (
                          <p className="text-xs text-rose mt-1.5">{fieldErrors.password}</p>
                        )}
                      </div>

                      {/* Forgot password link — only for login */}
                      {activeTab === 'login' && (
                        <div className="flex justify-end">
                          <a href="#" className="text-xs text-electric hover:text-electric-glow transition-colors">
                            Forgot password?
                          </a>
                        </div>
                      )}

                      {/* Submit */}
                      <button
                        type="submit"
                        disabled={isSubmitting}
                        className="shimmer-btn w-full py-3 px-6 rounded-xl text-sm font-semibold bg-electric hover:bg-electric-glow text-white shadow-lg shadow-electric/25 hover:shadow-electric/40 transition-all duration-300 cursor-pointer mt-2 disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                      >
                        {isSubmitting ? (
                          <>
                            <Loader2 className="w-4 h-4 animate-spin" />
                            {activeTab === 'login' ? 'Signing In...' : 'Creating Account...'}
                          </>
                        ) : (
                          activeTab === 'login' ? 'Sign In' : 'Create Account'
                        )}
                      </button>
                    </div>
                  </motion.div>
                </AnimatePresence>
              </form>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
