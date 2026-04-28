import React, { useRef } from 'react'
import { motion, useInView } from 'framer-motion'
import { Check, Zap, Building2, Rocket } from 'lucide-react'

const plans = [
  {
    name: 'Starter',
    price: 'Free',
    period: '',
    description: 'Perfect for individual developers exploring code quality.',
    icon: <Zap className="w-5 h-5" />,
    color: 'text-neon-cyan',
    iconBg: 'bg-neon-cyan/15',
    borderColor: 'border-neon-cyan/20',
    btnClass: 'border border-border hover:border-border-light text-text-primary hover:bg-surface/50',
    btnText: 'Get Started Free',
    features: [
      'Up to 3 projects',
      'Basic AST analysis',
      'SOLID compliance checks',
      '5 AI suggestions / day',
      'Community support',
    ],
  },
  {
    name: 'Pro',
    price: '$12',
    period: '/mo',
    description: 'For professional developers who demand the best.',
    icon: <Rocket className="w-5 h-5" />,
    color: 'text-electric',
    iconBg: 'bg-electric/15',
    borderColor: 'border-electric/30',
    popular: true,
    btnClass: 'bg-electric hover:bg-electric-glow text-white shadow-lg shadow-electric/25 hover:shadow-electric/40',
    btnText: 'Start Pro Trial',
    features: [
      'Unlimited projects',
      'Advanced AST + security audits',
      'Full SOLID analysis',
      'Unlimited AI suggestions',
      'Auto-fix engine',
      'LLM refactoring',
      'Priority support',
    ],
  },
  {
    name: 'Enterprise',
    price: '$49',
    period: '/mo',
    description: 'For teams that need scale, compliance, and control.',
    icon: <Building2 className="w-5 h-5" />,
    color: 'text-violet',
    iconBg: 'bg-violet/15',
    borderColor: 'border-violet/20',
    btnClass: 'border border-border hover:border-border-light text-text-primary hover:bg-surface/50',
    btnText: 'Contact Sales',
    features: [
      'Everything in Pro',
      'Team management dashboard',
      'Custom rule engine',
      'CI/CD pipeline integration',
      'SSO & SAML authentication',
      'SLA & dedicated support',
      'On-premise deployment',
    ],
  },
]

function PlanCard({ plan, index }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-60px' })

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay: index * 0.12 }}
      className="relative group"
    >
      {plan.popular && (
        <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 z-10">
          <span className="px-4 py-1 text-xs font-bold uppercase tracking-wider bg-electric text-white rounded-full shadow-lg shadow-electric/30">
            Most Popular
          </span>
        </div>
      )}
      <div
        className={`glass rounded-2xl p-8 h-full flex flex-col transition-all duration-500 border ${
          plan.popular
            ? 'border-electric/30 shadow-xl shadow-electric/5 scale-[1.02]'
            : 'border-border/40 hover:border-border-light'
        }`}
      >
        {/* Header */}
        <div className="mb-6">
          <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-4 ${plan.color} ${plan.iconBg}`}>
            {plan.icon}
          </div>
          <h3 className="text-xl font-bold text-text-primary mb-1">{plan.name}</h3>
          <p className="text-sm text-text-muted">{plan.description}</p>
        </div>

        {/* Price */}
        <div className="mb-6">
          <div className="flex items-baseline gap-1">
            <span className="text-4xl font-extrabold text-text-primary tracking-tight">{plan.price}</span>
            {plan.period && <span className="text-base text-text-muted font-medium">{plan.period}</span>}
          </div>
        </div>

        {/* Features */}
        <ul className="space-y-3 mb-8 flex-1">
          {plan.features.map((feature) => (
            <li key={feature} className="flex items-start gap-2.5">
              <div className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5 ${plan.color} ${plan.iconBg}`}>
                <Check className="w-3 h-3" />
              </div>
              <span className="text-sm text-text-secondary">{feature}</span>
            </li>
          ))}
        </ul>

        {/* CTA */}
        <button
          className={`w-full py-3 px-6 rounded-xl text-sm font-semibold transition-all duration-300 cursor-pointer ${plan.btnClass} ${
            plan.popular ? 'shimmer-btn' : ''
          }`}
        >
          {plan.btnText}
        </button>
      </div>
    </motion.div>
  )
}

export default function Pricing() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-80px' })

  return (
    <section id="pricing" className="relative py-20 lg:py-32">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        {/* Header */}
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 40 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7 }}
          className="text-center mb-16"
        >
          <span className="inline-block px-3 py-1 mb-4 text-xs font-semibold uppercase tracking-wider text-amber bg-amber/10 rounded-full border border-amber/20">
            Pricing
          </span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-text-primary">
            Simple, Transparent{' '}
            <span className="bg-gradient-to-r from-amber to-electric bg-clip-text text-transparent">
              Pricing
            </span>
          </h2>
          <p className="mt-4 text-lg text-text-secondary max-w-2xl mx-auto">
            Start free. Upgrade when you need more power. No hidden fees, cancel anytime.
          </p>
        </motion.div>

        {/* Plans Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 max-w-5xl mx-auto">
          {plans.map((plan, i) => (
            <PlanCard key={plan.name} plan={plan} index={i} />
          ))}
        </div>
      </div>
    </section>
  )
}
