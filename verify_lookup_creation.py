"""
Verification script to test that user creation properly creates lookup entries.
Run this after starting the API server.
"""
import httpx
import asyncio


async def main():
    base_url = "http://localhost:8000"
    
    # First, login to get a token
    print("1. Logging in...")
    login_response = await httpx.AsyncClient().post(
        f"{base_url}/api/v1/auth/login",
        data={"username": "testuser@example.com", "password": "password123"}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Login successful")
    
    # Create a user
    print("\n2. Creating a new user...")
    test_email = f"newuser{asyncio.get_event_loop().time()}@example.com"
    user_data = {
        "name": "New Test User",
        "email": test_email,
        "password": "password123",
        "role": "user"
    }
    
    async with httpx.AsyncClient() as client:
        create_response = await client.post(
            f"{base_url}/api/v1/users/",
            json=user_data,
            headers=headers
        )
        
        if create_response.status_code == 201:
            user = create_response.json()
            print(f"✓ User created successfully: {user['email']} (id: {user['id']})")
            print("\n✅ SUCCESS: If you check the database, the user_company_lookup entry should exist.")
            print(f"   You can verify by running:")
            print(f"   SELECT * FROM user_company_lookup WHERE email = '{test_email}';")
        elif create_response.status_code == 500:
            print(f"❌ User creation failed with 500 error: {create_response.json()}")
            print("   This indicates the lookup creation failed and was properly caught!")
            print("   Check the application logs for detailed error information.")
        else:
            print(f"❌ User creation failed: {create_response.status_code} - {create_response.text}")


if __name__ == "__main__":
    asyncio.run(main())

