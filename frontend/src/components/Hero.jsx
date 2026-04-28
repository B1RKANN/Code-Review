import React from 'react'
import { motion } from 'framer-motion'
import { Download, BookOpen, ArrowRight, Sparkles } from 'lucide-react'

export default function Hero() {
  return (
    <section id="product" className="relative pt-32 pb-20 lg:pt-44 lg:pb-32 overflow-hidden">
      {/* Subtle grid */}
      <div className="absolute inset-0 grid-pattern opacity-30" />

      <div className="relative max-w-7xl mx-auto px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 mb-8 rounded-full glass border border-electric/20 text-sm font-medium text-electric"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI-Powered Static Analysis</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </motion.div>

          {/* Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="text-5xl sm:text-6xl lg:text-8xl font-black tracking-tight leading-none mb-6"
          >
            <span className="block text-text-primary">Code Quality,</span>
            <span className="block mt-2 bg-gradient-to-r from-electric via-neon-cyan to-violet bg-clip-text text-transparent pb-4">
              Reimagined.
            </span>
          </motion.h1>

          {/* Subtext */}
          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.25 }}
            className="text-lg sm:text-xl text-text-secondary max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            The desktop-first analysis engine that masters{' '}
            <span className="text-text-primary font-medium">SOLID principles</span>,
            detects{' '}
            <span className="text-amber font-medium">security vulnerabilities</span>,
            and refactors your code with{' '}
            <span className="text-neon-cyan font-medium">LLM intelligence</span>
            — all in one unified workspace.
          </motion.p>

          {/* CTAs */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.4 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <a
              href="#download"
              className="shimmer-btn group relative inline-flex items-center gap-3 px-8 py-4 text-base font-semibold bg-gradient-to-r from-electric to-blue-500 text-white rounded-xl shadow-2xl shadow-electric/25 hover:shadow-electric/40 transition-all duration-300 hover:scale-[1.02]"
            >
              <Download className="w-5 h-5" />
              Download for Desktop
              <span className="absolute -top-1 -right-1 w-3 h-3 rounded-full bg-emerald animate-pulse-glow" />
            </a>
            <a
              href="#features"
              className="group inline-flex items-center gap-2.5 px-8 py-4 text-base font-semibold text-text-secondary hover:text-text-primary border border-border hover:border-border-light rounded-xl transition-all duration-300 hover:bg-surface/30"
            >
              <BookOpen className="w-5 h-5" />
              View Documentation
              <ArrowRight className="w-4 h-4 opacity-0 -ml-2 group-hover:opacity-100 group-hover:ml-0 transition-all duration-300" />
            </a>
          </motion.div>

          {/* Stats row */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.7 }}
            className="mt-16 flex flex-wrap items-center justify-center gap-8 sm:gap-12"
          >
            {[
              { value: '50K+', label: 'Active Developers' },
              { value: '2M+', label: 'Issues Detected' },
              { value: '99.2%', label: 'Accuracy Rate' },
              { value: '<1s', label: 'Analysis Time' },
            ].map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-2xl sm:text-3xl font-bold text-text-primary tracking-tight">
                  {stat.value}
                </div>
                <div className="text-xs sm:text-sm text-text-muted mt-1">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  )
}
