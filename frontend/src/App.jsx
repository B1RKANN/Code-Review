import React, { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import LivePreview from './components/LivePreview'
import FeatureGrid from './components/FeatureGrid'
import Pricing from './components/Pricing'
import AuthSection from './components/AuthSection'
import Footer from './components/Footer'
import Profile from './components/Profile'

export default function App() {
  const [currentRoute, setCurrentRoute] = useState(window.location.hash || '#home')
  const [isAuthenticated, setIsAuthenticated] = useState(localStorage.getItem('auth') === 'true')

  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash || '#home'
      if (hash === '#profile' && localStorage.getItem('auth') !== 'true') {
        window.location.hash = '#login'
        return
      }
      setCurrentRoute(hash)
    }
    handleHashChange()
    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  return (
    <div className="relative min-h-screen bg-midnight overflow-x-hidden">
      {/* Background ambient orbs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
        <div className="orb orb-blue" style={{ width: 800, height: 800, top: -200, right: -200 }} />
        <div className="orb orb-violet" style={{ width: 600, height: 600, top: 600, left: -150 }} />
        <div className="orb orb-cyan" style={{ width: 500, height: 500, top: 1800, right: 100 }} />
        <div className="orb orb-violet" style={{ width: 700, height: 700, top: 3200, left: -200 }} />
        <div className="orb orb-blue" style={{ width: 400, height: 400, top: 4500, right: -100 }} />
        <div className="orb orb-cyan" style={{ width: 500, height: 500, top: 5500, left: 100 }} />
      </div>

      <div className="relative z-10">
        <Navbar currentRoute={currentRoute} isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />
        {currentRoute === '#profile' ? (
          <Profile setIsAuthenticated={setIsAuthenticated} />
        ) : currentRoute === '#login' ? (
          <AuthSection setIsAuthenticated={setIsAuthenticated} />
        ) : (
          <>
            <Hero />
            <LivePreview />
            <FeatureGrid />
            <Pricing />
          </>
        )}
        <Footer />
      </div>
    </div>
  )
}
