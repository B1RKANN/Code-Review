import React, { useRef } from 'react'
import { motion, useInView } from 'framer-motion'
import { Bot, Send, Wand2, Copy, ThumbsUp, User, ArrowRight } from 'lucide-react'

const chatMessages = [
  {
    role: 'user',
    content: 'Why is line 45 flagged as critical?',
  },
  {
    role: 'ai',
    content: `The \`except:\` on line 45 is a **bare except clause**. It catches every exception, including \`SystemExit\`, \`KeyboardInterrupt\`, and \`GeneratorExit\` — which are not programming errors and should propagate.\n\n**Auto-fix suggestion:**`,
    codeBlock: `# Before (line 45)\nexcept:\n    logger.error("Failed")\n\n# After (recommended)\nexcept Exception as e:\n    logger.error(f"Failed: {e}")`,
    actions: true,
  },
  {
    role: 'user',
    content: 'Apply the fix and also check for similar patterns in the codebase.',
  },
  {
    role: 'ai',
    content: '✅ Fix applied to `api.py:45`. I found **3 more** bare except clauses in your project:\n\n- `utils/parser.py:112`\n- `handlers/auth.py:67`\n- `workers/task_runner.py:23`\n\nWould you like me to apply the same fix to all of them?',
    actions: false,
  },
]

function ChatBubble({ msg, index }) {
  const isAI = msg.role === 'ai'
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.15 }}
      className={`flex gap-3 ${isAI ? '' : 'flex-row-reverse'}`}
    >
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
        isAI ? 'bg-gradient-to-br from-electric to-violet' : 'bg-surface border border-border'
      }`}>
        {isAI ? <Bot className="w-4 h-4 text-white" /> : <User className="w-4 h-4 text-text-secondary" />}
      </div>

      {/* Message */}
      <div className={`max-w-[85%] ${isAI ? '' : 'text-right'}`}>
        <div className={`rounded-2xl px-4 py-3 text-sm leading-relaxed ${
          isAI
            ? 'glass border border-border/40 text-text-primary rounded-tl-md'
            : 'bg-electric/15 border border-electric/20 text-text-primary rounded-tr-md'
        }`}>
          {msg.content.split('\n').map((line, i) => (
            <p key={i} className={i > 0 ? 'mt-2' : ''}>
              {line.split('**').map((seg, j) =>
                j % 2 === 1 ? <strong key={j} className="text-text-primary font-semibold">{seg}</strong> : seg
              )}
            </p>
          ))}
          {msg.codeBlock && (
            <pre className="mt-3 p-3 rounded-lg bg-midnight/80 border border-border/30 text-xs font-mono text-text-secondary overflow-x-auto">
              {msg.codeBlock}
            </pre>
          )}
        </div>
        {msg.actions && (
          <div className="flex items-center gap-2 mt-2">
            <button className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-electric bg-electric/10 border border-electric/20 rounded-lg hover:bg-electric/20 transition-colors">
              <Wand2 className="w-3 h-3" /> Apply Fix
            </button>
            <button className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-text-muted hover:text-text-secondary rounded-lg hover:bg-surface/50 transition-colors">
              <Copy className="w-3 h-3" /> Copy
            </button>
            <button className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-text-muted hover:text-text-secondary rounded-lg hover:bg-surface/50 transition-colors">
              <ThumbsUp className="w-3 h-3" />
            </button>
          </div>
        )}
      </div>
    </motion.div>
  )
}

export default function AIChatPeek() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-80px' })

  return (
    <section className="relative py-20 lg:py-32">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Left — Copy */}
          <motion.div
            ref={ref}
            initial={{ opacity: 0, x: -40 }}
            animate={isInView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.7 }}
          >
            <span className="inline-block px-3 py-1 mb-4 text-xs font-semibold uppercase tracking-wider text-amber bg-amber/10 rounded-full border border-amber/20">
              AI Assistant
            </span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-text-primary mb-6">
              Your AI Copilot for{' '}
              <span className="bg-gradient-to-r from-amber to-rose bg-clip-text text-transparent">
                Code Quality
              </span>
            </h2>
            <p className="text-lg text-text-secondary leading-relaxed mb-8">
              Ask CodeGuard AI why an issue was flagged, get instant auto-fix suggestions, and scan your entire codebase for similar patterns — all in a conversational interface built right into your workflow.
            </p>
            <div className="space-y-4">
              {[
                'Explains every detection with context and severity',
                'One-click auto-fix with diff preview',
                'Codebase-wide pattern scanning',
                'Learns from your coding style over time',
              ].map((item) => (
                <div key={item} className="flex items-start gap-3">
                  <div className="w-5 h-5 rounded-full bg-electric/15 flex items-center justify-center shrink-0 mt-0.5">
                    <ArrowRight className="w-3 h-3 text-electric" />
                  </div>
                  <span className="text-sm text-text-secondary">{item}</span>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Right — Chat mock */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            animate={isInView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.7, delay: 0.2 }}
          >
            <div className="glass rounded-2xl overflow-hidden glow-blue">
              {/* Chat header */}
              <div className="flex items-center gap-3 px-5 py-4 border-b border-border/40">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-electric to-violet flex items-center justify-center">
                  <Bot className="w-4 h-4 text-white" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-text-primary">CodeGuard AI</h4>
                  <span className="text-xs text-text-muted">claude-haiku • online</span>
                </div>
                <div className="ml-auto flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald animate-pulse" />
                  <span className="text-xs text-emerald font-medium">Active</span>
                </div>
              </div>

              {/* Messages */}
              <div className="p-5 space-y-5 max-h-[480px] overflow-y-auto">
                {chatMessages.map((msg, i) => (
                  <ChatBubble key={i} msg={msg} index={i} />
                ))}
              </div>

              {/* Input */}
              <div className="px-5 py-4 border-t border-border/40">
                <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-midnight-lighter border border-border/40">
                  <input
                    type="text"
                    placeholder="Ask about any detected issue..."
                    className="flex-1 bg-transparent text-sm text-text-primary placeholder-text-muted outline-none"
                    readOnly
                  />
                  <button className="w-8 h-8 rounded-lg bg-electric flex items-center justify-center hover:bg-electric-glow transition-colors">
                    <Send className="w-4 h-4 text-white" />
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
