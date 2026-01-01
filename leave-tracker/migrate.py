"""
One-time database migration to add day_type column
This is safe to run multiple times - it checks if column exists first
"""
import sqlite3
import os

def migrate():
    """Add day_type column to leave_requests table if it doesn't exist"""
    
    db_path = 'leaves.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("ℹ️  Database doesn't exist yet - will be created by init_db.py")
        return
    
    print("🔍 Checking database for migration needs...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check current columns in leave_requests table
        cursor.execute("PRAGMA table_info(leave_requests)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"   Current columns: {', '.join(columns)}")
        
        if 'day_type' not in columns:
            print("➕ Adding day_type column...")
            cursor.execute("""
                ALTER TABLE leave_requests 
                ADD COLUMN day_type VARCHAR(20) DEFAULT 'Full Day'
            """)
            conn.commit()
            print("✅ day_type column added successfully!")
        else:
            print("✅ day_type column already exists - no migration needed")
            
    except Exception as e:
        print(f"❌ Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
