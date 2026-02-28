import React, { useState } from 'react'
import { cancelBooking, getMyBookings } from '../services/api'

function formatDateTime(iso) {
  if (!iso) return '—'
  try {
    const d = new Date(iso)
    return d.toLocaleString(undefined, { dateStyle: 'short', timeStyle: 'short' })
  } catch {
    return iso
  }
}

export default function MyBookings() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [bookings, setBookings] = useState(null)
  const [cancellingId, setCancellingId] = useState(null)
  const [cancelMessage, setCancelMessage] = useState(null)

  async function handleLoad(e) {
    e.preventDefault()
    if (!email.trim()) return
    setError(null)
    setCancelMessage(null)
    setBookings(null)
    setLoading(true)
    try {
      const data = await getMyBookings(email.trim())
      setBookings(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleCancel(bookingId) {
    setError(null)
    setCancelMessage(null)
    setCancellingId(bookingId)
    try {
      const res = await cancelBooking(bookingId)
      const pct = res?.refund_percentage
      const msg =
        typeof pct === 'number' && pct > 0
          ? `Cancelled. Refund: ${pct}%.`
          : 'Cancelled. No refund (within 24h of start).'
      setCancelMessage(msg)
      if (email.trim()) {
        const data = await getMyBookings(email.trim())
        setBookings(data)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setCancellingId(null)
    }
  }

  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="font-semibold text-slate-800">My bookings</h3>
      <p className="mt-1 text-sm text-slate-600">Enter your email to see your workshops.</p>
      <form onSubmit={handleLoad} className="mt-4 flex flex-wrap items-end gap-2">
        <div>
          <label htmlFor="my-bookings-email" className="block text-sm font-medium text-slate-700">
            Email
          </label>
          <input
            id="my-bookings-email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-slate-800"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="rounded bg-slate-800 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700 disabled:opacity-50"
        >
          {loading ? 'Loading…' : 'Load my bookings'}
        </button>
      </form>
      {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
      {cancelMessage && (
        <p className="mt-3 text-sm font-medium text-green-700">{cancelMessage}</p>
      )}
      {bookings && (
        <ul className="mt-4 space-y-3">
          {bookings.length === 0 ? (
            <li className="text-sm text-slate-500">No bookings found for this email.</li>
          ) : (
            bookings.map((b) => (
              <li
                key={b.id}
                className="rounded border border-slate-100 bg-slate-50 p-3 text-sm"
              >
                <p className="font-medium text-slate-800">{b.workshop_title || 'Workshop'}</p>
                <p className="text-slate-600">{formatDateTime(b.workshop_date_time)}</p>
                <p className="mt-1">
                  <span className="font-medium text-slate-700">{b.state}</span>
                  {b.state === 'waitlisted' && typeof b.position === 'number' && (
                    <> · position {b.position}</>
                  )}
                </p>
                {(b.state === 'confirmed' || b.state === 'waitlisted') && (
                  <button
                    type="button"
                    onClick={() => handleCancel(b.id)}
                    disabled={cancellingId === b.id}
                    className="mt-2 rounded border border-red-300 bg-white px-2 py-1 text-xs font-medium text-red-700 hover:bg-red-50 disabled:opacity-50"
                  >
                    {cancellingId === b.id ? 'Cancelling…' : 'Cancel booking'}
                  </button>
                )}
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  )
}
