import React, { useRef } from 'react'
import { motion, useInView } from 'framer-motion'
import { TreePine, ShieldCheck, Zap, BrainCircuit, FileCode2, Lock, Gauge, Sparkles } from 'lucide-react'

const features = [
  {
    icon: <TreePine className="w-6 h-6" />,
    title: 'AST Static Analysis',
    description: 'Deep abstract syntax tree parsing that understands your code structure at the fundamental level — no guesswork.',
    color: 'text-electric',
    glowColor: 'rgba(59,130,246,0.15)',
    tag: 'Core Engine',
    span: 'col-span-1 lg:col-span-2',
  },
  {
    icon: <ShieldCheck className="w-6 h-6" />,
    title: 'SOLID Compliance',
    description: 'Automated detection of Single Responsibility, Open/Closed, Liskov, Interface Segregation, and Dependency Inversion violations.',
    color: 'text-emerald',
    glowColor: 'rgba(16,185,129,0.15)',
    tag: 'Architecture',
    span: 'col-span-1',
  },
  {
    icon: <Lock className="w-6 h-6" />,
    title: 'Security Audits',
    description: 'Continuous scanning for vulnerabilities: SQL injection, XSS, hardcoded secrets, insecure dependencies, and more.',
    color: 'text-rose',
    glowColor: 'rgba(244,63,94,0.15)',
    tag: 'Security',
    span: 'col-span-1',
  },
  {
    icon: <BrainCircuit className="w-6 h-6" />,
    title: 'LLM Refactoring',
    description: 'AI-powered code refactoring suggestions that understand intent, preserve behavior, and improve readability.',
    color: 'text-violet',
    glowColor: 'rgba(139,92,246,0.15)',
    tag: 'AI-Powered',
    span: 'col-span-1 lg:col-span-2',
  },
  {
    icon: <Gauge className="w-6 h-6" />,
    title: 'Performance Profiling',
    description: 'Detect blocking I/O, memory leaks, N+1 queries, and algorithmic bottlenecks before they hit production.',
    color: 'text-amber',
    glowColor: 'rgba(245,158,11,0.15)',
    tag: 'Performance',
    span: 'col-span-1',
  },
  {
    icon: <Sparkles className="w-6 h-6" />,
    title: 'Auto-Fix Engine',
    description: 'One-click remediation for detected issues — from code style to critical security patches, applied intelligently.',
    color: 'text-neon-cyan',
    glowColor: 'rgba(34,211,238,0.15)',
    tag: 'Automation',
    span: 'col-span-1',
  },
]

function FeatureCard({ feature, index }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-60px' })

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay: index * 0.08 }}
      className={`${feature.span} group`}
    >
      <div className="glass glass-hover glow-border rounded-2xl p-6 lg:p-8 h-full transition-all duration-500 cursor-default">
        {/* Tag */}
        <span className={`inline-block text-xs font-semibold uppercase tracking-wider ${feature.color} mb-4 opacity-70`}>
          {feature.tag}
        </span>

        {/* Icon */}
        <div
          className={`w-12 h-12 rounded-xl flex items-center justify-center mb-5 ${feature.color} transition-transform duration-300 group-hover:scale-110`}
          style={{ background: feature.glowColor }}
        >
          {feature.icon}
        </div>

        {/* Content */}
        <h3 className="text-xl font-bold text-text-primary mb-3 tracking-tight">{feature.title}</h3>
        <p className="text-sm text-text-secondary leading-relaxed">{feature.description}</p>
      </div>
    </motion.div>
  )
}

export default function FeatureGrid() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-80px' })

  return (
    <section id="features" className="relative py-20 lg:py-32">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        {/* Header */}
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 40 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7 }}
          className="text-center mb-16"
        >
          <span className="inline-block px-3 py-1 mb-4 text-xs font-semibold uppercase tracking-wider text-violet bg-violet/10 rounded-full border border-violet/20">
            Features
          </span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-text-primary">
            Everything You Need to{' '}
            <span className="bg-gradient-to-r from-electric to-neon-cyan bg-clip-text text-transparent">
              Ship with Confidence
            </span>
          </h2>
          <p className="mt-4 text-lg text-text-secondary max-w-2xl mx-auto">
            A comprehensive toolkit that goes beyond linting — understanding your code's architecture, security posture, and performance profile.
          </p>
        </motion.div>

        {/* Grid — Bento layout */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-5">
          {features.map((feature, i) => (
            <FeatureCard key={feature.title} feature={feature} index={i} />
          ))}
        </div>
      </div>
    </section>
  )
}
