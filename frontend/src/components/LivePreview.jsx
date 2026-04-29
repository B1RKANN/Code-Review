import React, { useRef } from 'react'
import { motion, useInView } from 'framer-motion'
import { Search, FileCode2, ArrowRight, Zap, ShieldAlert, Cpu, CheckCircle2, ChevronRight, ChevronDown, Paperclip, Send, Clock, GitBranch, FolderOpen } from 'lucide-react'

function ScoreDial({ score, maxScore, label, statusText, color = '#10B981' }) {
  const radius = 60
  const circumference = 2 * Math.PI * radius
  const pct = score / maxScore
  const offset = circumference * (1 - pct)
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-50px' })

  return (
    <div ref={ref} className="flex gap-8 items-center rounded-xl p-6 border border-border/20 bg-[#12151D]">
      <div className="relative">
        <svg width="140" height="140" viewBox="0 0 140 140">
          <circle cx="70" cy="70" r={radius} fill="none" stroke="rgba(42,48,64,0.3)" strokeWidth="8" />
          <circle cx="70" cy="70" r={radius} fill="none" stroke={color} strokeWidth="8" strokeLinecap="round"
            strokeDasharray={circumference} strokeDashoffset={isInView ? offset : circumference}
            transform="rotate(-90 70 70)"
            style={{ transition: 'stroke-dashoffset 1.5s cubic-bezier(.4,0,.2,1)' }} />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-5xl font-bold text-white">{score}</span>
          <span className="text-xs text-text-muted mt-1 uppercase">genel</span>
        </div>
      </div>

      <div className="flex-1">
        <div className="text-xs text-text-muted mb-3 uppercase tracking-widest font-semibold">GENEL SAĞLAMLIK SKORU</div>
        <div className="flex items-baseline gap-2 mb-4">
          <span className="text-4xl font-bold text-white">{score}</span>
          <span className="text-lg text-text-muted">/ 100</span>
        </div>
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-lg bg-amber-900/30 border border-amber-700/50 text-amber-500 text-sm font-medium">
          {statusText}
        </div>
      </div>

      <div className="flex flex-col items-end justify-center text-right border-l border-border/20 pl-8 h-full">
        <span className="text-xs text-text-muted mb-4">son 7 gün</span>
        <span className="text-emerald text-base font-bold flex items-center gap-1 mb-4">▲ +6</span>
        <span className="text-xs text-text-muted">3 bulgu</span>
      </div>
    </div>
  )
}

function SmallScoreDial({ score, color, label }) {
  const radius = 35
  const circumference = 2 * Math.PI * radius
  const pct = score / 100
  const offset = circumference * (1 - pct)
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-50px' })

  return (
    <div ref={ref} className="relative shrink-0">
      <svg width="80" height="80" viewBox="0 0 80 80">
        <circle cx="40" cy="40" r={radius} fill="none" stroke="rgba(42,48,64,0.3)" strokeWidth="6" />
        <circle cx="40" cy="40" r={radius} fill="none" stroke={color} strokeWidth="6" strokeLinecap="round"
          strokeDasharray={circumference} strokeDashoffset={isInView ? offset : circumference}
          transform="rotate(-90 40 40)"
          style={{ transition: 'stroke-dashoffset 1.5s cubic-bezier(.4,0,.2,1)' }} />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="text-2xl font-bold text-white">{score}</span>
        <span className="text-[9px] text-text-muted uppercase mt-0.5">{label}</span>
      </div>
    </div>
  )
}

