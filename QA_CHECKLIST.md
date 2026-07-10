# Backend QA Checklist (TaskFlow API)

Use this checklist to validate the backend repository before submission/deployment.

## Environment & startup

- [ ] Python version is `3.12.8` recommended (or compatible `3.11+`)
- [ ] Virtualenv created and activated
- [ ] `pip install -r requirements.txt` succeeds
- [ ] `.env` created from `.env.example`
- [ ] `python manage.py migrate` succeeds
- [ ] `python manage.py runserver` starts API on `http://127.0.0.1:8000`
- [ ] Swagger docs available at `/api/docs/`

## Auth & user isolation

- [ ] `/api/auth/login/` returns access + refresh tokens for demo user
- [ ] Protected endpoints reject unauthenticated requests
- [ ] Data is user-scoped (no cross-user task/image/annotation leakage)

## Tasks API

- [ ] `GET /api/tasks/?due_date=YYYY-MM-DD` filters by date
- [ ] `POST /api/tasks/` creates a task with expected defaults/order
- [ ] `PATCH /api/tasks/{id}/` updates fields correctly
- [ ] `DELETE /api/tasks/{id}/` deletes task
- [ ] `PATCH /api/tasks/reorder/` updates status/order atomically
- [ ] `GET /api/tags/` returns available tags

## Annotation API

- [ ] `POST /api/images/` accepts image + patient/test identifiers
- [ ] Uploaded image stores width/height and original name
- [ ] `GET /api/images/` returns only current user images
- [ ] `GET /api/images/{id}/annotations/` lists current image polygons
- [ ] `POST /api/images/{id}/annotations/` validates normalized points `[0,1]`
- [ ] `DELETE /api/annotations/{id}/` deletes one polygon
- [ ] `DELETE /api/images/{id}/annotations/clear/` clears only that image

## Series-scoped behavior

- [ ] `GET/PATCH /api/series-review/?patient_id=&patient_code=&test_code=` is isolated per series key
- [ ] `DELETE /api/series-annotations/clear/?patient_id=&patient_code=&test_code=` clears only that series
- [ ] Clearing one series does not affect other series annotations
- [ ] Series review records are unique per `(user, patient_id, patient_code, test_code)`

## Settings & security checks

- [ ] `SECRET_KEY` not hard-coded for production
- [ ] `DEBUG=False` works in production mode
- [ ] `ALLOWED_HOSTS` includes Render hostname in production
- [ ] `CORS_ALLOWED_ORIGINS` configured for frontend domain
- [ ] `CSRF_TRUSTED_ORIGINS` configured for backend/frontend domains
- [ ] Static files collect with WhiteNoise enabled in production mode
- [ ] `python manage.py check` passes without issues

## Build/deploy checks (Render)

- [ ] `build.sh` runs: install deps, collectstatic, migrate, seed demo user
- [ ] `render.yaml` defines database + web service
- [ ] Start command uses ASGI + Gunicorn/Uvicorn worker
- [ ] Required env vars present on Render: `DATABASE_URL`, `SECRET_KEY`, `DEBUG`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`

## Regression quick script (recommended)

- [ ] Login, create task, reorder task
- [ ] Upload image, create polygon, delete polygon
- [ ] Save series review for two distinct series and verify isolation
- [ ] Clear one series and verify other series still intact

