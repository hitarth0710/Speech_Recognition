import sqlite3
import os
import sys

def run_migration():
    """Add display_name column to recordings table"""
    
    # Get the database path from the environment or use default
    db_path = os.environ.get('DEV_DATABASE_URL', 'sqlite:///dev.db')
    
    # Strip sqlite:/// prefix if present
    if db_path.startswith('sqlite:///'):
        db_path = db_path[10:]
    
    # Get absolute path if it's not already
    if not os.path.isabs(db_path):
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_path)
    
    print(f"Connecting to database: {db_path}")
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the display_name column already exists
        cursor.execute("PRAGMA table_info(recordings)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'display_name' not in columns:
            print("Adding 'display_name' column to recordings table...")
            cursor.execute("ALTER TABLE recordings ADD COLUMN display_name TEXT")
            
            # Initialize display_name with original_filename for existing records
            cursor.execute("UPDATE recordings SET display_name = original_filename WHERE original_filename IS NOT NULL")
            
            conn.commit()
            print("Migration successful!")
        else:
            print("Column 'display_name' already exists. No changes needed.")
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False
    finally:
        if conn:
            conn.close()
    
    return True

if __name__ == "__main__":
    if run_migration():
        print("Database migration completed successfully.")
    else:
        print("Database migration failed.")
        sys.exit(1)