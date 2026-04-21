# FastAPI Authentication Project

A modern REST API built with FastAPI featuring user authentication and authorization capabilities.

## Features

- 🔐 User authentication with JWT tokens
- 👤 User management system
- 🗄️ SQLAlchemy ORM with Alembic migrations
- 🐳 Docker and Docker Compose support
- 📝 OpenAPI/Swagger documentation
- 🔒 Password hashing and security best practices

## Project Structure

```
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── config.py           # Configuration and environment variables
│   │   └── security.py         # Authentication and security utilities
│   ├── db/
│   │   ├── base.py             # SQLAlchemy base model
│   │   ├── session.py          # Database session management
│   │   └── models/
│   │       └── user.py         # User database model
│   └── modules/
│       ├── auth/
│       │   ├── router.py       # Authentication routes
│       │   ├── schemas.py      # Pydantic schemas for auth
│       │   └── service.py      # Authentication business logic
│       └── users/
│           ├── router.py       # User management routes
│           ├── schemas.py      # Pydantic schemas for users
│           └── service.py      # User business logic
├── alembic/
│   ├── env.py                  # Alembic environment configuration
│   └── versions/               # Database migration scripts
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose services
├── alembic.ini                 # Alembic configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Prerequisites

- Python 3.9+
- pip or pip3
- Docker and Docker Compose (optional)
- PostgreSQL or SQLite

## Installation

### Using pip (Local Development)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd python-fastApi-auth
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory with your configuration:
   ```
   DATABASE_URL=sqlite:///./test.db
   JWT_SECRET=your-secret-key-here
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the application:**
   
   **Development mode (with auto-reload):**
   ```bash
   uvicorn app.main:app --reload
   ```

   **Production mode:**
   ```bash
   gunicorn app.main:app -c gunicorn.conf.py
   ```

   The API will be available at `http://localhost:8008`
   Swagger documentation: `http://localhost:8008/docs`

### Using Docker

1. **Build and run with Docker Compose:**
   
   **Development mode (with hot-reload):**
   ```bash
   docker-compose up -d
   ```
   This uses Uvicorn directly with auto-reload enabled.

   **Production mode:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```
   This uses Gunicorn with Uvicorn workers for better performance.

2. **View logs:**
   ```bash
   docker-compose logs -f api
   ```

The API will be available at `http://localhost:8008`

Note: Migrations are automatically applied on container startup.

## API Endpoints

### Authentication (`/auth`)
- `POST /auth/login` - Login with credentials
- `POST /auth/register` - Create a new user account

### Users (`/users`)
- `GET /users/me` - Get current user information (requires authentication)
- `PATCH /users/me` - Update current user's profile (requires authentication)
  - Request body: `{"full_name": "string"}`
  - Updates the authenticated user's full name

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback last migration:
```bash
alembic downgrade -1
```

## Environment Variables

Key environment variables to configure:

- `DATABASE_URL` - Database connection string
- `JWT_SECRET` - Secret key for JWT token signing
- `JWT_ALGORITHM` - Algorithm for JWT encoding (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `APP_ENV` - Environment mode (`local` for development, `production` for production)

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black app/
```

### Linting

```bash
flake8 app/
pylint app/
```

## Security Notes

- Always use strong secret keys in production
- Store sensitive variables in environment files (not in version control)
- Use HTTPS in production
- Implement rate limiting for authentication endpoints
- Regularly update dependencies

## Contributing

1. Create a feature branch (`git checkout -b feature/your-feature`)
2. Commit your changes (`git commit -am 'Add your feature'`)
3. Push to the branch (`git push origin feature/your-feature`)
4. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open an issue on the repository.
