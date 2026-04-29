import React, { useRef, useState } from 'react'
import { motion, useInView, AnimatePresence } from 'framer-motion'
import { LogIn, UserPlus, Mail, Lock, User, ArrowRight, Eye, EyeOff } from 'lucide-react'

export default function AuthSection({ setIsAuthenticated }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-80px' })
  const [activeTab, setActiveTab] = useState('login')
  const [showPassword, setShowPassword] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    // Simulate authentication
    localStorage.setItem('auth', 'true')
    setIsAuthenticated(true)
    // Redirect to profile upon successful sign in/register
    window.location.hash = '#profile'
  }

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
                  onClick={() => setActiveTab('login')}
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
                  onClick={() => setActiveTab('register')}
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
              <div className="p-6 sm:p-8">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={activeTab}
                    initial={{ opacity: 0, y: 12 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -12 }}
                    transition={{ duration: 0.25 }}
                  >
                    <form onSubmit={handleSubmit} className="space-y-4">
                      {/* Name field — only for register */}
                      {activeTab === 'register' && (
                        <div>
                          <label className="block text-xs font-medium text-text-muted mb-1.5 uppercase tracking-wider">
                            Full Name
                          </label>
                          <div className="relative">
                            <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
                            <input
                              type="text"
                              placeholder="John Doe"
                              className="w-full pl-11 pr-4 py-3 rounded-xl bg-midnight-lighter border border-border/50 text-sm text-text-primary placeholder-text-muted outline-none focus:border-electric/50 focus:ring-1 focus:ring-electric/20 transition-all"
                            />
                          </div>
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
                            type="email"
                            placeholder="you@example.com"
                            className="w-full pl-11 pr-4 py-3 rounded-xl bg-midnight-lighter border border-border/50 text-sm text-text-primary placeholder-text-muted outline-none focus:border-electric/50 focus:ring-1 focus:ring-electric/20 transition-all"
                          />
                        </div>
                      </div>

                      {/* Password */}
                      <div>
                        <label className="block text-xs font-medium text-text-muted mb-1.5 uppercase tracking-wider">
                          Password
                        </label>
                        <div className="relative">
                          <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
                          <input
                            type={showPassword ? 'text' : 'password'}
                            placeholder="••••••••"
                            className="w-full pl-11 pr-11 py-3 rounded-xl bg-midnight-lighter border border-border/50 text-sm text-text-primary placeholder-text-muted outline-none focus:border-electric/50 focus:ring-1 focus:ring-electric/20 transition-all"
                          />
                          <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-3.5 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-secondary transition-colors cursor-pointer"
                          >
                            {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                          </button>
                        </div>
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
                      <button type="submit" className="shimmer-btn w-full py-3 px-6 rounded-xl text-sm font-semibold bg-electric hover:bg-electric-glow text-white shadow-lg shadow-electric/25 hover:shadow-electric/40 transition-all duration-300 cursor-pointer mt-2">
                        {activeTab === 'login' ? 'Sign In' : 'Create Account'}
                      </button>

                    </form>
                  </motion.div>
                </AnimatePresence>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
