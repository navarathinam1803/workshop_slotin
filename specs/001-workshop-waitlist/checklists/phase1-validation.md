# Phase 1 Validation Checklist — Workshop SlotIn (001-workshop-waitlist)

**Purpose**: Verify all Phase 1 (Setup) tasks are complete before proceeding to Phase 2.  
**Phase 1 scope**: T001, T002, T003, T004  
**Created**: 2026-03-01

---

## T001 — Directory structure

- [ ] **Backend** — `backend/` exists at repo root
- [ ] **Backend** — `backend/main.py` exists
- [ ] **Backend** — `backend/services.py` exists
- [ ] **Backend** — `backend/models.py` exists
- [ ] **Backend** — `backend/tests/` exists
- [ ] **Backend** — `backend/tests/test_services.py` exists
- [ ] **Frontend** — `frontend/` exists at repo root
- [ ] **Frontend** — `frontend/src/components/` exists
- [ ] **Frontend** — `frontend/src/pages/` exists
- [ ] **Frontend** — `frontend/src/services/` exists
- [ ] **Frontend** — `frontend/src/context/` exists

---

## T002 — Backend initialization

- [ ] **Backend** — `backend/requirements.txt` exists
- [ ] **Backend** — `requirements.txt` lists `fastapi`
- [ ] **Backend** — `requirements.txt` lists `uvicorn`
- [ ] **Backend** — `requirements.txt` lists `pydantic`
- [ ] **Backend** — Python 3.10+ can install deps: `pip install -r backend/requirements.txt` (optional run)

---

## T003 — Frontend initialization (Vite, React, Tailwind, Lucide)

- [ ] **Frontend** — `frontend/package.json` exists
- [ ] **Frontend** — `package.json` has `react`, `react-dom`
- [ ] **Frontend** — `package.json` has `vite`, `@vitejs/plugin-react`
- [ ] **Frontend** — `package.json` has `tailwindcss`, `postcss`, `autoprefixer`
- [ ] **Frontend** — `package.json` has `lucide-react`
- [ ] **Frontend** — `frontend/vite.config.js` exists
- [ ] **Frontend** — `frontend/index.html` exists and mounts `src/main.jsx`
- [ ] **Frontend** — `frontend/src/main.jsx` exists
- [ ] **Frontend** — `frontend/src/App.jsx` exists
- [ ] **Frontend** — `frontend/src/index.css` exists with Tailwind directives (`@tailwind base/components/utilities`)
- [ ] **Frontend** — `frontend/tailwind.config.js` exists
- [ ] **Frontend** — `frontend/postcss.config.js` exists
- [ ] **Frontend** — Dependencies installed: `frontend/node_modules/` present (or `npm install` in frontend succeeds)
- [ ] **Frontend** — Dev server runs: `cd frontend && npm run dev` (optional)

---

## T004 — Formatting and linting config

- [ ] **Backend** — `backend/pyproject.toml` exists (or `black`/`ruff` config elsewhere)
- [ ] **Backend** — `[tool.black]` section present in `pyproject.toml`
- [ ] **Backend** — `[tool.ruff]` section present in `pyproject.toml`
- [ ] **Frontend** — `frontend/.prettierrc` exists
- [ ] **Frontend** — `frontend/.prettierignore` exists (e.g. ignores `node_modules`, `dist`)

---

## tasks.md and Git

- [ ] **tasks.md** — T001 is marked complete: `- [x] T001 ...`
- [ ] **tasks.md** — T002 is marked complete: `- [x] T002 ...`
- [ ] **tasks.md** — T003 is marked complete: `- [x] T003 ...`
- [ ] **tasks.md** — T004 is marked complete: `- [x] T004 ...`
- [ ] **Git** — Four Phase 1 commits exist (one per task): `git log --oneline` shows T001, T002, T003, T004 messages
- [ ] **Git** — Branch `001-workshop-waitlist` is pushed to `origin` (optional): `git status` shows up to date with origin

---

## Constitution alignment (Phase 1)

- [ ] **No Redux** — No `redux` in frontend dependencies
- [ ] **Tailwind only** — Frontend uses Tailwind (no manual CSS files for layout)
- [ ] **React hooks** — `App.jsx` uses function component (no class component)
- [ ] **Backend stack** — FastAPI + Pydantic in backend; no external DB

---

## Sign-off

| Role        | Name | Date | Notes |
|------------|------|------|--------|
| Developer  |      |      |        |
| Reviewer   |      |      |        |

**Phase 1 complete when all checkboxes above are checked.** Proceed to Phase 2 (T005–T010) after sign-off.
