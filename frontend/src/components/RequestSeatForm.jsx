import React, { useState } from 'react'
import { requestSeat } from '../services/api'

function formatDateTime(iso) {
  if (!iso) return '—'
  try {
    const d = new Date(iso)
    return d.toLocaleString(undefined, { dateStyle: 'short', timeStyle: 'short' })
  } catch {
    return iso
  }
}

export default function RequestSeatForm({ workshop, onClose }) {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!workshop?.id || !email.trim()) return
    setError(null)
    setResult(null)
    setLoading(true)
    try {
      const data = await requestSeat(workshop.id, email.trim())
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-slate-800">Request a seat</h3>
        {onClose && (
          <button
            type="button"
            onClick={onClose}
            className="text-slate-500 hover:text-slate-700"
            aria-label="Close"
          >
            ×
          </button>
        )}
      </div>
      {workshop && (
        <p className="mt-1 text-sm text-slate-600">
          {workshop.title} · {formatDateTime(workshop.date_time)}
        </p>
      )}
      <form onSubmit={handleSubmit} className="mt-4 space-y-3">
        <div>
          <label htmlFor="request-email" className="block text-sm font-medium text-slate-700">
            Your email
          </label>
          <input
            id="request-email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
            className="mt-1 w-full rounded border border-slate-300 px-3 py-2 text-slate-800"
          />
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        {result && (
          <div className="rounded bg-slate-100 p-3 text-sm">
            {result.state === 'confirmed' && (
              <p className="font-medium text-green-700">You have a confirmed seat.</p>
            )}
            {result.state === 'waitlisted' && (
              <p className="font-medium text-amber-700">
                You are on the waitlist (position {result.position ?? '—'}).
              </p>
            )}
            <p className="mt-1 text-slate-600">Booking ID: {result.booking_id}</p>
          </div>
        )}
        <div className="flex gap-2">
          <button
            type="submit"
            disabled={loading}
            className="rounded bg-slate-800 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700 disabled:opacity-50"
          >
            {loading ? 'Requesting…' : 'Request seat'}
          </button>
          {onClose && (
            <button type="button" onClick={onClose} className="rounded border border-slate-300 px-4 py-2 text-sm text-slate-700 hover:bg-slate-100">
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  )
}
