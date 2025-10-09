# Resource API

A production-ready FastAPI application for managing cloud resources, registries, and container images.

## Features

- ✅ **Complete CRUD Operations** for all domain models
- ✅ **JWT Authentication** with secure password hashing
- ✅ **Async SQLAlchemy** for high-performance database operations
- ✅ **RESTful API Design** with proper HTTP status codes
- ✅ **API Versioning** (v1)
- ✅ **CORS Support** for cross-origin requests
- ✅ **Automatic API Documentation** (Swagger UI & ReDoc)
- ✅ **Type Safety** with Pydantic schemas
- ✅ **Dependency Injection** for clean architecture

## Project Structure

```
resource-api/
├── app/
│   ├── api/
│   │   ├── deps.py                 # Dependency injection utilities
│   │   └── v1/
│   │       ├── api.py              # Router aggregation
│   │       └── endpoints/          # API endpoints
│   │           ├── auth.py         # Authentication (register, login)
│   │           ├── users.py        # User management
│   │           ├── companies.py    # Company management
│   │           ├── teams.py        # Team management
│   │           ├── cloud_providers.py
│   │           ├── registry_providers.py
│   │           ├── registries.py
│   │           ├── registry_credentials.py
│   │           ├── container_images.py
│   │           ├── service_types.py
│   │           └── tags.py
│   ├── core/
│   │   ├── config.py               # Configuration settings
│   │   └── security.py             # Password hashing, JWT tokens
│   ├── crud/
│   │   ├── base.py                 # Base CRUD operations
│   │   └── crud_*.py               # Specific CRUD implementations
│   ├── db/
│   │   ├── database.py             # Database setup
│   │   └── create_tables.py        # Table creation
│   ├── models/                     # SQLAlchemy models
│   └── schemas/                    # Pydantic schemas
├── main.py                         # FastAPI application entry point
├── requirements.txt                # Python dependencies
└── README.md
```

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL database

### Setup

1. **Clone the repository** (if applicable)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

4. **Create database tables:**
   ```bash
   python -m app.db.create_tables
   ```

## Running the Application

### Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL:** http://localhost:8000
- **Interactive Docs (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

### Production Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Usage

### Authentication

#### Register a new user

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "user"
  }'
```

#### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Protected Endpoints

All resource endpoints require authentication. Include the JWT token in the Authorization header:

```bash
curl -X GET "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Available Endpoints

Each resource has the following endpoints:

- **POST /** - Create a new resource
- **GET /** - List resources (with pagination: `?skip=0&limit=100`)
- **GET /{id}** - Get a specific resource by ID
- **PUT /{id}** - Update a resource
- **DELETE /{id}** - Delete a resource

### Resources

- `/api/v1/auth/register` - User registration
- `/api/v1/auth/login` - User login
- `/api/v1/users` - User management
- `/api/v1/companies` - Company management
- `/api/v1/teams` - Team management
- `/api/v1/cloud-providers` - Cloud provider management
- `/api/v1/registry-providers` - Registry provider management
- `/api/v1/registries` - Registry management
- `/api/v1/registry-credentials` - Registry credential management
- `/api/v1/container-images` - Container image management
- `/api/v1/service-types` - Service type management
- `/api/v1/tags` - Tag management

## Examples

### Create a Company

```bash
curl -X POST "http://localhost:8000/api/v1/companies/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corporation"
  }'
```

### List Companies with Pagination

```bash
curl -X GET "http://localhost:8000/api/v1/companies/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update a Company

```bash
curl -X PUT "http://localhost:8000/api/v1/companies/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corp Updated"
  }'
```

### Delete a Company

```bash
curl -X DELETE "http://localhost:8000/api/v1/companies/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Security Considerations

### Production Deployment

Before deploying to production, make sure to:

1. **Update the SECRET_KEY** in `app/core/security.py`:
   ```python
   SECRET_KEY = os.getenv("SECRET_KEY", "your-production-secret-key")
   ```
   Add `SECRET_KEY` to your `.env` file with a secure random string.

2. **Configure CORS** in `main.py`:
   ```python
   allow_origins=["https://yourdomain.com"]  # Replace with your actual domain
   ```

3. **Use HTTPS** in production

4. **Set secure database credentials**

5. **Enable rate limiting** (consider using `slowapi`)

6. **Add logging and monitoring**

## Development

### Adding a New Resource

1. Create the SQLAlchemy model in `app/models/`
2. Create Pydantic schemas in `app/schemas/`
3. Create CRUD operations in `app/crud/`
4. Create API endpoints in `app/api/v1/endpoints/`
5. Register the router in `app/api/v1/api.py`

### Database Migrations

For database migrations, consider using Alembic:

```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Testing

To test the API, you can:

1. Use the interactive Swagger UI at http://localhost:8000/docs
2. Use curl commands (examples above)
3. Use tools like Postman or Insomnia
4. Write automated tests using `pytest` and `httpx`

## Error Handling

The API uses standard HTTP status codes:

- **200** - Success
- **201** - Created
- **204** - No Content (successful deletion)
- **400** - Bad Request
- **401** - Unauthorized
- **404** - Not Found
- **422** - Validation Error
- **500** - Internal Server Error

## License

[Your License Here]

## Support

For issues or questions, please contact [your-email@example.com]

