# Quick Start Guide

## ⚡ Get Started in 5 Minutes

### Step 1: Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### Step 2: Verify Environment (30 sec)
Make sure your `.env` file exists with database configuration:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Step 3: Create Database Tables (30 sec)
```bash
python -m app.db.create_tables
```

### Step 4: Start the Server (30 sec)
```bash
uvicorn main:app --reload
```

Or use the convenience script:
```bash
./start.sh
```

### Step 5: Test the API (2 min)

#### Option A: Use the Interactive Docs
1. Open http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Execute requests directly from the browser

#### Option B: Use the Test Script
```bash
python test_api.py
```

#### Option C: Manual Testing with cURL

**Register a user:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepass123",
    "role": "user"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=securepass123"
```

**Use the token:**
```bash
# Save the token from the login response
TOKEN="your_token_here"

# List users
curl -X GET "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer $TOKEN"
```

## 🎯 What You Get

### Endpoints Available
- **Authentication**: Register and login
- **Users**: Full CRUD operations
- **Companies**: Full CRUD operations
- **Teams**: Full CRUD operations
- **Cloud Providers**: Full CRUD operations
- **Registry Providers**: Full CRUD operations
- **Registries**: Full CRUD operations
- **Registry Credentials**: Full CRUD operations
- **Container Images**: Full CRUD operations
- **Service Types**: Full CRUD operations
- **Tags**: Full CRUD operations

### Each Resource Has
- ✅ `POST /` - Create
- ✅ `GET /` - List (with pagination)
- ✅ `GET /{id}` - Get by ID
- ✅ `PUT /{id}` - Update
- ✅ `DELETE /{id}` - Delete

## 📚 Next Steps

### Learn More
- Read `README.md` for comprehensive documentation
- Check `API_REFERENCE.md` for endpoint details
- Review `IMPLEMENTATION_SUMMARY.md` for architecture overview

### Development Workflow
1. **Make changes** to your code
2. **Server auto-reloads** (with `--reload` flag)
3. **Test in browser** at http://localhost:8000/docs
4. **Or use test script**: `python test_api.py`

### Common Tasks

#### Add a New Endpoint
1. Create CRUD operations in `app/crud/`
2. Create endpoints in `app/api/v1/endpoints/`
3. Register router in `app/api/v1/api.py`

#### Access Database Directly
```python
from app.db.database import async_session
from app.models import User
from sqlalchemy import select

async def get_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()
```

#### Test Authentication Flow
```python
import httpx

async def test_auth():
    async with httpx.AsyncClient() as client:
        # Register
        await client.post("http://localhost:8000/api/v1/auth/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "pass123"
        })
        
        # Login
        response = await client.post("http://localhost:8000/api/v1/auth/login", data={
            "username": "test@example.com",
            "password": "pass123"
        })
        
        token = response.json()["access_token"]
        
        # Use token
        headers = {"Authorization": f"Bearer {token}"}
        users = await client.get("http://localhost:8000/api/v1/users/", headers=headers)
        print(users.json())
```

## 🐛 Troubleshooting

### Issue: "Could not connect to database"
**Solution:** Check your `.env` file and ensure PostgreSQL is running
```bash
# Check if PostgreSQL is running
psql -h localhost -U your_user -d your_database
```

### Issue: "Module not found"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Port already in use"
**Solution:** Change the port or kill the existing process
```bash
# Use a different port
uvicorn main:app --reload --port 8001

# Or find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Issue: "Token has expired"
**Solution:** Login again to get a new token (tokens expire after 30 minutes)

### Issue: "Unauthorized" error
**Solution:** Make sure you're including the token in the Authorization header
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/v1/users/
```

## 📊 Project Status

### ✅ Completed
- [x] Complete API layer with all endpoints
- [x] JWT authentication
- [x] CRUD operations for all models
- [x] Async database operations
- [x] Input validation
- [x] Error handling
- [x] API documentation
- [x] CORS support

### 🚀 Ready for Production (After Setup)
1. Update `SECRET_KEY` in environment variables
2. Configure CORS for specific origins
3. Set up HTTPS
4. Enable database migrations (Alembic)
5. Add logging and monitoring
6. Set up rate limiting

## 💡 Tips

1. **Use the Swagger UI** - It's the fastest way to explore the API
2. **Check the logs** - The server logs show all SQL queries (set `echo=False` in production)
3. **Use type hints** - Your IDE will provide better autocomplete
4. **Read the docstrings** - All functions are documented
5. **Follow the patterns** - The codebase is consistent and follows best practices

## 🎉 You're All Set!

Your API is now running with:
- 55+ endpoints
- 10 domain models
- Full authentication
- Complete CRUD operations
- Production-ready architecture

Happy coding! 🚀

