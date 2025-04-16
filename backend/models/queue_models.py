import sqlite3
import os
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union, Any
import logging
from models.database import db, BaseModel
import uuid

# Try to import psycopg2 for PostgreSQL support
try:
    import psycopg2
    import psycopg2.extras
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    logging.warning("psycopg2 not available. PostgreSQL support disabled.")

class PriorityLevel(Enum):
    """Enum for case priority levels"""
    URGENT = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1

class QueueCase(BaseModel):
    """Model for cases in the priority queue"""
    __tablename__ = 'queue_cases'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = db.Column(db.String(36), db.ForeignKey('cases.id'), nullable=False)
    priority = db.Column(db.String(20), nullable=False)  # URGENT, HIGH, MEDIUM, LOW
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    situation_type = db.Column(db.String(50), nullable=False)
    metadata = db.Column(db.Text)  # JSON string
    assigned_lawyer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    assigned_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, assigned, completed

    # Relationships
    case = db.relationship('Case', backref=db.backref('queue_entries', lazy=True))
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('queued_cases', lazy=True))
    assigned_lawyer = db.relationship('User', foreign_keys=[assigned_lawyer_id], backref=db.backref('assigned_cases', lazy=True))

    def to_dict(self) -> Dict[str, Any]:
        """Convert queue case to dictionary"""
        return {
            'id': self.id,
            'case_id': self.case_id,
            'priority': self.priority,
            'timestamp': self.timestamp.isoformat(),
            'user_id': self.user_id,
            'situation_type': self.situation_type,
            'metadata': json.loads(self.metadata) if self.metadata else {},
            'assigned_lawyer_id': self.assigned_lawyer_id,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'status': self.status
        }

