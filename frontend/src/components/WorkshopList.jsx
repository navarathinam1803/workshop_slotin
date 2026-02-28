import React from 'react'

function formatDateTime(iso) {
  if (!iso) return '—'
  try {
    const d = new Date(iso)
    return d.toLocaleString(undefined, { dateStyle: 'short', timeStyle: 'short' })
  } catch {
    return iso
  }
}

export default function WorkshopList({ workshops = [] }) {
  return (
    <ul className="space-y-4">
      {workshops.map((ws) => (
        <li
          key={ws.id}
          className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
        >
          <h3 className="font-semibold text-slate-800">{ws.title}</h3>
          <p className="mt-1 text-sm text-slate-600">
            {formatDateTime(ws.date_time)}
          </p>
          <p className="mt-2 text-sm text-slate-500">
            Capacity: {ws.confirmed_count ?? 0} / {ws.capacity} confirmed
            {typeof ws.waitlisted_count === 'number' && (
              <> · {ws.waitlisted_count} waitlisted</>
            )}
          </p>
        </li>
      ))}
    </ul>
  )
}
