import React, { createContext, useContext, useState, useCallback, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircle, AlertTriangle, XCircle, X, Info } from 'lucide-react'

/* ─── Context ──────────────────────────────────────── */
const ToastContext = createContext(null)

const ICON_MAP = {
  success: CheckCircle,
  error: XCircle,
  warning: AlertTriangle,
  info: Info,
}

const STYLE_MAP = {
  success: {
    border: 'border-emerald/30',
    icon: 'text-emerald',
    bg: 'bg-emerald/10',
    glow: 'shadow-emerald/10',
  },
  error: {
    border: 'border-rose/30',
    icon: 'text-rose',
    bg: 'bg-rose/10',
    glow: 'shadow-rose/10',
  },
  warning: {
    border: 'border-amber/30',
    icon: 'text-amber',
    bg: 'bg-amber/10',
    glow: 'shadow-amber/10',
  },
  info: {
    border: 'border-electric/30',
    icon: 'text-electric',
    bg: 'bg-electric/10',
    glow: 'shadow-electric/10',
  },
}

let toastId = 0

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])
  const timersRef = useRef({})

  const removeToast = useCallback((id) => {
    clearTimeout(timersRef.current[id])
    delete timersRef.current[id]
    setToasts((prev) => prev.filter((t) => t.id !== id))
  }, [])

  const addToast = useCallback((message, type = 'info', duration = 4000) => {
    const id = ++toastId
    setToasts((prev) => [...prev, { id, message, type }])
    timersRef.current[id] = setTimeout(() => removeToast(id), duration)
    return id
  }, [removeToast])

  const toast = {
    success: (msg, dur) => addToast(msg, 'success', dur),
    error: (msg, dur) => addToast(msg, 'error', dur),
    warning: (msg, dur) => addToast(msg, 'warning', dur),
    info: (msg, dur) => addToast(msg, 'info', dur),
  }

  return (
    <ToastContext.Provider value={toast}>
      {children}

      {/* Toast Container */}
      <div className="fixed top-5 right-5 z-[9999] flex flex-col gap-3 pointer-events-none max-w-sm w-full">
        <AnimatePresence>
          {toasts.map((t) => {
            const Icon = ICON_MAP[t.type]
            const style = STYLE_MAP[t.type]
            return (
              <motion.div
                key={t.id}
                initial={{ opacity: 0, x: 60, scale: 0.95 }}
                animate={{ opacity: 1, x: 0, scale: 1 }}
                exit={{ opacity: 0, x: 60, scale: 0.95 }}
                transition={{ duration: 0.3, ease: 'easeOut' }}
                className={`pointer-events-auto flex items-start gap-3 px-4 py-3.5 rounded-xl glass border ${style.border} shadow-lg ${style.glow}`}
              >
                <div className={`p-1 rounded-lg ${style.bg} shrink-0 mt-0.5`}>
                  <Icon className={`w-4 h-4 ${style.icon}`} />
                </div>
                <p className="text-sm text-text-primary leading-snug flex-1">{t.message}</p>
                <button
                  onClick={() => removeToast(t.id)}
                  className="text-text-muted hover:text-text-secondary transition-colors shrink-0 mt-0.5 cursor-pointer"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </motion.div>
            )
          })}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error('useToast must be used within a ToastProvider')
  return ctx
}
