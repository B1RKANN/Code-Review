import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { User, Mail, Shield, Activity, Key, LogOut, CheckCircle, AlertTriangle } from 'lucide-react'

export default function Profile({ setIsAuthenticated }) {
  const [userData, setUserData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate fetching from /me endpoint
    // In a real app, you would fetch from your backend here
    // Example: fetch('http://localhost:8000/api/auth/me', { headers: { Authorization: `Bearer ${token}` } })
    setTimeout(() => {
      setUserData({
        id: "64a7f9b8c3d2e1f0a4b5c6d7",
        full_name: "Alex Developer",
        email: "alex@example.com",
        is_active: true,
        stats: {
          scans: 142,
          issues_fixed: 89,
          security_score: 98
        }
      })
      setLoading(false)
    }, 1000)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center pt-20">
        <div className="w-12 h-12 border-4 border-electric/30 border-t-electric rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <div className="min-h-screen pt-24 pb-12 px-6 lg:px-8 max-w-7xl mx-auto relative z-10">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8"
      >
        <h1 className="text-3xl md:text-4xl font-bold text-text-primary mb-2">Account Profile</h1>
        <p className="text-text-secondary">Manage your personal settings and view your CodeGuard statistics.</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: User Info Card */}
        <div className="lg:col-span-1 space-y-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="p-[1px] rounded-2xl bg-gradient-to-br from-border/50 via-border/10 to-transparent"
          >
            <div className="bg-surface/80 backdrop-blur-xl rounded-2xl p-6 h-full border border-white/5">
              <div className="flex flex-col items-center text-center">
                <div className="relative mb-4">
                  <div className="w-24 h-24 rounded-full bg-gradient-to-br from-electric to-violet p-[2px]">
                    <div className="w-full h-full rounded-full bg-surface flex items-center justify-center overflow-hidden">
                      <User className="w-10 h-10 text-electric" />
                    </div>
                  </div>
                  {userData?.is_active && (
                    <div className="absolute bottom-1 right-1 w-5 h-5 bg-green-500 border-2 border-surface rounded-full flex items-center justify-center">
                      <CheckCircle className="w-3 h-3 text-white" />
                    </div>
                  )}
                </div>
                
                <h2 className="text-xl font-bold text-text-primary mb-1">{userData?.full_name || 'CodeGuard User'}</h2>
                <div className="flex items-center gap-2 text-text-secondary mb-6">
                  <Mail className="w-4 h-4" />
                  <span className="text-sm">{userData?.email}</span>
                </div>

                <div className="w-full space-y-3">
                  <button className="w-full py-2.5 px-4 rounded-lg bg-white/5 hover:bg-white/10 border border-white/5 text-sm font-medium transition-colors flex items-center justify-center gap-2">
                    <Key className="w-4 h-4" />
                    Change Password
                  </button>
                  <button 
                    onClick={() => {
                      localStorage.removeItem('auth')
                      setIsAuthenticated(false)
                      window.location.hash = '#home'
                    }}
                    className="w-full py-2.5 px-4 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/10 text-sm font-medium transition-colors flex items-center justify-center gap-2"
                  >
                    <LogOut className="w-4 h-4" />
                    Sign Out
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Right Column: Stats & Settings */}
        <div className="lg:col-span-2 space-y-6">
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="p-[1px] rounded-2xl bg-gradient-to-br from-electric/30 to-transparent"
            >
              <div className="bg-surface/80 backdrop-blur-xl rounded-2xl p-6 h-full border border-white/5 flex flex-col justify-center">
                <div className="flex items-center gap-3 mb-2">
                  <div className="p-2 rounded-lg bg-electric/10 text-electric">
                    <Activity className="w-5 h-5" />
                  </div>
                  <span className="text-sm font-medium text-text-secondary">Total Scans</span>
                </div>
                <div className="text-3xl font-bold text-text-primary">{userData?.stats?.scans}</div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="p-[1px] rounded-2xl bg-gradient-to-br from-green-500/30 to-transparent"
            >
              <div className="bg-surface/80 backdrop-blur-xl rounded-2xl p-6 h-full border border-white/5 flex flex-col justify-center">
                <div className="flex items-center gap-3 mb-2">
                  <div className="p-2 rounded-lg bg-green-500/10 text-green-400">
                    <Shield className="w-5 h-5" />
                  </div>
                  <span className="text-sm font-medium text-text-secondary">Issues Fixed</span>
                </div>
                <div className="text-3xl font-bold text-text-primary">{userData?.stats?.issues_fixed}</div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
              className="p-[1px] rounded-2xl bg-gradient-to-br from-violet/30 to-transparent"
            >
              <div className="bg-surface/80 backdrop-blur-xl rounded-2xl p-6 h-full border border-white/5 flex flex-col justify-center">
                <div className="flex items-center gap-3 mb-2">
                  <div className="p-2 rounded-lg bg-violet/10 text-violet">
                    <AlertTriangle className="w-5 h-5" />
                  </div>
                  <span className="text-sm font-medium text-text-secondary">Security Score</span>
                </div>
                <div className="flex items-end gap-1">
                  <div className="text-3xl font-bold text-text-primary">{userData?.stats?.security_score}</div>
                  <div className="text-sm text-text-secondary mb-1">/ 100</div>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Account Details Form */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="p-[1px] rounded-2xl bg-gradient-to-br from-border/50 via-border/10 to-transparent"
          >
            <div className="bg-surface/80 backdrop-blur-xl rounded-2xl p-6 border border-white/5">
              <h3 className="text-lg font-semibold text-text-primary mb-6">Personal Information</h3>
              
              <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="text-sm font-medium text-text-secondary">Full Name</label>
                    <input 
                      type="text" 
                      defaultValue={userData?.full_name}
                      className="w-full bg-midnight/50 border border-border/50 rounded-lg px-4 py-2.5 text-text-primary focus:outline-none focus:border-electric transition-colors"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-sm font-medium text-text-secondary">Email Address</label>
                    <input 
                      type="email" 
                      defaultValue={userData?.email}
                      className="w-full bg-midnight/50 border border-border/50 rounded-lg px-4 py-2.5 text-text-primary focus:outline-none focus:border-electric transition-colors"
                      readOnly
                    />
                  </div>
                </div>
                
                <div className="pt-4 flex justify-end">
                  <button type="submit" className="px-5 py-2.5 bg-electric hover:bg-electric-glow text-white rounded-lg font-medium transition-all shadow-lg shadow-electric/20">
                    Save Changes
                  </button>
                </div>
              </form>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}
