# Backend QA Checklist (TaskFlow API)

Use this checklist to validate the backend repository before submission/deployment.

## Environment & startup

- [x] Python version is `3.12.8` recommended (or compatible `3.11+`)
- [x] Virtualenv created and activated
- [x] `pip install -r requirements.txt` succeeds
- [x] `.env` created from `.env.example`
- [x] `python manage.py migrate` succeeds
- [x] `python manage.py runserver` starts API on `http://127.0.0.1:8000`
- [x] Swagger docs available at `/api/docs/`

## Auth & user isolation

- [x] `/api/auth/login/` returns access + refresh tokens for demo user
- [x] Protected endpoints reject unauthenticated requests
- [x] Data is user-scoped (no cross-user task/image/annotation leakage)

## Tasks API

- [x] `GET /api/tasks/?due_date=YYYY-MM-DD` filters by date
- [x] `POST /api/tasks/` creates a task with expected defaults/order
- [x] `PATCH /api/tasks/{id}/` updates fields correctly
- [x] `DELETE /api/tasks/{id}/` deletes task
- [x] `PATCH /api/tasks/reorder/` updates status/order atomically
- [x] `GET /api/tags/` returns available tags

## Annotation API

- [x] `POST /api/images/` accepts image + patient/test identifiers
- [x] Uploaded image stores width/height and original name
- [x] `GET /api/images/` returns only current user images
- [x] `GET /api/images/{id}/annotations/` lists current image polygons
- [x] `POST /api/images/{id}/annotations/` validates normalized points `[0,1]`
- [x] `DELETE /api/annotations/{id}/` deletes one polygon
- [x] `DELETE /api/images/{id}/annotations/clear/` clears only that image

## Series-scoped behavior

- [x] `GET/PATCH /api/series-review/?patient_id=&patient_code=&test_code=` is isolated per series key
- [x] `DELETE /api/series-annotations/clear/?patient_id=&patient_code=&test_code=` clears only that series
- [x] Clearing one series does not affect other series annotations
- [x] Series review records are unique per `(user, patient_id, patient_code, test_code)`

## Settings & security checks

- [x] `SECRET_KEY` not hard-coded for production
- [x] `DEBUG=False` works in production mode
- [x] `ALLOWED_HOSTS` includes Render hostname in production
- [x] `CORS_ALLOWED_ORIGINS` configured for frontend domain
- [x] `CSRF_TRUSTED_ORIGINS` configured for backend/frontend domains
- [x] Static files collect with WhiteNoise enabled in production mode
- [x] `python manage.py check` passes without issues

## Build/deploy checks (Render)

- [x] `build.sh` runs: install deps, collectstatic, migrate, seed demo user
- [x] `render.yaml` defines database + web service
- [x] Start command uses ASGI + Gunicorn/Uvicorn worker
- [x] Required env vars present on Render: `DATABASE_URL`, `SECRET_KEY`, `DEBUG`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`

## Regression quick script (recommended)

- [x] Login, create task, reorder task
- [x] Upload image, create polygon, delete polygon
- [x] Save series review for two distinct series and verify isolation
- [x] Clear one series and verify other series still intact