class QueueHistory(BaseModel):
    """Model for tracking queue history and metrics"""
    __tablename__ = 'queue_history'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_cases = db.Column(db.Integer, nullable=False)
    urgent_cases = db.Column(db.Integer, nullable=False)
    high_cases = db.Column(db.Integer, nullable=False)
    medium_cases = db.Column(db.Integer, nullable=False)
    low_cases = db.Column(db.Integer, nullable=False)
    average_wait_time = db.Column(db.Float)  # in minutes
    longest_wait_time = db.Column(db.Float)  # in minutes

    def to_dict(self) -> Dict[str, Any]:
        """Convert queue history to dictionary"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'total_cases': self.total_cases,
            'cases_by_priority': {
                'URGENT': self.urgent_cases,
                'HIGH': self.high_cases,
                'MEDIUM': self.medium_cases,
                'LOW': self.low_cases
            },
            'average_wait_time': self.average_wait_time,
            'longest_wait_time': self.longest_wait_time
        }

class DatabaseAdapter:
    """Base class for database adapters"""
    
    def __init__(self):
        self.conn = None
    
    def connect(self):
        """Connect to the database"""
        raise NotImplementedError
    
    def disconnect(self):
        """Disconnect from the database"""
        if self.conn:
            self.conn.close()
            self.conn = None

    def add_case(self, case_id, priority, timestamp, user_id, situation_type, metadata=None, assigned_lawyer_id=None):
        raise NotImplementedError
        
    def update_case_priority(self, case_id, new_priority):
        raise NotImplementedError
        
    def assign_case(self, case_id, lawyer_id):
        raise NotImplementedError
        
    def get_case(self, case_id):
        raise NotImplementedError
        
    def get_active_cases(self):
        raise NotImplementedError
        
    def record_queue_snapshot(self):
        raise NotImplementedError
        
    def get_queue_history(self, limit=100):
        raise NotImplementedError
        
    def get_lawyer_performance(self, lawyer_id=None):
        raise NotImplementedError
        
    def get_queue_stats(self):
        """Get current queue statistics"""
        raise NotImplementedError

class SQLiteAdapter(DatabaseAdapter):
    """SQLite implementation of the database adapter"""
    
    def __init__(self, db_path='data/queue.db'):
        """Initialize the database connection"""
        self.db_path = db_path
        self._ensure_db_directory()
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.initialize_tables()
        
    def _ensure_db_directory(self):
        """Ensure the directory for the database exists"""
        dir_path = os.path.dirname(self.db_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    def initialize_tables(self):
        """Initialize database tables if they don't exist"""
        try:
            cursor = self.conn.cursor()
            
            # Create queue_cases table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS queue_cases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    priority TEXT NOT NULL CHECK(priority IN ('URGENT', 'HIGH', 'MEDIUM', 'LOW')),
                    client_id INTEGER NOT NULL,
                    lawyer_id INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    active INTEGER DEFAULT 1,
                    resolution_time DATETIME,
                    FOREIGN KEY (client_id) REFERENCES users(id),
                    FOREIGN KEY (lawyer_id) REFERENCES users(id)
                )
            ''')
            
            # Drop and recreate queue_history table to reset any constraints issues
            cursor.execute('DROP TABLE IF EXISTS queue_history')
            
            # Create queue_history table with default values
            cursor.execute('''
                CREATE TABLE queue_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_cases INTEGER NOT NULL DEFAULT 0,
                    active_cases INTEGER NOT NULL DEFAULT 0,
                    resolved_cases INTEGER NOT NULL DEFAULT 0,
                    urgent_cases INTEGER NOT NULL DEFAULT 0,
                    avg_wait_time REAL NOT NULL DEFAULT 0.0,
                    avg_resolution_time REAL NOT NULL DEFAULT 0.0
                )
            ''')
            
            self.conn.commit()
            print("Database tables initialized successfully")
            
        except Exception as e:
            print(f"Error initializing tables: {str(e)}")
            self.conn.rollback()
    
    def add_case(self, case_id, priority, timestamp, user_id, situation_type, metadata=None, assigned_lawyer_id=None):
        """Add a case to the database"""
        cursor = self.conn.cursor()
        
        metadata_json = json.dumps(metadata) if metadata else '{}'
        
        cursor.execute('''
        INSERT INTO queue_cases 
        (case_id, priority, timestamp, user_id, situation_type, metadata, assigned_lawyer_id, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        ''', (
            case_id, 
            priority.name, 
            timestamp.isoformat(), 
            user_id, 
            situation_type, 
            metadata_json,
            assigned_lawyer_id
        ))
        
        self.conn.commit()
        
    def update_case_priority(self, case_id, new_priority):
        """Update a case's priority"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
        UPDATE queue_cases 
        SET priority = ?
        WHERE case_id = ? AND active = 1
        ''', (new_priority.name, case_id))
        
        self.conn.commit()
        return cursor.rowcount > 0
        
    def assign_case(self, case_id, lawyer_id):
        """Assign a case to a lawyer"""
        cursor = self.conn.cursor()
        
        # Update the case record
        cursor.execute('''
        UPDATE queue_cases 
        SET assigned_lawyer_id = ?, active = 0
        WHERE case_id = ? AND active = 1
        ''', (lawyer_id, case_id))
        
        if cursor.rowcount > 0:
            # Add to assignment table
            cursor.execute('''
            INSERT INTO case_assignments
            (case_id, lawyer_id, timestamp, status)
            VALUES (?, ?, ?, ?)
            ''', (
                case_id,
                lawyer_id,
                datetime.now().isoformat(),
                'assigned'
            ))
            
            self.conn.commit()
            return True
        
        self.conn.commit()
        return False
        
    def get_case(self, case_id):
        """Get a case by ID"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
        SELECT * FROM queue_cases 
        WHERE case_id = ?
        ''', (case_id,))
        
        case = cursor.fetchone()
        return dict(case) if case else None
        
    def get_active_cases(self):
        """Get all active cases in the queue"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
        SELECT * FROM queue_cases 
        WHERE active = 1
        ORDER BY 
            CASE priority
                WHEN 'URGENT' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            timestamp ASC
        ''')
        
        return [dict(case) for case in cursor.fetchall()]
        
    def record_queue_snapshot(self):
        """Record current queue statistics"""
        try:
            cursor = self.conn.cursor()
            
            # Get queue statistics using direct SQL aggregation
            cursor.execute('''
                INSERT INTO queue_history (
                    timestamp,
                    total_cases,
                    active_cases,
                    resolved_cases,
                    urgent_cases,
                    avg_wait_time,
                    avg_resolution_time
                )
                SELECT 
                    CURRENT_TIMESTAMP,
                    COALESCE(COUNT(*), 0) as total_cases,
                    COALESCE(SUM(CASE WHEN active = 1 THEN 1 ELSE 0 END), 0) as active_cases,
                    COALESCE(SUM(CASE WHEN active = 0 THEN 1 ELSE 0 END), 0) as resolved_cases,
                    COALESCE(SUM(CASE WHEN priority = 'URGENT' AND active = 1 THEN 1 ELSE 0 END), 0) as urgent_cases,
                    COALESCE(
                        AVG(CASE 
                            WHEN active = 1 THEN 
                                ROUND((JULIANDAY('now') - JULIANDAY(timestamp)) * 24 * 60)
                            ELSE NULL 
                        END
                    ), 0) as avg_wait_time,
                    COALESCE(
                        AVG(CASE 
                            WHEN active = 0 AND resolution_time IS NOT NULL THEN 
                                ROUND((JULIANDAY(resolution_time) - JULIANDAY(timestamp)) * 24 * 60)
                            ELSE NULL 
                        END
                    ), 0) as avg_resolution_time
                FROM queue_cases
            ''')
            
            self.conn.commit()
            return True
            
        except Exception as e:
            self.conn.rollback()
            print(f"Error recording queue snapshot: {str(e)}")
            return False
        
    def get_queue_history(self, limit=100):
        """Get historical queue snapshots"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
        SELECT * FROM queue_history
        ORDER BY timestamp DESC
        LIMIT ?
        ''', (limit,))
        
        return [dict(record) for record in cursor.fetchall()]
        
    def get_lawyer_performance(self, lawyer_id=None):
        """Get performance metrics for lawyers"""
        cursor = self.conn.cursor()
        
        if lawyer_id:
            cursor.execute('''
            SELECT 
                lawyer_id,
                COUNT(*) as total_cases,
                AVG(
                    CASE 
                        WHEN resolution_time IS NOT NULL 
                        THEN (julianday(resolution_time) - julianday(timestamp)) * 24 * 60 
                        ELSE NULL 
                    END
                ) as avg_resolution_minutes
            FROM case_assignments
            WHERE lawyer_id = ?
            GROUP BY lawyer_id
            ''', (lawyer_id,))
        else:
            cursor.execute('''
            SELECT 
                lawyer_id,
                COUNT(*) as total_cases,
                AVG(
                    CASE 
                        WHEN resolution_time IS NOT NULL 
                        THEN (julianday(resolution_time) - julianday(timestamp)) * 24 * 60 
                        ELSE NULL 
                    END
                ) as avg_resolution_minutes
            FROM case_assignments
            GROUP BY lawyer_id
            ''')
            
        return [dict(record) for record in cursor.fetchall()]
        
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def get_queue_stats(self):
        """Get current queue statistics"""
        try:
            cursor = self.conn.cursor()
            
            # Get total cases
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN priority = 'URGENT' THEN 1 ELSE 0 END) as urgent,
                    SUM(CASE WHEN priority = 'HIGH' THEN 1 ELSE 0 END) as high,
                    SUM(CASE WHEN priority = 'MEDIUM' THEN 1 ELSE 0 END) as medium,
                    SUM(CASE WHEN priority = 'LOW' THEN 1 ELSE 0 END) as low,
                    AVG(JULIANDAY('now') - JULIANDAY(timestamp)) * 24 as avg_wait
                FROM queue_cases 
                WHERE active = 1
            ''')
            
            row = cursor.fetchone()
            if row:
                return {
                    'total_cases': row[0] or 0,
                    'urgent_cases': row[1] or 0,
                    'high_priority_cases': row[2] or 0,
                    'medium_priority_cases': row[3] or 0,
                    'low_priority_cases': row[4] or 0,
                    'avg_wait_time': round(row[5] or 0, 2)
                }
            
            return {
                'total_cases': 0,
                'urgent_cases': 0,
                'high_priority_cases': 0,
                'medium_priority_cases': 0,
                'low_priority_cases': 0,
                'avg_wait_time': 0
            }
            
        except Exception as e:
            print(f"Error getting queue stats: {str(e)}")
            return {
                'total_cases': 0,
                'urgent_cases': 0,
                'high_priority_cases': 0,
                'medium_priority_cases': 0,
                'low_priority_cases': 0,
                'avg_wait_time': 0
            }

class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL implementation of the database adapter"""
    
    def __init__(self, connection_params=None):
        """Initialize the database connection"""
        if not POSTGRES_AVAILABLE:
            raise ImportError("psycopg2 is not installed. Cannot use PostgreSQL adapter.")
            
        # Default connection parameters
        if connection_params is None:
            connection_params = {}
            
            # Get connection parameters from environment variables
            db_name = os.environ.get('POSTGRES_DB', 'smartprobono')
            db_user = os.environ.get('POSTGRES_USER', 'postgres')
            db_password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
            db_host = os.environ.get('POSTGRES_HOST', 'localhost')
            db_port = os.environ.get('POSTGRES_PORT', '5432')
            
            # Build connection string
            self.connection_string = f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"
        else:
            # Use provided connection parameters
            self.connection_string = " ".join([f"{k}={v}" for k, v in connection_params.items()])
        
        # Create the connection
        self.conn = psycopg2.connect(self.connection_string)
        self.initialize_tables()
    
    def initialize_tables(self):
        """Create the necessary tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Create cases table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS queue_cases (
            case_id TEXT PRIMARY KEY,
            priority TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            user_id TEXT NOT NULL,
            situation_type TEXT NOT NULL,
            metadata JSONB,
            assigned_lawyer_id TEXT,
            active BOOLEAN DEFAULT TRUE
        );
        ''')
        
        # Create queue history table with updated schema
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS queue_history (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            total_cases INTEGER NOT NULL DEFAULT 0,
            urgent_cases INTEGER NOT NULL DEFAULT 0,
            high_priority_cases INTEGER NOT NULL DEFAULT 0,
            medium_priority_cases INTEGER NOT NULL DEFAULT 0,
            low_priority_cases INTEGER NOT NULL DEFAULT 0,
            avg_wait_time REAL NOT NULL DEFAULT 0
        );
        ''')
        
        # Create case assignment table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS case_assignments (
            id SERIAL PRIMARY KEY,
            case_id TEXT NOT NULL,
            lawyer_id TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            status TEXT NOT NULL,
            resolution_time TIMESTAMP,
            FOREIGN KEY (case_id) REFERENCES queue_cases(case_id)
        );
        ''')
        
        # Create index for faster queries
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_queue_cases_active_priority 
        ON queue_cases(active, priority);
        ''')
        
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_case_assignments_lawyer 
        ON case_assignments(lawyer_id);
        ''')
        
        self.conn.commit()
    
    def add_case(self, case_id, priority, timestamp, user_id, situation_type, metadata=None, assigned_lawyer_id=None):
        """Add a case to the database"""
        cursor = self.conn.cursor()
        
        metadata_json = json.dumps(metadata) if metadata else '{}'
        
        cursor.execute('''
        INSERT INTO queue_cases 
        (case_id, priority, timestamp, user_id, situation_type, metadata, assigned_lawyer_id, active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
        ''', (
            case_id, 
            priority.name, 
            timestamp, 
            user_id, 
            situation_type, 
            metadata_json,
            assigned_lawyer_id
        ))
        
        self.conn.commit()
        
    def update_case_priority(self, case_id, new_priority):
        """Update a case's priority"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
        UPDATE queue_cases 
        SET priority = %s
        WHERE case_id = %s AND active = TRUE
        ''', (new_priority.name, case_id))
        
        self.conn.commit()
        return cursor.rowcount > 0
        
    def assign_case(self, case_id, lawyer_id):
        """Assign a case to a lawyer"""
        cursor = self.conn.cursor()
        
        # Update the case record
        cursor.execute('''
        UPDATE queue_cases 
        SET assigned_lawyer_id = %s, active = FALSE
        WHERE case_id = %s AND active = TRUE
        ''', (lawyer_id, case_id))
        
        if cursor.rowcount > 0:
            # Add to assignment table
            cursor.execute('''
            INSERT INTO case_assignments
            (case_id, lawyer_id, timestamp, status)
            VALUES (%s, %s, %s, %s)
            ''', (
                case_id,
                lawyer_id,
                datetime.now(),
                'assigned'
            ))
            
            self.conn.commit()
            return True
        
        self.conn.commit()
        return False
        
    def get_case(self, case_id):
        """Get a case by ID"""
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cursor.execute('''
        SELECT * FROM queue_cases 
        WHERE case_id = %s
        ''', (case_id,))
        
        case = cursor.fetchone()
        return dict(case) if case else None
        
    def get_active_cases(self):
        """Get all active cases in the queue"""
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cursor.execute('''
        SELECT * FROM queue_cases 
        WHERE active = TRUE
        ORDER BY 
            CASE priority
                WHEN 'URGENT' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            timestamp ASC
        ''')
        
        return [dict(case) for case in cursor.fetchall()]
        
    def record_queue_snapshot(self):
        """Record current queue statistics"""
        try:
            cursor = self.conn.cursor()
            
            # Get queue statistics using direct SQL aggregation
            cursor.execute('''
                INSERT INTO queue_history (
                    timestamp,
                    total_cases,
                    active_cases,
                    resolved_cases,
                    urgent_cases,
                    avg_wait_time,
                    avg_resolution_time
                )
                SELECT 
                    CURRENT_TIMESTAMP,
                    COALESCE(COUNT(*), 0) as total_cases,
                    COALESCE(SUM(CASE WHEN active = 1 THEN 1 ELSE 0 END), 0) as active_cases,
                    COALESCE(SUM(CASE WHEN active = 0 THEN 1 ELSE 0 END), 0) as resolved_cases,
                    COALESCE(SUM(CASE WHEN priority = 'URGENT' AND active = 1 THEN 1 ELSE 0 END), 0) as urgent_cases,
                    COALESCE(
                        AVG(CASE 
                            WHEN active = 1 THEN 
                                ROUND((JULIANDAY('now') - JULIANDAY(timestamp)) * 24 * 60)
                            ELSE NULL 
                        END
                    ), 0) as avg_wait_time,
                    COALESCE(
                        AVG(CASE 
                            WHEN active = 0 AND resolution_time IS NOT NULL THEN 
                                ROUND((JULIANDAY(resolution_time) - JULIANDAY(timestamp)) * 24 * 60)
                            ELSE NULL 
                        END
                    ), 0) as avg_resolution_time
                FROM queue_cases
            ''')
            
            self.conn.commit()
            return True
            
        except Exception as e:
            self.conn.rollback()
            print(f"Error recording queue snapshot: {str(e)}")
            return False
        
    def get_queue_history(self, limit=100):
        """Get historical queue snapshots"""
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cursor.execute('''
        SELECT * FROM queue_history
        ORDER BY timestamp DESC
        LIMIT %s
        ''', (limit,))
        
        return [dict(record) for record in cursor.fetchall()]
        
    def get_lawyer_performance(self, lawyer_id=None):
        """Get performance metrics for lawyers"""
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        if lawyer_id:
            cursor.execute('''
            SELECT 
                lawyer_id,
                COUNT(*) as total_cases,
                AVG(
                    CASE 
                        WHEN resolution_time IS NOT NULL 
                        THEN EXTRACT(EPOCH FROM (resolution_time - timestamp))/60
                        ELSE NULL 
                    END
                ) as avg_resolution_minutes
            FROM case_assignments
            WHERE lawyer_id = %s
            GROUP BY lawyer_id
            ''', (lawyer_id,))
        else:
            cursor.execute('''
            SELECT 
                lawyer_id,
                COUNT(*) as total_cases,
                AVG(
                    CASE 
                        WHEN resolution_time IS NOT NULL 
                        THEN EXTRACT(EPOCH FROM (resolution_time - timestamp))/60
                        ELSE NULL 
                    END
                ) as avg_resolution_minutes
            FROM case_assignments
            GROUP BY lawyer_id
            ''')
            
        return [dict(record) for record in cursor.fetchall()]
        
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def get_queue_stats(self):
        """Get current queue statistics"""
        try:
            cursor = self.conn.cursor()
            
            # Get total cases
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN priority = 'URGENT' THEN 1 ELSE 0 END) as urgent,
                    SUM(CASE WHEN priority = 'HIGH' THEN 1 ELSE 0 END) as high,
                    SUM(CASE WHEN priority = 'MEDIUM' THEN 1 ELSE 0 END) as medium,
                    SUM(CASE WHEN priority = 'LOW' THEN 1 ELSE 0 END) as low,
                    AVG(JULIANDAY('now') - JULIANDAY(timestamp)) * 24 as avg_wait
                FROM queue_cases 
                WHERE active = 1
            ''')
            
            row = cursor.fetchone()
            if row:
                return {
                    'total_cases': row[0] or 0,
                    'urgent_cases': row[1] or 0,
                    'high_priority_cases': row[2] or 0,
                    'medium_priority_cases': row[3] or 0,
                    'low_priority_cases': row[4] or 0,
                    'avg_wait_time': round(row[5] or 0, 2)
                }
            
            return {
                'total_cases': 0,
                'urgent_cases': 0,
                'high_priority_cases': 0,
                'medium_priority_cases': 0,
                'low_priority_cases': 0,
                'avg_wait_time': 0
            }
            
        except Exception as e:
            print(f"Error getting queue stats: {str(e)}")
            return {
                'total_cases': 0,
                'urgent_cases': 0,
                'high_priority_cases': 0,
                'medium_priority_cases': 0,
                'low_priority_cases': 0,
                'avg_wait_time': 0
            }

class QueueDatabase:
    """Database facade that selects the appropriate adapter based on configuration"""
    
    def __init__(self):
        """Initialize the database with the appropriate adapter"""
        db_type = os.environ.get('DB_TYPE', 'sqlite').lower()
        
        if db_type == 'postgres' or db_type == 'postgresql':
            if POSTGRES_AVAILABLE:
                self.adapter = PostgreSQLAdapter()
                logging.info("Using PostgreSQL database")
            else:
                logging.warning("PostgreSQL requested but psycopg2 not available. Falling back to SQLite.")
                self.adapter = SQLiteAdapter()
        else:
            self.adapter = SQLiteAdapter()
            logging.info("Using SQLite database")
    
    def add_case(self, case_id, priority, timestamp, user_id, situation_type, metadata=None, assigned_lawyer_id=None):
        return self.adapter.add_case(case_id, priority, timestamp, user_id, situation_type, metadata, assigned_lawyer_id)
    
    def update_case_priority(self, case_id, new_priority):
        return self.adapter.update_case_priority(case_id, new_priority)
    
    def assign_case(self, case_id, lawyer_id):
        return self.adapter.assign_case(case_id, lawyer_id)
    
    def get_case(self, case_id):
        return self.adapter.get_case(case_id)
    
    def get_active_cases(self):
        return self.adapter.get_active_cases()
    
    def record_queue_snapshot(self):
        return self.adapter.record_queue_snapshot()
    
    def get_queue_history(self, limit=100):
        return self.adapter.get_queue_history(limit)
    
    def get_lawyer_performance(self, lawyer_id=None):
        return self.adapter.get_lawyer_performance(lawyer_id)
    
    def close(self):
        return self.adapter.close()

# Create global instance
queue_db = QueueDatabase() 