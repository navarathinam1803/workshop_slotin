import React, { useEffect, useState } from 'react'
import WorkshopList from './components/WorkshopList'
import { getWorkshops } from './services/api'

function App() {
  const [workshops, setWorkshops] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getWorkshops()
      .then(setWorkshops)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <h1 className="text-2xl font-semibold text-slate-800">Workshop SlotIn</h1>
      <p className="mt-2 text-slate-600">Browse workshops and see availability.</p>

      {loading && <p className="mt-4 text-slate-500">Loading workshops…</p>}
      {error && (
        <p className="mt-4 text-red-600">Failed to load workshops: {error}</p>
      )}
      {!loading && !error && (
        <div className="mt-6">
          <WorkshopList workshops={workshops} />
        </div>
      )}
    </div>
  )
}

export default App
