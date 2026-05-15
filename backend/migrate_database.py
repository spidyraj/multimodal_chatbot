#!/usr/bin/env python3
"""
Database migration script to add username column
"""
import os
import sys
from sqlalchemy import create_engine, text
from core.config import settings

def migrate_database():
    try:
        print("Starting database migration...")
        
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            # Check if username column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'username'
            """))
            
            if result.fetchone():
                print("✅ Username column already exists")
                return
            
            # Add username column
            print("📝 Adding username column to users table...")
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN username VARCHAR(50) UNIQUE NOT NULL DEFAULT 'temp_user'
            """))
            
            # Update existing users with temporary usernames
            conn.execute(text("""
                UPDATE users 
                SET username = 'user_' || id::text 
                WHERE username = 'temp_user'
            """))
            
            # Create unique index
            conn.execute(text("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username 
                ON users(username)
            """))
            
            conn.commit()
            print("✅ Migration completed successfully!")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate_database()
