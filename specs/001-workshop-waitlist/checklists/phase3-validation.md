# Phase 3 Validation Checklist — Workshop SlotIn (001-workshop-waitlist)

**Purpose**: Verify Phase 3 (User Story 1 — Browse Workshops) is complete before proceeding to Phase 4.  
**Phase 3 scope**: T011, T012, T013, T014  
**Created**: 2026-03-01

---

## T011 — GET /workshops (backend)

- [ ] **Backend** — `backend/main.py` defines `GET /workshops` route (or `/api/workshops`)
- [ ] **Backend** — Route uses `load_workshops()` from services
- [ ] **Backend** — For each workshop, `confirmed_count` and `waitlisted_count` are derived from bookings (via `get_bookings_by_workshop` or equivalent)
- [ ] **Backend** — Response is a JSON array of objects with: `id`, `title`, `date_time`, `capacity`, `confirmed_count`, `waitlisted_count`
- [ ] **Backend** — `confirmed_count` ≤ `capacity` for each returned workshop (invariant)
- [ ] **Manual** — With backend running, `curl http://localhost:8000/workshops` returns 200 and valid JSON array (optional)

---

## T012 — Frontend API client getWorkshops()

- [ ] **Frontend** — `frontend/src/services/api.js` exists (or .ts)
- [ ] **Frontend** — API base URL is configurable (e.g. `VITE_API_URL` or default `http://localhost:8000`)
- [ ] **Frontend** — `getWorkshops()` function is exported
- [ ] **Frontend** — `getWorkshops()` fetches `GET ${API_BASE}/workshops` and returns parsed JSON (or throws on error)
- [ ] **Constitution** — No direct call to external 3rd party API; only backend URL

---

## T013 — WorkshopList component

- [ ] **Frontend** — `frontend/src/components/WorkshopList.jsx` exists (or .tsx)
- [ ] **Frontend** — Component accepts `workshops` prop (array)
- [ ] **Frontend** — Renders workshop `title`
- [ ] **Frontend** — Renders `date_time` (formatted for display, e.g. locale string)
- [ ] **Frontend** — Renders `capacity`
- [ ] **Frontend** — Renders `confirmed_count` and `waitlisted_count`
- [ ] **Frontend** — Uses Tailwind utility classes only (no manual CSS for layout)
- [ ] **Frontend** — Function component (hooks); no class component

---

## T014 — Home page wired to workshop list

- [ ] **Frontend** — `frontend/src/App.jsx` (or pages/Home.jsx) imports `getWorkshops` and `WorkshopList`
- [ ] **Frontend** — On mount, fetches workshops (e.g. `useEffect` calling `getWorkshops()`)
- [ ] **Frontend** — State holds workshop list (e.g. `useState` for workshops)
- [ ] **Frontend** — Displays loading state while fetching
- [ ] **Frontend** — Displays error state if fetch fails
- [ ] **Frontend** — Renders `WorkshopList` with fetched workshops when loaded successfully
- [ ] **Manual** — With backend and frontend running, home page shows at least one workshop with correct counts (optional)

---

## tasks.md and Git

- [ ] **tasks.md** — T011 through T014 are marked complete: `- [x] T011 ...` … `- [x] T014 ...`
- [ ] **Git** — Four Phase 3 commits exist (one per task): T011, T012, T013, T014 in `git log --oneline`
- [ ] **Git** — Branch `001-workshop-waitlist` pushed to `origin` (optional)

---

## User Story 1 — Independent test (MVP)

- [ ] **E2E** — Load app in browser → workshop list displays
- [ ] **E2E** — Each workshop shows title, date/time, capacity, confirmed count, waitlisted count
- [ ] **E2E** — Confirmed count never exceeds capacity (data invariant visible in UI)

---

## Sign-off

| Role        | Name | Date | Notes |
|------------|------|------|--------|
| Developer  |      |      |        |
| Reviewer   |      |      |        |

**Phase 3 complete when all checkboxes above are checked.** Proceed to Phase 4 (T015–T020) after sign-off.
