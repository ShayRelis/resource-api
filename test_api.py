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
    
    # Test 3: Login (user must be bootstrapped first)
    print("\n3. Testing user login...")
    print("   Note: You must first create an admin user using bootstrap_admin.py")
    user_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
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
    
    # Test 4: Access protected endpoint
    print("\n4. Testing protected endpoint (list users)...")
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
    
    # Test 5: Create a company
    print("\n5. Testing company creation...")
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
            
            # Test 6: Update the company
            print("\n6. Testing company update...")
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
            
            # Test 7: Get the company
            print("\n7. Testing company retrieval...")
            response = await client.get(
                f"{base_url}/api/v1/companies/{company_id}",
                headers=headers
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ Company retrieved successfully!")
                print(f"   Company: {response.json()['name']}")
            
            # Test 8: List companies
            print("\n8. Testing company listing with pagination...")
            response = await client.get(
                f"{base_url}/api/v1/companies/?skip=0&limit=10",
                headers=headers
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                companies = response.json()
                print(f"   ✅ Successfully retrieved {len(companies)} company(ies)")
            
            # Test 9: Delete the company
            print("\n9. Testing company deletion...")
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

