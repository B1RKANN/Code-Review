import React from 'react'
import { Shield, ExternalLink, MessageCircle, Mail } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="relative border-t border-border/30">
      <div className="max-w-7xl mx-auto px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10">
          {/* Brand */}
          <div className="md:col-span-1">
            <a href="#" className="flex items-center gap-2.5 mb-4">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-electric to-violet flex items-center justify-center">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <span className="text-lg font-bold tracking-tight text-text-primary">
                Code<span className="text-electric">Guard</span>
              </span>
            </a>
            <p className="text-sm text-text-muted leading-relaxed">
              AI-powered static analysis for modern development teams. Ship cleaner, safer code.
            </p>
            <div className="flex items-center gap-3 mt-5">
              {[ExternalLink, MessageCircle, Mail].map((Icon, i) => (
                <a key={i} href="#" className="w-9 h-9 rounded-lg flex items-center justify-center text-text-muted hover:text-text-primary hover:bg-surface/50 border border-transparent hover:border-border/50 transition-all duration-200">
                  <Icon className="w-4 h-4" />
                </a>
              ))}
            </div>
          </div>

          {/* Links */}
          {[
            { title: 'Product', links: ['Features', 'Pricing', 'Changelog', 'Download'] },
            { title: 'Resources', links: ['Documentation', 'API Reference', 'Blog', 'Community'] },
            { title: 'Company', links: ['About', 'Careers', 'Contact', 'Legal'] },
          ].map((col) => (
            <div key={col.title}>
              <h4 className="text-sm font-semibold text-text-primary mb-4">{col.title}</h4>
              <ul className="space-y-2.5">
                {col.links.map((link) => (
                  <li key={link}>
                    <a href="#" className="text-sm text-text-muted hover:text-text-secondary transition-colors duration-200">
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom bar */}
        <div className="mt-14 pt-6 border-t border-border/30 flex flex-col sm:flex-row items-center justify-between gap-4">
          <span className="text-xs text-text-muted">
            © {new Date().getFullYear()} CodeGuard. All rights reserved.
          </span>
          <div className="flex items-center gap-6">
            {['Privacy', 'Terms', 'Cookies'].map((link) => (
              <a key={link} href="#" className="text-xs text-text-muted hover:text-text-secondary transition-colors">
                {link}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  )
}
