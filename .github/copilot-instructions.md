# Copilot Instructions for LinkeyDigital_back (soyyo-services-django)

## Project Overview
- **Framework:** Django 4.1.1 (REST API backend)
- **Main entry:** `manage.py` (development), `Procfile` with Gunicorn (production)
- **Modular apps:** Each business domain (authentication, administration, profile, contact, pay, mercado_pago, booking, client_contact, ecommerce, public) is a Django app with its own models, views, services, and URLs.
- **Custom authentication:** Uses Firebase via `authentication/authentication.py` (see `FirebaseAuthentication` class). Integrates with Django's user model (`authentication.CustomerUser`).
- **Multi-environment config:** Core settings (DB, Firebase, etc.) are in `conf_fire_base.py` and imported in `soyyo_api/settings.py`. Modes for Bolivia, Chile, Brazil, Portugal.

## Key Workflows
- **Run locally:**
  - `python manage.py runserver` (uses settings from `soyyo_api/settings.py`)
- **Production run:**
  - `gunicorn soyyo_api.wsgi --log-file -` (see `Procfile`)
- **Database:**
  - Default: PostgreSQL (see `conf_fire_base.py`)
  - Migrations: `python manage.py makemigrations`, `python manage.py migrate`
- **Testing:**
  - No standard test runner or test structure enforced; check each app's `tests.py` for custom logic.

## Project Conventions & Patterns
- **App structure:** Each app (e.g., `authentication`, `administration`, etc.) contains `models/`, `views/`, `services/`, and sometimes `serializers.py` or `Utilities*.py`.
- **URL routing:** All app URLs are included in `soyyo_api/urls.py` under their respective prefixes.
- **Settings:**
  - Sensitive and environment-specific config is in `conf_fire_base.py` (not versioned; see comments in file).
  - `soyyo_api/settings.py` imports from `conf_fire_base.py` for DB, email, and mode selection.
- **Authentication:**
  - Custom DRF authentication using Firebase tokens (see `authentication/authentication.py`).
  - Raises custom exceptions for token issues.
- **External integrations:**
  - Firebase (auth, config in `conf_fire_base.py`)
  - MercadoPago (see `mercado_pago/`)

## Examples
- **Add a new API endpoint:**
  1. Create a view in the relevant app's `views/`.
  2. Add a URL pattern in the app's `urls.py`.
  3. Include the app's URLs in `soyyo_api/urls.py` if not already present.
- **Switch environment:**
  - Edit flags in `conf_fire_base.py` (e.g., `BOLIVIA_MODE = True`).

## References
- `soyyo_api/settings.py`, `conf_fire_base.py`, `authentication/authentication.py`, `Procfile`, each app's `urls.py` and `views/`

---
If any section is unclear or missing, please specify what needs more detail or examples.
