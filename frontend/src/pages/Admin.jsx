import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getAdminBookings, noShowBooking } from '../services/api'

function formatDateTime(iso) {
  if (!iso) return '—'
  try {
    const d = new Date(iso)
    return d.toLocaleString(undefined, { dateStyle: 'short', timeStyle: 'short' })
  } catch {
    return iso
  }
}

export default function Admin() {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [markingId, setMarkingId] = useState(null)

  function loadBookings() {
    setLoading(true)
    setError(null)
    getAdminBookings()
      .then(setBookings)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadBookings()
  }, [])

  async function handleNoShow(bookingId) {
    setError(null)
    setMarkingId(bookingId)
    try {
      await noShowBooking(bookingId)
      loadBookings()
    } catch (err) {
      setError(err.message)
    } finally {
      setMarkingId(null)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="mb-4 flex items-center gap-4">
        <Link to="/" className="text-slate-600 hover:text-slate-800">
          ← Workshop SlotIn
        </Link>
      </div>
      <h1 className="text-2xl font-semibold text-slate-800">Admin — No-show</h1>
      <p className="mt-2 text-slate-600">Mark confirmed participants as no-show. No seat freed; no waitlist promotion.</p>

      {loading && <p className="mt-4 text-slate-500">Loading confirmed bookings…</p>}
      {error && <p className="mt-4 text-red-600">{error}</p>}
      {!loading && !error && (
        <div className="mt-6">
          {bookings.length === 0 ? (
            <p className="text-slate-500">No confirmed bookings.</p>
          ) : (
            <ul className="space-y-3">
              {bookings.map((b) => (
                <li
                  key={b.id}
                  className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-slate-200 bg-white p-4"
                >
                  <div>
                    <p className="font-medium text-slate-800">{b.workshop_title || 'Workshop'}</p>
                    <p className="text-sm text-slate-600">{formatDateTime(b.workshop_date_time)}</p>
                    <p className="mt-1 text-sm text-slate-700">{b.email}</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleNoShow(b.id)}
                    disabled={markingId === b.id}
                    className="rounded border border-amber-300 bg-white px-3 py-1.5 text-sm font-medium text-amber-800 hover:bg-amber-50 disabled:opacity-50"
                  >
                    {markingId === b.id ? 'Marking…' : 'Mark no-show'}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  )
}