function MetricCard({ title, score, desc, stats, icon, scoreLabel }) {
  return (
    <div className="rounded-xl p-5 border border-border/20 bg-[#12151D] flex items-center gap-5">
      <SmallScoreDial score={score} color="#10B981" label={scoreLabel} />
      <div className="flex-1">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-5 h-5 rounded-md bg-[#1A1D27] border border-border/40 flex items-center justify-center">
            {icon}
          </div>
          <span className="text-sm font-semibold text-text-primary">{title}</span>
        </div>
        <p className="text-xs text-text-muted leading-relaxed mb-3">{desc}</p>
        <div className="flex items-center gap-4 text-xs font-mono">
          {stats.map((stat, i) => (
            <div key={i} className="flex gap-1.5 items-center">
              <span className="text-text-primary">{stat.val}</span>
              <span className="text-text-muted">{stat.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function FileTreeItem({ name, score, colorClass, indent = 0, isFolder = false, isOpen = false, isActive = false }) {
  return (
    <div className={`flex items-center justify-between px-4 py-1.5 cursor-pointer text-sm font-medium ${isActive ? 'bg-[#3A5335] border-l-2 border-[#86C166] text-white' : 'hover:bg-[#1A1D27] text-text-secondary'}`} style={{ paddingLeft: `${16 + indent * 16}px` }}>
      <div className="flex items-center gap-2">
        {isFolder ? (
          isOpen ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />
        ) : (
          <div className="w-3.5 h-3.5" />
        )}
        {isFolder ? <FolderOpen className="w-4 h-4 text-amber-500/80" /> : <FileCode2 className="w-4 h-4 text-electric/80" />}
        <span>{name}</span>
      </div>
      {score && (
        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${colorClass} bg-opacity-10 bg-current`}>
          {score}
        </span>
      )}
    </div>
  )
}

export default function LivePreview() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-100px' })

  return (
    <section className="relative py-20 lg:py-32">
      <div className="max-w-[1400px] mx-auto px-4 lg:px-8">
        <motion.div ref={ref} initial={{ opacity: 0, y: 40 }} animate={isInView ? { opacity: 1, y: 0 } : {}} transition={{ duration: 0.7 }} className="text-center mb-16">
          <span className="inline-block px-3 py-1 mb-4 text-xs font-semibold uppercase tracking-wider text-neon-cyan bg-neon-cyan/10 rounded-full border border-neon-cyan/20">Live Dashboard & AI Assistant</span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-text-primary">Your Codebase, <span className="text-electric">Analyzed</span></h2>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 60 }} animate={isInView ? { opacity: 1, y: 0 } : {}} transition={{ duration: 1, delay: 0.2 }} className="relative rounded-xl overflow-hidden border border-[#2A3040] shadow-2xl shadow-black/80 bg-[#0F111A] font-sans flex flex-col h-[800px]">
          
          {/* Top Header Bar */}
          <div className="h-10 bg-[#0B0E14] border-b border-[#2A3040] flex items-center px-4 justify-between shrink-0 select-none">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-xs font-semibold text-text-primary">
                <ShieldAlert className="w-4 h-4 text-electric" /> CodeGuard
              </div>
              <div className="text-xs text-text-muted ml-2 font-medium">fastapi-payments / app / api / auth.py</div>
            </div>
            <div className="flex items-center gap-3">
              <div className="bg-[#1A1D27] border border-[#2A3040] rounded px-3 py-1 flex items-center gap-2 w-64 text-xs text-text-muted">
                <Search className="w-3.5 h-3.5" /> Ara... <span className="ml-auto opacity-50">Ctrl+K</span>
              </div>
              <div className="flex gap-4 text-text-muted">
                <div className="w-3 h-3 rounded-full bg-border/50" />
                <div className="w-3 h-3 rounded-full bg-border/50" />
                <div className="w-3 h-3 rounded-full bg-border/50" />
              </div>
            </div>
          </div>

          {/* Main IDE Area */}
          <div className="flex flex-1 overflow-hidden">
            
            {/* Left Sidebar - Explorer */}
            <div className="w-72 border-r border-[#2A3040] bg-[#0B0E14] flex flex-col shrink-0 select-none">
              <div className="mt-4 px-4 text-[10px] font-semibold text-text-muted uppercase tracking-wider flex items-center justify-between">
                WORKSPACE <span className="cursor-pointer text-lg leading-none">+</span>
              </div>
              <div className="mt-2 px-2">
                <div className="bg-[#1A1D27] border border-[#2A3040] rounded-lg p-2.5 flex items-center gap-3">
                  <div className="w-8 h-8 rounded border border-electric/30 flex items-center justify-center bg-electric/5">
                    <ShieldAlert className="w-4 h-4 text-electric" />
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-white">fastapi-payments</div>
                    <div className="text-[10px] text-text-muted">3.12.2 • poetry • 47 deps</div>
                  </div>
                </div>
              </div>

              <div className="mt-6 px-4 flex items-center justify-between text-[10px] font-semibold text-text-muted uppercase tracking-wider">
                FILES <Search className="w-3 h-3" />
              </div>
              
              {/* File Tree */}
              <div className="mt-2 flex-1 overflow-y-auto">
                <FileTreeItem name="app" isFolder isOpen indent={0} />
                <FileTreeItem name="api" isFolder isOpen indent={1} />
                <FileTreeItem name="__init__.py" score="98" colorClass="text-emerald-500" indent={2} />
                <FileTreeItem name="webhooks.py" score="62" colorClass="text-rose-500" indent={2} />
                <FileTreeItem name="payments.py" score="81" colorClass="text-amber-500" indent={2} />
                <FileTreeItem name="auth.py" score="74" colorClass="text-amber-500" indent={2} isActive />
                
                <FileTreeItem name="core" isFolder isOpen indent={1} />
                <FileTreeItem name="config.py" score="88" colorClass="text-amber-500" indent={2} />
                <FileTreeItem name="security.py" score="71" colorClass="text-amber-500" indent={2} />
                <FileTreeItem name="db.py" score="91" colorClass="text-emerald-500" indent={2} />
                
                <FileTreeItem name="models" isFolder isOpen indent={1} />
                <FileTreeItem name="user.py" score="94" colorClass="text-emerald-500" indent={2} />
                <FileTreeItem name="transaction.py" score="86" colorClass="text-amber-500" indent={2} />
                
                <FileTreeItem name="services" isFolder isOpen indent={1} />
                <FileTreeItem name="stripe_client.py" score="79" colorClass="text-amber-500" indent={2} />
                <FileTreeItem name="notifier.py" score="92" colorClass="text-emerald-500" indent={2} />
                
                <FileTreeItem name="main.py" score="95" colorClass="text-emerald-500" indent={1} />
                <FileTreeItem name="tests" isFolder indent={1} />
              </div>

              {/* Bottom Runtime Panel */}
              <div className="p-4 border-t border-[#2A3040] bg-[#12151D]">
                <div className="flex flex-col gap-1.5 text-xs font-mono text-text-muted">
                  <div className="flex gap-4"><span className="w-12">runtime</span><span className="text-text-primary flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-emerald-500" /> python 3.12.2</span></div>
                  <div className="flex gap-4"><span className="w-12">venv</span><span className="text-text-primary">.venv (active)</span></div>
                  <div className="flex gap-4"><span className="w-12">deps</span><span className="text-text-primary">poetry · 47 deps</span></div>
                </div>
              </div>
            </div>

            {/* Center Content - Dashboard */}
            <div className="flex-1 flex flex-col bg-[#0F111A] overflow-y-auto relative">
              <div className="sticky top-0 bg-[#0F111A] z-10 px-6 py-3 flex items-center justify-between border-b border-[#2A3040]">
                <div className="flex gap-2">
                  <button className="px-4 py-1.5 rounded bg-[#1A1D27] text-text-primary text-sm font-medium border border-[#2A3040] flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-electric" /> Skorlar
                  </button>
                  <button className="px-4 py-1.5 rounded text-text-muted text-sm font-medium hover:bg-[#1A1D27] flex items-center gap-2">
                    {'</>'} Kod
                  </button>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-[11px] text-text-muted flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" /> son tarama 2 dk önce
                  </span>
                  <button className="w-20 h-7 rounded border border-[#2A3040] bg-transparent" />
                </div>
              </div>

              <div className="p-8 max-w-4xl mx-auto w-full">
                <div className="mb-6 flex justify-between items-end">
                  <div>
                    <h1 className="text-2xl font-bold text-white tracking-tight">Kod Sağlamlık Raporu</h1>
                    <div className="text-[13px] text-text-muted mt-1">app/api/auth.py</div>
                  </div>
                  <div className="flex gap-2">
                    <div className="text-[11px] font-mono text-text-muted border border-[#2A3040] rounded-full px-4 py-1.5">scan • 2.4s</div>
                    <div className="text-[11px] font-mono text-text-muted border border-[#2A3040] rounded-full px-4 py-1.5">feat/webhook-retry</div>
                    <div className="text-[11px] font-mono text-text-muted border border-[#2A3040] rounded-full px-4 py-1.5">@e4f2c91</div>
                  </div>
                </div>

                <ScoreDial score={87} maxScore={100} statusText="Sağlıklı" />

                <div className="grid grid-cols-2 gap-4 mt-6">
                  <MetricCard 
                    title="Ağ Güvenliği" 
                    score={92} 
                    scoreLabel="secure"
                    desc="Bilinen CVE yok, secret sızıntısı tespit edilmedi." 
                    stats={[{ val: '0', label: 'Açık' }, { val: '12', label: 'Çözüldü' }]}
                    icon={<ShieldAlert className="w-3.5 h-3.5 text-text-muted" />} 
                  />
                  <MetricCard 
                    title="Temiz Kod" 
                    score={84} 
                    scoreLabel="clean"
                    desc="Tutarlı stil, düşük karmaşıklık. Birkaç uzun import bloğu." 
                    stats={[{ val: '4', label: 'Smell' }, { val: '0.8%', label: 'Duplicate' }]}
                    icon={<div className="w-3.5 h-3.5 flex items-center justify-center font-bold text-[10px]">+</div>} 
                  />
                  <MetricCard 
                    title="Performans / Bellek" 
                    score={88} 
                    scoreLabel="perf"
                    desc="Async pattern doğru kullanılıyor, bellek profili düz." 
                    stats={[{ val: '0', label: 'Hot path' }, { val: '31', label: 'Avg ms' }]}
                    icon={<Cpu className="w-3.5 h-3.5 text-text-muted" />} 
                  />
                  <MetricCard 
                    title="Genel Sağlamlık" 
                    score={85} 
                    scoreLabel="valid"
                    desc="Kapsamlı test paketi, anlamlı hata mesajları." 
                    stats={[{ val: '18', label: 'Try block' }, { val: '87%', label: 'Coverage' }]}
                    icon={<CheckCircle2 className="w-3.5 h-3.5 text-text-muted" />} 
                  />
                </div>

                <div className="mt-6 border-t border-[#2A3040] pt-4 flex justify-between items-center text-xs text-text-muted">
                  <span>Bulgular</span>
                  <span>3 aktif • 0 yüksek</span>
                </div>
              </div>
            </div>

            {/* Right Sidebar - AI Assistant */}
            <div className="w-[360px] border-l border-[#2A3040] bg-[#0B0E14] flex flex-col shrink-0">
              <div className="p-3 border-b border-[#2A3040] flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded bg-blue-600 flex items-center justify-center font-bold text-white text-xs">CG</div>
                  <div>
                    <div className="text-[13px] font-semibold text-white leading-tight">CodeGuard AI</div>
                    <div className="text-[10px] text-text-muted">python kalite uzmanı</div>
                  </div>
                </div>
                <div className="flex gap-3 text-text-muted">
                  <Clock className="w-4 h-4" />
                  <div className="w-4 h-4 flex items-center justify-center text-lg leading-none">+</div>
                </div>
              </div>
              
              <div className="flex-1 p-4 overflow-y-auto space-y-5">
                {/* AI Msg */}
                <div>
                  <div className="text-[10px] text-text-muted mb-1 flex items-center gap-1.5">CodeGuard AI • şimdi</div>
                  <div className="text-[13px] text-text-primary leading-relaxed bg-[#12151D] border border-[#2A3040] rounded-xl p-3">
                    En kritik konu: <span className="font-mono text-[11px] text-amber-500">app/api/webhooks.py</span> içinde imza doğrulaması atlanmış ve async fonksiyonda senkron HTTP çağrısı bulunuyor.
                  </div>
                  <div className="mt-2 flex flex-wrap gap-2">
                    <button className="px-3 py-1.5 rounded-lg bg-[#3A5335] border border-[#86C166] text-[#86C166] text-xs font-medium">Webhooks dosyasını aç</button>
                    <button className="px-3 py-1.5 rounded-lg bg-[#1A1D27] border border-[#2A3040] text-text-secondary text-xs font-medium">Tüm bulguları listele</button>
                    <button className="px-3 py-1.5 rounded-lg bg-[#1A1D27] border border-[#2A3040] text-text-secondary text-xs font-medium">Auto-fix önerileri</button>
                  </div>
                </div>

                {/* User Msg */}
                <div className="flex flex-col items-end">
                  <div className="text-[10px] text-text-muted mb-1">Sen • şimdi</div>
                  <div className="bg-[#2E4A28] border border-[#4F7346] text-white text-[13px] px-4 py-2 rounded-xl rounded-tr-sm">
                    Tüm bulguları listele
                  </div>
                </div>

                {/* User Msg */}
                <div className="flex flex-col items-end">
                  <div className="text-[10px] text-text-muted mb-1">Sen • şimdi</div>
                  <div className="bg-[#2E4A28] border border-[#4F7346] text-white text-[13px] px-4 py-2 rounded-xl rounded-tr-sm">
                    Auto-fix önerileri
                  </div>
                </div>

                {/* AI Msg 2 */}
                <div>
                  <div className="text-[10px] text-text-muted mb-1 flex items-center gap-1.5">CodeGuard AI • şimdi</div>
                  <div className="text-[13px] text-text-primary leading-relaxed bg-[#12151D] border border-[#2A3040] rounded-xl p-3">
                    <p className="mb-3">Anlıyorum. <span className="font-mono text-[11px] text-amber-500">app/api/auth.py</span> bağlamında bu konuya bakıyorum — analiz sonucu kısaca: dosya genel olarak iyi durumda, ancak 2-3 küçük iyileştirme alanı tespit ettim.</p>
                    <p>Hangi yöne odaklanmamı istersin: <span className="font-semibold text-white">güvenlik</span>, <span className="font-semibold text-white">performans</span>, yoksa <span className="font-semibold text-white">okunabilirlik</span>?</p>
                  </div>
                  <div className="mt-2 flex flex-wrap gap-2">
                    <button className="px-4 py-1.5 rounded-lg bg-[#1A1D27] border border-[#2A3040] text-text-secondary text-xs font-medium">Güvenlik</button>
                    <button className="px-4 py-1.5 rounded-lg bg-[#1A1D27] border border-[#2A3040] text-text-secondary text-xs font-medium">Performans</button>
                    <button className="px-4 py-1.5 rounded-lg bg-[#1A1D27] border border-[#2A3040] text-text-secondary text-xs font-medium">Okunabilirlik</button>
                  </div>
                </div>
              </div>

              {/* Chat Input Area */}
              <div className="p-4 border-t border-[#2A3040] bg-[#0B0E14] shrink-0">
                <div className="flex gap-2 overflow-x-hidden mb-3 whitespace-nowrap scrollbar-hide">
                  <span className="px-3 py-1.5 rounded-full border border-[#2A3040] text-[10px] text-text-muted bg-[#12151D] cursor-pointer hover:bg-[#1A1D27]">scan tüm projeyi</span>
                  <span className="px-3 py-1.5 rounded-full border border-[#2A3040] text-[10px] text-text-muted bg-[#12151D] cursor-pointer hover:bg-[#1A1D27]">lam webhooks.py</span>
                  <span className="px-3 py-1.5 rounded-full border border-[#2A3040] text-[10px] text-text-muted bg-[#12151D] cursor-pointer hover:bg-[#1A1D27]">sync refactor on</span>
                  <span className="px-3 py-1.5 rounded-full border border-[#2A3040] text-[10px] text-text-muted bg-[#12151D] cursor-pointer hover:bg-[#1A1D27]">verage'ı nasıl ar</span>
                </div>
                <div className="relative">
                  <Paperclip className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted -rotate-45 cursor-pointer hover:text-white" />
                  <input type="text" placeholder="auth.py hakkında soru sor..." className="w-full bg-[#12151D] border border-[#2A3040] rounded-xl py-3 pl-10 pr-12 text-[13px] text-text-primary focus:outline-none focus:border-electric/50" />
                  <button className="absolute right-1.5 top-1/2 -translate-y-1/2 w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center hover:bg-blue-500 transition-colors">
                    <Send className="w-4 h-4 text-white ml-0.5" />
                  </button>
                </div>
              </div>
            </div>

          </div>

          {/* Bottom Status Bar */}
          <div className="h-7 bg-[#0B0E14] border-t border-[#2A3040] flex items-center px-4 justify-between text-[11px] text-text-muted font-mono shrink-0 select-none">
            <div className="flex items-center gap-4">
              <span className="flex items-center gap-1.5 hover:text-text-primary cursor-pointer"><ArrowRight className="w-3.5 h-3.5" /> feat/webhook-retry <span className="opacity-50">@e4f2c91</span></span>
              <span className="hover:text-text-primary cursor-pointer text-emerald-500">✓ venv aktif</span>
              <span>python 3.12.2</span>
            </div>
            <div className="flex items-center gap-5">
              <span>auth.py</span>
              <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-emerald-500" /> skor 87</span>
              <span>CodeGuard 1.2.0</span>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
