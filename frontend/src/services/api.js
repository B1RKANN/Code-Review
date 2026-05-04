const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_V1 = `${API_URL}/api/v1`

/**
 * Wrapper around fetch that automatically adds JSON headers
 * and Bearer token if provided.
 */
async function request(endpoint, { method = 'GET', body, token } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const config = { method, headers }
  if (body) config.body = JSON.stringify(body)

  const res = await fetch(`${API_V1}${endpoint}`, config)
  const data = await res.json()

  if (!res.ok) {
    // Backend returns { detail: "..." } for errors
    const message = data.detail || 'Bir hata oluştu'
    const error = new Error(message)
    error.status = res.status
    throw error
  }

  return data
}

/* ────────────────────────────────────────
   Auth Service
   ──────────────────────────────────────── */

export const authService = {
  /**
   * Register a new user
   * @returns {{ user, access_token, token_type }}
   */
  register: (email, password, full_name) =>
    request('/auth/register', {
      method: 'POST',
      body: { email, password, full_name: full_name || undefined },
    }),

  /**
   * Login with email + password
   * @returns {{ access_token, token_type }}
   */
  login: (email, password) =>
    request('/auth/login', {
      method: 'POST',
      body: { email, password },
    }),

  /**
   * Get the current user profile
   * @returns {{ id, email, full_name, is_active }}
   */
  getMe: (token) =>
    request('/auth/me', { token }),
}

/* ────────────────────────────────────────
   Analyze Service
   ──────────────────────────────────────── */

export const analyzeService = {
  /**
   * Get all reports for the current user
   */
  getReports: (token) =>
    request('/analyze/reports', { token }),

  /**
   * Upload a file for analysis (uses FormData, not JSON)
   */
  uploadFile: async (file, token) => {
    const formData = new FormData()
    formData.append('file', file)

    const res = await fetch(`${API_V1}/analyze/upload`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    })

    const data = await res.json()
    if (!res.ok) {
      const message = data.detail || 'Dosya analizi başarısız oldu'
      const error = new Error(message)
      error.status = res.status
      throw error
    }
    return data
  },
}
