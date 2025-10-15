# Resource API Test Suite

Comprehensive pytest-based test suite for the Resource API, covering all entities and endpoints with CRUD operations, validation, error handling, and relationship testing.

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `pytest>=7.4.0` - Testing framework
- `pytest-asyncio>=0.21.0` - Async test support
- `httpx>=0.25.0` - Async HTTP client

### Start the Server

Before running tests, make sure the API server is running:

```bash
# Start the server
uvicorn main:app --reload

# Or use the start script
./start.sh
```

The server should be running on `http://localhost:8000`.

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run Tests for a Specific File

```bash
# Test authentication
pytest tests/test_auth.py

# Test companies
pytest tests/test_companies.py

# Test container images
pytest tests/test_container_images.py
```

### Run a Specific Test Class

```bash
pytest tests/test_auth.py::TestUserRegistration
```

### Run a Specific Test Function

```bash
pytest tests/test_auth.py::TestUserRegistration::test_register_user_success
```

### Run Tests by Pattern

```bash
# Run all CRUD tests
pytest -k "crud"

# Run all validation tests
pytest -k "validation"

# Run all error tests
pytest -k "error"
```

### Run Tests with Coverage (if pytest-cov is installed)

```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
```

## Test Structure

The test suite is organized by entity, with each file testing a specific resource:

### Test Files

- **test_auth.py** - Authentication (registration, login, token validation)
- **test_users.py** - User CRUD operations and validation
- **test_companies.py** - Company CRUD operations and validation
- **test_teams.py** - Team CRUD operations and company relationships
- **test_cloud_providers.py** - Cloud provider CRUD operations
- **test_registry_providers.py** - Registry provider CRUD operations
- **test_registries.py** - Registry CRUD operations and relationships
- **test_registry_credentials.py** - Registry credential CRUD operations
- **test_container_images.py** - Container image CRUD operations and relationships
- **test_service_types.py** - Service type CRUD operations
- **test_tags.py** - Tag CRUD operations and company relationships

### Test Organization

Each test file is organized into classes by test type:

```python
class TestEntityCRUD:
    # Test create, read, update, delete operations
    
class TestEntityPagination:
    # Test listing with skip/limit parameters
    
class TestEntityValidation:
    # Test validation rules and missing fields
    
class TestEntityRelationships:
    # Test foreign key relationships
    
class TestEntityErrors:
    # Test 404 and error responses
```

## Shared Fixtures

The `conftest.py` file contains shared fixtures used across all tests:

### Core Fixtures

- **async_client** - httpx.AsyncClient for making HTTP requests
- **auth_token** - Authentication token for protected endpoints
- **auth_headers** - Headers dict with Bearer token
- **test_user_data** - Sample user data for tests

### Entity Fixtures

- **test_company** - Creates and cleans up a test company
- **test_registry_provider** - Creates and cleans up a test registry provider
- **test_registry** - Creates and cleans up a test registry

These fixtures handle both setup and teardown automatically.

## Test Coverage

The test suite provides comprehensive coverage:

### CRUD Operations
- ✅ Create operations with valid data
- ✅ Read single entities
- ✅ Update entities
- ✅ Delete entities
- ✅ List all entities

### Pagination
- ✅ List with skip parameter
- ✅ List with limit parameter
- ✅ List with both skip and limit

### Validation
- ✅ Missing required fields
- ✅ Invalid data formats
- ✅ Empty values
- ✅ Invalid email formats
- ✅ Invalid foreign keys

### Error Handling
- ✅ 404 for non-existent entities
- ✅ 401 for unauthorized access
- ✅ 422 for validation errors
- ✅ 400 for invalid foreign keys

### Relationships
- ✅ Valid foreign key references
- ✅ Invalid foreign key references
- ✅ Optional foreign key fields (NULL values)
- ✅ Cascading relationships

## Example Test Session

```bash
$ pytest tests/test_companies.py -v

tests/test_companies.py::TestCompanyCRUD::test_create_company PASSED
tests/test_companies.py::TestCompanyCRUD::test_get_company PASSED
tests/test_companies.py::TestCompanyCRUD::test_update_company PASSED
tests/test_companies.py::TestCompanyCRUD::test_delete_company PASSED
tests/test_companies.py::TestCompanyCRUD::test_list_companies PASSED
tests/test_companies.py::TestCompanyPagination::test_list_companies_with_pagination PASSED
tests/test_companies.py::TestCompanyValidation::test_create_company_missing_name PASSED
tests/test_companies.py::TestCompanyErrors::test_get_nonexistent_company PASSED
tests/test_companies.py::TestCompanyErrors::test_update_nonexistent_company PASSED
tests/test_companies.py::TestCompanyErrors::test_delete_nonexistent_company PASSED

========== 10 passed in 2.34s ==========
```

## Troubleshooting

### Connection Errors

If you get connection errors:
```
ERROR: Could not connect to the server!
```

Make sure the server is running:
```bash
uvicorn main:app --reload
```

### Test Database

The tests use the same database as the development server. For production use, consider:
- Using a separate test database
- Implementing database cleanup between test runs
- Using database transactions that rollback after each test

### Async Warnings

If you see warnings about async tests, make sure `pytest-asyncio` is installed:
```bash
pip install pytest-asyncio>=0.21.0
```

## Writing New Tests

When adding new endpoints or features, follow the existing test patterns:

```python
class TestNewFeature:
    """Test new feature."""

    async def test_new_feature_success(
        self, 
        async_client: httpx.AsyncClient, 
        auth_headers: dict
    ):
        """Test successful new feature."""
        # Arrange
        data = {"key": "value"}
        
        # Act
        response = await async_client.post(
            "/api/v1/new-endpoint/",
            json=data,
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 201
        assert response.json()["key"] == "value"
```

## Contributing

When contributing tests:
1. Follow the existing test structure and naming conventions
2. Use descriptive test names that explain what is being tested
3. Include docstrings for test classes and functions
4. Test both success and failure cases
5. Clean up any test data created during tests
6. Ensure all tests pass before submitting

## Next Steps

- Consider adding integration tests for complex workflows
- Add performance/load testing with tools like locust
- Implement database fixtures for consistent test data
- Add test coverage reporting to CI/CD pipeline
- Consider using pytest-xdist for parallel test execution

