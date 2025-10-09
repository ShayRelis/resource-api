# API Reference

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment
Create a `.env` file:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 3. Create Tables
```bash
python -m app.db.create_tables
```

### 4. Run the Server
```bash
uvicorn main:app --reload
```

### 5. Access the API
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## Authentication Flow

### Step 1: Register
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepass123",
  "role": "user"
}
```

### Step 2: Login
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=john@example.com&password=securepass123
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Step 3: Use Token
Include the token in all subsequent requests:
```http
Authorization: Bearer eyJhbGc...
```

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login and get token | No |

### Users
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/users/` | Create user | Yes |
| GET | `/api/v1/users/` | List users | Yes |
| GET | `/api/v1/users/{id}` | Get user by ID | Yes |
| PUT | `/api/v1/users/{id}` | Update user | Yes |
| DELETE | `/api/v1/users/{id}` | Delete user | Yes |

### Companies
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/companies/` | Create company | Yes |
| GET | `/api/v1/companies/` | List companies | Yes |
| GET | `/api/v1/companies/{id}` | Get company by ID | Yes |
| PUT | `/api/v1/companies/{id}` | Update company | Yes |
| DELETE | `/api/v1/companies/{id}` | Delete company | Yes |

### Teams
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/teams/` | Create team | Yes |
| GET | `/api/v1/teams/` | List teams | Yes |
| GET | `/api/v1/teams/{id}` | Get team by ID | Yes |
| PUT | `/api/v1/teams/{id}` | Update team | Yes |
| DELETE | `/api/v1/teams/{id}` | Delete team | Yes |

### Cloud Providers
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/cloud-providers/` | Create cloud provider | Yes |
| GET | `/api/v1/cloud-providers/` | List cloud providers | Yes |
| GET | `/api/v1/cloud-providers/{id}` | Get cloud provider by ID | Yes |
| PUT | `/api/v1/cloud-providers/{id}` | Update cloud provider | Yes |
| DELETE | `/api/v1/cloud-providers/{id}` | Delete cloud provider | Yes |

### Registry Providers
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/registry-providers/` | Create registry provider | Yes |
| GET | `/api/v1/registry-providers/` | List registry providers | Yes |
| GET | `/api/v1/registry-providers/{id}` | Get registry provider by ID | Yes |
| PUT | `/api/v1/registry-providers/{id}` | Update registry provider | Yes |
| DELETE | `/api/v1/registry-providers/{id}` | Delete registry provider | Yes |

### Registries
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/registries/` | Create registry | Yes |
| GET | `/api/v1/registries/` | List registries | Yes |
| GET | `/api/v1/registries/{id}` | Get registry by ID | Yes |
| PUT | `/api/v1/registries/{id}` | Update registry | Yes |
| DELETE | `/api/v1/registries/{id}` | Delete registry | Yes |

### Registry Credentials
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/registry-credentials/` | Create credential | Yes |
| GET | `/api/v1/registry-credentials/` | List credentials | Yes |
| GET | `/api/v1/registry-credentials/{id}` | Get credential by ID | Yes |
| PUT | `/api/v1/registry-credentials/{id}` | Update credential | Yes |
| DELETE | `/api/v1/registry-credentials/{id}` | Delete credential | Yes |

### Container Images
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/container-images/` | Create container image | Yes |
| GET | `/api/v1/container-images/` | List container images | Yes |
| GET | `/api/v1/container-images/{id}` | Get container image by ID | Yes |
| PUT | `/api/v1/container-images/{id}` | Update container image | Yes |
| DELETE | `/api/v1/container-images/{id}` | Delete container image | Yes |

### Service Types
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/service-types/` | Create service type | Yes |
| GET | `/api/v1/service-types/` | List service types | Yes |
| GET | `/api/v1/service-types/{id}` | Get service type by ID | Yes |
| PUT | `/api/v1/service-types/{id}` | Update service type | Yes |
| DELETE | `/api/v1/service-types/{id}` | Delete service type | Yes |

### Tags
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/tags/` | Create tag | Yes |
| GET | `/api/v1/tags/` | List tags | Yes |
| GET | `/api/v1/tags/{id}` | Get tag by ID | Yes |
| PUT | `/api/v1/tags/{id}` | Update tag | Yes |
| DELETE | `/api/v1/tags/{id}` | Delete tag | Yes |

## Query Parameters

All `GET /` endpoints support pagination:
- `skip` (default: 0) - Number of records to skip
- `limit` (default: 100) - Maximum number of records to return

**Example:**
```http
GET /api/v1/users/?skip=0&limit=20
```

## Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Resource deleted successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required or failed |
| 404 | Not Found - Resource not found |
| 422 | Validation Error - Invalid input data |
| 500 | Internal Server Error - Server error |

## Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Architecture Overview

### Layers

1. **API Layer** (`app/api/`)
   - Handles HTTP requests/responses
   - Validates input using Pydantic schemas
   - Enforces authentication
   - Returns appropriate HTTP status codes

2. **CRUD Layer** (`app/crud/`)
   - Database operations (Create, Read, Update, Delete)
   - Business logic
   - Database transaction management

3. **Model Layer** (`app/models/`)
   - SQLAlchemy ORM models
   - Database schema definitions

4. **Schema Layer** (`app/schemas/`)
   - Pydantic models for validation
   - Request/Response schemas

### Dependency Injection

The API uses FastAPI's dependency injection for:
- Database sessions (`get_db`)
- Authentication (`get_current_user`, `get_current_active_user`)

### Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication (30-minute expiration)
- All endpoints (except auth) require authentication
- CORS enabled (configure for production)

## Development Tips

### Testing with cURL

```bash
# Store token in variable
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=securepass123" \
  | jq -r '.access_token')

# Use token in requests
curl -X GET "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer $TOKEN"
```

### Testing with Python

```python
import httpx

# Login
response = httpx.post(
    "http://localhost:8000/api/v1/auth/login",
    data={"username": "john@example.com", "password": "securepass123"}
)
token = response.json()["access_token"]

# Make authenticated request
headers = {"Authorization": f"Bearer {token}"}
response = httpx.get("http://localhost:8000/api/v1/users/", headers=headers)
print(response.json())
```

## Production Checklist

- [ ] Update `SECRET_KEY` in environment variables
- [ ] Configure CORS with specific origins
- [ ] Enable HTTPS
- [ ] Set up database connection pooling
- [ ] Add rate limiting
- [ ] Configure logging
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Use production database credentials
- [ ] Configure reverse proxy (nginx)
- [ ] Set up database backups
- [ ] Enable database migrations (Alembic)

