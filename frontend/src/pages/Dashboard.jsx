import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import {
  FileCode2, Shield, AlertTriangle, ArrowLeft,
  Clock, ChevronRight, BarChart3, Upload, Loader2, FileWarning
} from 'lucide-react'
import { useAuth } from '../services/authContext'
import { analyzeService } from '../services/api'
import { useToast } from '../components/Toast'

const SEV_BADGE = {
  High: { bg: 'bg-rose/10', text: 'text-rose', border: 'border-rose/20' },
  Medium: { bg: 'bg-amber/10', text: 'text-amber', border: 'border-amber/20' },
  Low: { bg: 'bg-neon-cyan/10', text: 'text-neon-cyan', border: 'border-neon-cyan/20' },
}

export default function Dashboard() {
  const { user, token, logout } = useAuth()
  const toast = useToast()
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [selectedReport, setSelectedReport] = useState(null)

  useEffect(() => {
    fetchReports()
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const fetchReports = async () => {
    try {
      setLoading(true)
      const data = await analyzeService.getReports(token)
      setReports(data)
    } catch (err) {
      if (err.status === 401) {
        toast.error('Oturum süresi doldu. Lütfen tekrar giriş yapın.')
        logout()
        return
      }
      toast.error('Raporlar yüklenirken hata oluştu')
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    try {
      await analyzeService.uploadFile(file, token)
      toast.success(`${file.name} başarıyla analiz edildi!`)
      await fetchReports()
    } catch (err) {
      toast.error(err.message || 'Dosya analizi başarısız oldu')
    } finally {
      setUploading(false)
      e.target.value = ''
    }
  }

  const getIssueCount = (report) => {
    return report.report_data?.total_issues || report.report_data?.issues?.length || 0
  }

  const getHighestSeverity = (report) => {
    const issues = report.report_data?.issues || []
    if (issues.some((i) => i.severity === 'High')) return 'High'
    if (issues.some((i) => i.severity === 'Medium')) return 'Medium'
    return 'Low'
  }

  const formatDate = (dateStr) => {
    const d = new Date(dateStr)
    return d.toLocaleDateString('tr-TR', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  return (
    <div className="min-h-screen bg-midnight relative overflow-x-hidden">
      {/* Background orbs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
        <div className="orb orb-blue" style={{ width: 600, height: 600, top: -150, right: -150 }} />
        <div className="orb orb-violet" style={{ width: 500, height: 500, top: 400, left: -100 }} />
      </div>

      <div className="relative z-10 max-w-6xl mx-auto px-6 lg:px-8 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8"
        >
          <div>
            <a
              href="/"
              className="inline-flex items-center gap-1.5 text-xs text-text-muted hover:text-text-secondary transition-colors mb-3"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              Ana Sayfa
            </a>
            <h1 className="text-2xl sm:text-3xl font-bold text-text-primary">
              Hoş Geldin, <span className="text-electric">{user?.full_name?.split(' ')[0] || 'Kullanıcı'}</span>
            </h1>
            <p className="text-text-secondary text-sm mt-1">Analiz raporlarını buradan görüntüleyebilirsin.</p>
          </div>

          {/* Upload Button */}
          <label
            className={`shimmer-btn inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold bg-electric hover:bg-electric-glow text-white shadow-lg shadow-electric/25 hover:shadow-electric/40 transition-all duration-300 cursor-pointer ${
              uploading ? 'opacity-60 pointer-events-none' : ''
            }`}
          >
            {uploading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Analiz ediliyor...
              </>
            ) : (
              <>
                <Upload className="w-4 h-4" />
                Dosya Yükle
              </>
            )}
            <input
              type="file"
              className="hidden"
              onChange={handleFileUpload}
              accept=".py,.js,.ts,.jsx,.tsx,.java,.cpp,.c,.go,.rs,.rb,.php,.cs"
              disabled={uploading}
            />
          </label>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8"
        >
          {[
            {
              label: 'Toplam Rapor',
              value: reports.length,
              icon: BarChart3,
              color: 'text-electric',
              bg: 'bg-electric/10',
            },
            {
              label: 'Toplam Sorun',
              value: reports.reduce((sum, r) => sum + getIssueCount(r), 0),
              icon: AlertTriangle,
              color: 'text-amber',
              bg: 'bg-amber/10',
            },
            {
              label: 'Analiz Edilen Dosya',
              value: new Set(reports.map((r) => r.file_name)).size,
              icon: FileCode2,
              color: 'text-emerald',
              bg: 'bg-emerald/10',
            },
          ].map((stat) => (
            <div key={stat.label} className="glass rounded-xl p-5 flex items-center gap-4">
              <div className={`p-2.5 rounded-lg ${stat.bg}`}>
                <stat.icon className={`w-5 h-5 ${stat.color}`} />
              </div>
              <div>
                <p className="text-2xl font-bold text-text-primary">{stat.value}</p>
                <p className="text-xs text-text-muted">{stat.label}</p>
              </div>
            </div>
          ))}
        </motion.div>

        {/* Reports List */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h2 className="text-lg font-semibold text-text-primary mb-4 flex items-center gap-2">
            <FileCode2 className="w-5 h-5 text-electric" />
            Analiz Raporları
          </h2>

          {loading ? (
            <div className="glass rounded-xl p-12 flex flex-col items-center gap-3">
              <Loader2 className="w-8 h-8 text-electric animate-spin" />
              <p className="text-sm text-text-muted">Raporlar yükleniyor...</p>
            </div>
          ) : reports.length === 0 ? (
            <div className="glass rounded-xl p-12 flex flex-col items-center gap-3 text-center">
              <FileWarning className="w-12 h-12 text-text-muted" />
              <p className="text-text-secondary font-medium">Henüz rapor yok</p>
              <p className="text-sm text-text-muted max-w-sm">
                Yukarıdaki "Dosya Yükle" butonunu kullanarak ilk analiz raporunuzu oluşturun.
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {reports.map((report, idx) => {
                const sev = getHighestSeverity(report)
                const sevStyle = SEV_BADGE[sev]
                const issueCount = getIssueCount(report)
                const isExpanded = selectedReport === report.id

                return (
                  <motion.div
                    key={report.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: idx * 0.05 }}
                    className="glass rounded-xl overflow-hidden hover:border-electric/20 transition-colors duration-300 cursor-pointer"
                    onClick={() => setSelectedReport(isExpanded ? null : report.id)}
                  >
                    <div className="px-5 py-4 flex items-center gap-4">
                      <div className="p-2 rounded-lg bg-surface shrink-0">
                        <FileCode2 className="w-4.5 h-4.5 text-electric" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-text-primary truncate">{report.file_name}</p>
                        <div className="flex items-center gap-3 mt-1">
                          <span className="flex items-center gap-1 text-xs text-text-muted">
                            <Clock className="w-3 h-3" />
                            {formatDate(report.created_at)}
                          </span>
                          <span
                            className={`inline-flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-full border ${sevStyle.bg} ${sevStyle.text} ${sevStyle.border}`}
                          >
                            {issueCount} sorun
                          </span>
                        </div>
                      </div>
                      <ChevronRight
                        className={`w-4 h-4 text-text-muted transition-transform duration-200 ${
                          isExpanded ? 'rotate-90' : ''
                        }`}
                      />
                    </div>

                    {/* Expanded Detail */}
                    {isExpanded && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        transition={{ duration: 0.25 }}
                        className="border-t border-border/30 px-5 py-4"
                      >
                        {report.report_data?.issues?.length > 0 ? (
                          <div className="space-y-2.5">
                            {report.report_data.issues.slice(0, 5).map((issue, i) => {
                              const isev = SEV_BADGE[issue.severity] || SEV_BADGE.Low
                              return (
                                <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-midnight-lighter/50">
                                  <span
                                    className={`inline-flex items-center text-[10px] font-bold px-1.5 py-0.5 rounded border ${isev.bg} ${isev.text} ${isev.border} shrink-0 mt-0.5`}
                                  >
                                    {issue.severity}
                                  </span>
                                  <div className="min-w-0">
                                    <p className="text-xs text-text-primary leading-snug">{issue.message}</p>
                                    {issue.suggestion && (
                                      <p className="text-[11px] text-text-muted mt-1">💡 {issue.suggestion}</p>
                                    )}
                                  </div>
                                </div>
                              )
                            })}
                            {report.report_data.issues.length > 5 && (
                              <p className="text-xs text-text-muted text-center py-1">
                                +{report.report_data.issues.length - 5} daha fazla sorun
                              </p>
                            )}
                          </div>
                        ) : (
                          <p className="text-sm text-emerald flex items-center gap-2">
                            <Shield className="w-4 h-4" />
                            Herhangi bir sorun tespit edilmedi!
                          </p>
                        )}

                        {report.llm_suggestions && (
                          <div className="mt-4 p-3 rounded-lg bg-midnight-lighter/50 border border-border/20">
                            <p className="text-[11px] font-medium text-text-muted uppercase tracking-wider mb-2">
                              AI Önerileri
                            </p>
                            <p className="text-xs text-text-secondary leading-relaxed whitespace-pre-wrap">
                              {report.llm_suggestions.slice(0, 400)}
                              {report.llm_suggestions.length > 400 && '...'}
                            </p>
                          </div>
                        )}
                      </motion.div>
                    )}
                  </motion.div>
                )
              })}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}
