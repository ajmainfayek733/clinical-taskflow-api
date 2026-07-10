# Clinical TaskFlow — Backend

Django 6 + Django REST Framework API for clinical task management and image annotation.

## Requirements

- Python 3.11+ (tested on 3.14)
- pip / venv

## Setup

```bash
cd taskflow-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_demo_user
python manage.py runserver
```

| Resource | URL |
|---|---|
| API | `http://127.0.0.1:8000/api` |
| Swagger | `http://127.0.0.1:8000/api/docs/` |

## Demo credentials

| Field | Value |
|---|---|
| Email | `demo.doctor@taskflow.local` |
| Password | `DoctorDemo123!` |

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/login/` | JWT login |
| GET/POST | `/api/tasks/` | Task CRUD (filter `?due_date=`) |
| PATCH | `/api/tasks/reorder/` | Bulk drag/drop reorder |
| GET/POST | `/api/images/` | Upload with `patient_id`, `patient_code`, `test_code` |
| GET/POST | `/api/images/{id}/annotations/` | List/create polygons |
| DELETE | `/api/annotations/{id}/` | Delete one polygon |
| DELETE | `/api/images/{id}/annotations/clear/` | Clear image polygons |
| DELETE | `/api/series-annotations/clear/?patient_id=&patient_code=&test_code=` | Clear all polygons in a series |
| GET/PATCH | `/api/series-review/` | Series-level notes |

## QA checklist

See [`../QA_CHECKLIST.md`](../QA_CHECKLIST.md) for acceptance criteria and demo script.

## Challenges faced

- **Image dimensions:** Pillow reads width/height on upload for correct canvas letterboxing.
- **Annotation validation:** normalized `[0,1]` polygon points validated server-side.
- **User isolation:** all querysets filtered by `request.user` — no cross-user data access.
- **JWT auth:** SimpleJWT access/refresh tokens for decoupled Next.js frontend.

## Deployment on Render

This project is configured for [Render](https://render.com) using the official Django guide:
[Deploy a Django App on Render](https://render.com/docs/deploy-django).

### Blueprint (recommended)

1. Push this repo to GitHub.
2. In Render Dashboard → **Blueprints** → **New Blueprint Instance**.
3. Connect the repository and apply `render.yaml`.
4. After deploy, set these environment variables on the web service:
   - `CORS_ALLOWED_ORIGINS` = `https://<your-frontend>.onrender.com`
   - `CSRF_TRUSTED_ORIGINS` = `https://<your-backend>.onrender.com,https://<your-frontend>.onrender.com`

### Manual web service

| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Build Command | `./build.sh` |
| Start Command | `python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker` |

Required env vars: `DATABASE_URL`, `SECRET_KEY`, `DEBUG=False`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`.

`build.sh` installs dependencies, runs `collectstatic`, migrates, and seeds the demo user.

### Notes

- PostgreSQL is used on Render via `DATABASE_URL`; local dev still defaults to SQLite.
- Uploaded images are stored on the service disk (ephemeral on free tier). For production persistence, use S3-compatible storage.
- API docs: `https://<your-backend>.onrender.com/api/docs/`

## Local production check

```bash
export SECRET_KEY=your-secret
export DEBUG=False
export ALLOWED_HOSTS=127.0.0.1,localhost
export CORS_ALLOWED_ORIGINS=http://localhost:3000
python manage.py collectstatic --no-input
python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
```
