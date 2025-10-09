"""
Quick test script to verify the API is working correctly.
Run this after starting the server with: uvicorn main:app --reload
"""

import httpx
import asyncio


async def test_api():
    """Test the API endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Resource API\n")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    
    # Test 2: Health check
    print("\n2. Testing health check...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    
    # Test 3: Register a user
    print("\n3. Testing user registration...")
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123",
        "role": "user"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/api/v1/auth/register",
            json=user_data
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print(f"   ✅ User created successfully!")
            print(f"   User ID: {response.json()['id']}")
        elif response.status_code == 400:
            print(f"   ⚠️  User already exists (this is OK for subsequent runs)")
        else:
            print(f"   ❌ Error: {response.json()}")
    
    # Test 4: Login
    print("\n4. Testing user login...")
    login_data = {
        "username": user_data["email"],  # OAuth2 uses 'username' field
        "password": user_data["password"]
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/api/v1/auth/login",
            data=login_data
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print(f"   ✅ Login successful!")
            print(f"   Token (first 50 chars): {token[:50]}...")
        else:
            print(f"   ❌ Login failed: {response.json()}")
            return
    
    # Test 5: Access protected endpoint
    print("\n5. Testing protected endpoint (list users)...")
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/api/v1/users/",
            headers=headers
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            users = response.json()
            print(f"   ✅ Successfully retrieved {len(users)} user(s)")
        else:
            print(f"   ❌ Error: {response.json()}")
    
    # Test 6: Create a company
    print("\n6. Testing company creation...")
    company_data = {
        "name": "Test Company Inc."
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/api/v1/companies/",
            json=company_data,
            headers=headers
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            company = response.json()
            company_id = company["id"]
            print(f"   ✅ Company created successfully!")
            print(f"   Company ID: {company_id}")
            
            # Test 7: Update the company
            print("\n7. Testing company update...")
            update_data = {
                "name": "Test Company Inc. (Updated)"
            }
            
            response = await client.put(
                f"{base_url}/api/v1/companies/{company_id}",
                json=update_data,
                headers=headers
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ Company updated successfully!")
                print(f"   New name: {response.json()['name']}")
            
            # Test 8: Get the company
            print("\n8. Testing company retrieval...")
            response = await client.get(
                f"{base_url}/api/v1/companies/{company_id}",
                headers=headers
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ Company retrieved successfully!")
                print(f"   Company: {response.json()['name']}")
            
            # Test 9: List companies
            print("\n9. Testing company listing with pagination...")
            response = await client.get(
                f"{base_url}/api/v1/companies/?skip=0&limit=10",
                headers=headers
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                companies = response.json()
                print(f"   ✅ Successfully retrieved {len(companies)} company(ies)")
            
            # Test 10: Delete the company
            print("\n10. Testing company deletion...")
            response = await client.delete(
                f"{base_url}/api/v1/companies/{company_id}",
                headers=headers
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 204:
                print(f"   ✅ Company deleted successfully!")
        else:
            print(f"   ❌ Error creating company: {response.json()}")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!\n")
    print("Next steps:")
    print("1. Visit http://localhost:8000/docs for interactive API documentation")
    print("2. Try other endpoints using the Swagger UI")
    print("3. Review the API_REFERENCE.md for detailed endpoint information")


if __name__ == "__main__":
    print("\n⚠️  Make sure the server is running:")
    print("   uvicorn main:app --reload\n")
    
    try:
        asyncio.run(test_api())
    except httpx.ConnectError:
        print("\n❌ ERROR: Could not connect to the server!")
        print("   Please make sure the server is running on http://localhost:8000")
        print("   Start it with: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

