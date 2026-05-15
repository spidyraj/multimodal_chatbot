#!/usr/bin/env python3
"""
Script to add username column to existing users table
"""
import psycopg2
import os

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:sJgLfSHcvTrqZoDNXvhGRfmXHRpcXvyX@caboose.proxy.rlwy.net:54475/railway")

def add_username_column():
    try:
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check if username column already exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'username'
        """)
        
        if cursor.fetchone():
            print("Username column already exists")
            return
        
        # Add username column
        print("Adding username column to users table...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN username VARCHAR(50) UNIQUE NOT NULL
        """)
        
        # Create unique index on username
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username 
            ON users(username)
        """)
        
        conn.commit()
        print("Username column added successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    add_username_column()
