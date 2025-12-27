# Project Structure and Technology Stack

## Technology Stack

- **Backend Framework:** FastAPI (Python)
- **Database:** MariaDB (via Docker Compose)
- **ORM/ODM:** SQLModel (SQLAlchemy-based)
- **Templating:** Jinja2
- **Password Hashing:** hashlib (SHA256)
- **Testing:** pytest
- **Linting/Formatting:** ruff
- **Migrations:** Alembic
- **Environment Management:** uv
- **Containerization:** Docker Compose

## Directory Organization

```
root/
│
├── app/                  # Main application package
│   ├── __init__.py
│   ├── main.py           # FastAPI app entrypoint
│   ├── lib/              # Utility modules (e.g., passwords)
│   ├── models/           # Database models (e.g., user.py)
│   ├── routes/           # API routes (e.g., api/health.py)
│   └── templates/        # Jinja2 HTML templates
│       ├── _layout.html  # Base layout template
│       └── dashboard.html
│
├── utils/                # Standalone scripts (e.g., create_admin_user.py)
│
├── tests/                # Test suite (pytest)
│   └── lib/              # Tests for utility modules
│
├── docker-compose.yml    # Docker Compose configuration
├── Makefile              # Project automation commands
├── pyproject.toml        # Python project metadata and dependencies
├── .env.example          # Example environment variables
├── .env                  # Actual environment variables (not committed)
└── _specs/               # Project documentation and specifications
    └── project-structure.md
```

## Notes
- All environment variables are managed via `.env` files and loaded with `python-dotenv`.
- The Makefile provides commands for development, testing, linting, formatting, and database migrations.
- The project is designed for modularity, with clear separation between business logic, models, routes, and utilities.
