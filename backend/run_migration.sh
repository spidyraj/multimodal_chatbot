#!/bin/bash
echo "🔄 Running database migration..."

# Set environment variables
export DATABASE_URL="postgresql://postgres:sJgLfSHcvTrqZoDNXvhGRfmXHRpcXvyX@caboose.proxy.rlwy.net:54475/railway"

# Run migration
python -c "
import os
from sqlalchemy import create_engine, text

try:
    print('🔄 Connecting to database...')
    engine = create_engine(os.getenv('DATABASE_URL'))
    
    with engine.connect() as conn:
        # Check if username column exists
        result = conn.execute(text('''
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = \"users\" AND column_name = \"username\"
        '''))
        
        if result.fetchone():
            print('✅ Username column already exists')
        else:
            print('📝 Adding username column...')
            conn.execute(text('''
                ALTER TABLE users 
                ADD COLUMN username VARCHAR(50) UNIQUE NOT NULL DEFAULT \"temp_user\"
            '''))
            
            # Update existing users
            conn.execute(text('''
                UPDATE users 
                SET username = \"user_\" || id::text 
                WHERE username = \"temp_user\"
            '''))
            
            # Create index
            conn.execute(text('''
                CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username 
                ON users(username)
            '''))
            
            conn.commit()
            print('✅ Migration completed!')
            
except Exception as e:
    print(f'❌ Error: {e}')
    exit(1)
"

echo "✅ Migration script completed"
