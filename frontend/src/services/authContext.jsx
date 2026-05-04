import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { authService } from './api'

const AuthContext = createContext(null)

const TOKEN_KEY = 'codeguard_token'

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY))
  const [isLoading, setIsLoading] = useState(true)

  const isAuthenticated = !!user

  // Persist token
  const saveToken = useCallback((newToken) => {
    setToken(newToken)
    if (newToken) {
      localStorage.setItem(TOKEN_KEY, newToken)
    } else {
      localStorage.removeItem(TOKEN_KEY)
    }
  }, [])

  // Fetch user profile from token
  const fetchUser = useCallback(async (tkn) => {
    try {
      const userData = await authService.getMe(tkn)
      setUser(userData)
      return true
    } catch {
      // Token invalid or expired — clear it
      saveToken(null)
      setUser(null)
      return false
    }
  }, [saveToken])

  // On mount: restore session from stored token
  useEffect(() => {
    let cancelled = false
    async function restore() {
      if (token) {
        await fetchUser(token)
      }
      if (!cancelled) setIsLoading(false)
    }
    restore()
    return () => { cancelled = true }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  // ── Actions ──────────────────────────────────────

  const register = async (email, password, fullName) => {
    const data = await authService.register(email, password, fullName)
    saveToken(data.access_token)
    setUser(data.user)
    return data
  }

  const login = async (email, password) => {
    const data = await authService.login(email, password)
    saveToken(data.access_token)
    // Login response doesn't include user data, so fetch it
    await fetchUser(data.access_token)
    return data
  }

  const logout = () => {
    saveToken(null)
    setUser(null)
  }

  const value = {
    user,
    token,
    isAuthenticated,
    isLoading,
    register,
    login,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider')
  return ctx
}
