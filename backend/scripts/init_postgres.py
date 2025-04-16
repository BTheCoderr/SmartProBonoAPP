import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def init_postgres():
    """Initialize PostgreSQL database for SmartProBono."""
    try:
        # On macOS with Homebrew, the default superuser is your system username
        current_user = os.environ.get('USER')
        
        # Connect to PostgreSQL server (on macOS, no password is required by default)
        conn = psycopg2.connect(
            host="localhost",
            user=current_user,
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'smartprobono_db'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('CREATE DATABASE smartprobono_db')
            print("Database 'smartprobono_db' created successfully")
        
        # Create user if it doesn't exist
        cursor.execute("SELECT 1 FROM pg_roles WHERE rolname='smartprobono'")
        exists = cursor.fetchone()
        if not exists:
            # Generate a secure password
            import secrets
            password = secrets.token_urlsafe(32)
            cursor.execute(f"CREATE USER smartprobono WITH PASSWORD '{password}'")
            print("User 'smartprobono' created successfully")
            
            # Save the credentials to .env file
            env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
            with open(env_path, 'r') as f:
                env_contents = f.read()
            
            # Update DATABASE_URL in .env
            new_db_url = f"postgresql://smartprobono:{password}@localhost:5432/smartprobono_db"
            if 'DATABASE_URL=' in env_contents:
                env_contents = '\n'.join(
                    line if not line.startswith('DATABASE_URL=') else f'DATABASE_URL={new_db_url}'
                    for line in env_contents.splitlines()
                )
            else:
                env_contents += f'\nDATABASE_URL={new_db_url}'
            
            with open(env_path, 'w') as f:
                f.write(env_contents)
            
            print(f"\nDatabase URL has been updated in .env file")
        
        # Grant privileges
        cursor.execute('GRANT ALL PRIVILEGES ON DATABASE smartprobono_db TO smartprobono')
        print("Privileges granted to user 'smartprobono'")
        
        cursor.close()
        conn.close()
        
        print("\nPostgreSQL database initialized successfully!")
        print("\nNext steps:")
        print("1. Run 'flask db upgrade' to create the tables")
        print("2. Run 'python init_db.py' to seed the database")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_postgres() 