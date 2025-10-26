"""
Bootstrap script to create the first company and admin user.

This script helps solve the chicken-and-egg problem: you need a company to create users,
but you need an admin user to create companies.

Usage:
    python bootstrap_admin.py
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.db.database import create_company_schema, get_tenant_session
from app.models.company import Company
from app.models.user import User, UserRole
from app.models.user_company_lookup import UserCompanyLookup


async def bootstrap_admin():
    """Create the first company and admin user."""
    settings = get_settings()
    
    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        future=True
    )
    
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    print("\n" + "="*60)
    print("Bootstrap Admin User - First Company Setup")
    print("="*60 + "\n")
    
    # Get company details
    company_name = input("Enter company name: ").strip()
    if not company_name:
        print("❌ Company name is required")
        return
    
    # Get admin user details
    print("\n--- Admin User Details ---")
    admin_name = input("Admin name: ").strip()
    admin_email = input("Admin email: ").strip()
    admin_password = input("Admin password: ").strip()
    
    if not all([admin_name, admin_email, admin_password]):
        print("❌ All fields are required")
        return
    
    try:
        # Step 1: Create company in public schema
        async with async_session() as session:
            print(f"\n✓ Creating company '{company_name}'...")
            company = Company(name=company_name)
            session.add(company)
            await session.commit()
            await session.refresh(company)
            company_id = company.id
            print(f"✓ Company created with ID: {company_id}")
        
        # Step 2: Create tenant schema
        print(f"\n✓ Creating tenant schema 'company_{company_id}'...")
        await create_company_schema(company_id, seed_data=True)
        print(f"✓ Tenant schema created and reference data seeded")
        
        # Step 3: Create admin user in tenant schema
        print(f"\n✓ Creating admin user '{admin_email}'...")
        async for tenant_session in get_tenant_session(company_id):
            user = User(
                name=admin_name,
                email=admin_email,
                password_hash=get_password_hash(admin_password),
                role=UserRole.admin,
                is_active=True
            )
            tenant_session.add(user)
            await tenant_session.commit()
            await tenant_session.refresh(user)
            print(f"✓ Admin user created with ID: {user.id}")
        
        # Step 4: Create user_company_lookup entry
        print(f"\n✓ Creating user lookup entry...")
        async with async_session() as session:
            lookup = UserCompanyLookup(
                email=admin_email,
                company_id=company_id
            )
            session.add(lookup)
            await session.commit()
            print(f"✓ User lookup entry created")
        
        print("\n" + "="*60)
        print("✅ BOOTSTRAP SUCCESSFUL!")
        print("="*60)
        print(f"\nCompany: {company_name} (ID: {company_id})")
        print(f"Admin User: {admin_name} ({admin_email})")
        print(f"\nYou can now login with:")
        print(f"  Email: {admin_email}")
        print(f"  Password: {admin_password}")
        print(f"\nLogin command:")
        print(f'  curl -X POST http://localhost:8000/api/v1/auth/login \\')
        print(f'    -H "Content-Type: application/x-www-form-urlencoded" \\')
        print(f'    -d "username={admin_email}&password={admin_password}"')
        print()
        
    except Exception as e:
        print(f"\n❌ Error during bootstrap: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(bootstrap_admin())

