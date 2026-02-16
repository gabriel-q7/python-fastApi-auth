# Copilot Instructions

## Architecture Overview

This is a modular FastAPI authentication service using JWT tokens, SQLAlchemy ORM, and PostgreSQL. The codebase follows a **domain-driven design pattern** with clear separation between routers, services, and database models.

**Key architecture decisions:**
- **Module structure**: Each domain (`auth`, `users`) has its own `router.py` (HTTP layer), `service.py` (business logic), and `schemas.py` (Pydantic models)
- **Dependency injection**: Database sessions are injected via `Depends(get_db)` from [app/db/session.py](app/db/session.py)
- **Authentication flow**: JWT tokens issued in [app/core/security.py](app/core/security.py), validated by `get_current_user` dependency in [app/modules/users/router.py](app/modules/users/router.py#L13-L25)
- **Settings management**: All configuration via Pydantic Settings in [app/core/config.py](app/core/config.py) - uses `.env` file or environment variables

## Environment & Dependencies

**Python version**: Use Python 3.12 or 3.13 only - Python 3.14+ breaks `pydantic` compilation (see [lessons-learned.md](lessons-learned.md#L18-L66))

**Required environment variables** (in `.env`):
```env
DATABASE_URL=postgresql://app:app@localhost:5432/app
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Note: README.md uses outdated variable names (`SECRET_KEY`, `ALGORITHM`) - correct ones are `JWT_SECRET` and `JWT_ALGORITHM` per [app/core/config.py](app/core/config.py#L6-L7).

## Development Workflows

**Initial setup (first terminal run):**
```bash
source .venv/bin/activate
```

**Running locally:**
```bash
# Development with auto-reload
uvicorn app.main:app --reload

# Production mode
gunicorn app.main:app -c gunicorn.conf.py
```

**Docker development:**
```bash
# Development (Uvicorn with hot-reload)
docker-compose up -d

# Production (Gunicorn + Uvicorn workers)
docker-compose -f docker-compose.prod.yml up -d
```

Migrations run automatically on container startup via [start.sh](start.sh).

**Testing:**
```bash
pytest -v  # All tests with verbose output
pytest tests/test_auth.py  # Specific module
```

Tests use in-memory SQLite and fixtures from [tests/conftest.py](tests/conftest.py). The `create_test_user` fixture auto-registers a user and returns a token for authenticated endpoints.

## Database & Migrations

Database models live in `app/db/models/`. Base model is [app/db/base.py](app/db/base.py).

**Creating migrations:**
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

**SQLAlchemy patterns used:**
- SQLAlchemy 2.0 style with `select()` statements (not legacy Query API)
- Example: `db.scalar(select(User).where(User.email == email))` in [app/modules/auth/service.py](app/modules/auth/service.py#L9)

## Project Conventions

**Error handling:**
- Services raise `ValueError` with string codes (e.g., `"EMAIL_EXISTS"`)
- Routers catch these and convert to HTTP exceptions with appropriate status codes
- See [app/modules/auth/router.py](app/modules/auth/router.py#L11-L15) for pattern

**Security patterns:**
- Password hashing: `hash_password()` and `verify_password()` from [app/core/security.py](app/core/security.py)
- Token creation: `create_access_token(subject=str(user.id))` - subject is always user ID
- Protected endpoints: Use `user=Depends(get_current_user)` dependency

**Response models:**
- Always define Pydantic response models in `schemas.py`
- Use `response_model` parameter on router decorators
- Example: `@router.get("/me", response_model=UserOut)`

## Known Issues & Gotchas

- **No refresh token endpoint yet** - listed in TODOs but not implemented despite being in README
- **PATCH /users/me exists** but README doesn't document it (see [TODOs.md](TODOs.md#L3-L6))
- **Gunicorn logs** go to `logs/` directory - ensure it exists or mount volume in Docker
- **User endpoints missing** - Only `/users/me` and `PATCH /users/me` exist; other CRUD endpoints from README are not implemented

## Adding New Features

**Creating a new module:**
1. Create directory under `app/modules/`
2. Add `router.py`, `service.py`, `schemas.py`
3. Register router in [app/main.py](app/main.py): `app.include_router(router)`
4. Follow existing auth/users module structure

**Adding database models:**
1. Create model in `app/db/models/` inheriting from `Base`
2. Import in `app/db/base.py` for Alembic autogenerate
3. Run `alembic revision --autogenerate -m "add_model"`
