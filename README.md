# Shravani Construction

A professional, responsive construction and architecture company website built with Python Flask.

## Features
- Architecture-led landing page with company introduction
- Services, process, and completed-project showcase (illustrative demo projects)
- Responsive navigation and mobile-friendly layout
- Contact form backed by Flask and SQLite
- Direct phone and WhatsApp contact links

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Deployment
Set `SECRET_KEY` in the hosting environment and run `gunicorn app:app`. A `render.yaml` is included as a starting point.

## Business details
- Company: Shravani Construction
- Owner: Nitin Chandane
- Phone: +91 91465 85218

**Note:** Project cards are sample/demo portfolio entries. Replace them with verified company projects, photos, locations, and completion details before publishing as factual work.
