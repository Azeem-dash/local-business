"""
SQLite database for storing businesses, demos, and outreach tracking.
"""
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
from config import Config

try:
    import libsql_experimental as libsql
    HAS_LIBSQL = True
except ImportError:
    HAS_LIBSQL = False


class Database:
    """Manage business leads database."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establish database connection."""
        if Config.TURSO_DATABASE_URL and Config.TURSO_AUTH_TOKEN:
            if not HAS_LIBSQL:
                print("⚠️ TURSO_DATABASE_URL set but 'libsql' package not found. Falling back to local SQLite.")
                self.conn = sqlite3.connect(self.db_path)
                self.conn.row_factory = sqlite3.Row  # Enable column access by name
            else:
                print(f"☁️ Connecting to Turso Cloud Database: {Config.TURSO_DATABASE_URL}")
                self.conn = libsql.connect(
                    database=Config.TURSO_DATABASE_URL,
                    auth_token=Config.TURSO_AUTH_TOKEN
                )
                # libsql doesn't support row_factory, but returns dict-like rows by default
        else:
            print(f"🏠 Connecting to local database: {self.db_path}")
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            
        self.cursor = self.conn.cursor()
    
    def _row_to_dict(self, row) -> Dict:
        """Convert database row to dictionary (works for both sqlite3.Row and libsql rows)."""
        if row is None:
            return None
        # libsql rows are already dict-like, sqlite3.Row needs conversion
        if isinstance(row, dict):
            return row  # libsql row
        else:
            return dict(row)  # sqlite3.Row

    
    def _create_tables(self):
        """Create database schema if not exists."""
        
        # Searches table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                location TEXT,
                engine TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Businesses table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                location TEXT,
                address TEXT,
                phone TEXT,
                rating REAL,
                review_count INTEGER,
                website TEXT,
                website_status TEXT,
                google_maps_url TEXT,
                lead_score INTEGER,
                is_valid_lead BOOLEAN,
                validation_notes TEXT,
                owner_name TEXT,
                last_review_date TEXT,
                outreach_stage TEXT DEFAULT 'lead',
                review_snippets TEXT,
                discovered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source TEXT DEFAULT 'google_maps',
                search_id INTEGER,
                notes TEXT,
                FOREIGN KEY (search_id) REFERENCES searches(id)
            )
        ''')
        
        # Add search_id column if it doesn't exist (for existing databases)
        try:
            self.cursor.execute('ALTER TABLE businesses ADD COLUMN search_id INTEGER REFERENCES searches(id)')
        except (sqlite3.OperationalError, ValueError):
            pass  # Column already exists
        
        # Demos table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS demos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_id INTEGER NOT NULL,
                template_used TEXT,
                demo_url TEXT,
                local_path TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (business_id) REFERENCES businesses(id)
            )
        ''')
        
        # Outreach tracking table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS outreach (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_id INTEGER NOT NULL,
                contact_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                method TEXT,
                status TEXT,
                response_received BOOLEAN DEFAULT 0,
                notes TEXT,
                FOREIGN KEY (business_id) REFERENCES businesses(id)
            )
        ''')
        
        self.conn.commit()
    
    def add_business(self, business: Dict) -> int:
        """Add a new business to the database."""
        self.cursor.execute('''
            INSERT INTO businesses 
            (name, category, location, address, phone, rating, review_count, 
             website, website_status, google_maps_url, lead_score, is_valid_lead, 
             validation_notes, owner_name, last_review_date, outreach_stage, 
             review_snippets, source, search_id, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            business.get('name'),
            business.get('category'),
            business.get('location'),
            business.get('address'),
            business.get('phone'),
            business.get('rating'),
            business.get('review_count'),
            business.get('website'),
            business.get('website_status'),
            business.get('google_maps_url'),
            business.get('lead_score', 0),
            business.get('is_valid_lead', 0),
            business.get('validation_notes', ''),
            business.get('owner_name'),
            business.get('last_review_date'),
            business.get('outreach_stage', 'lead'),
            business.get('review_snippets'),
            business.get('source', 'google_maps'),
            business.get('search_id'),
            business.get('notes', '')
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_business(self, business_id: int) -> Optional[Dict]:
        """Get a business by ID."""
        self.cursor.execute('SELECT * FROM businesses WHERE id = ?', (business_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def create_search(self, query: str, location: str, engine: str) -> int:
        """Create a new search record and return its ID."""
        self.cursor.execute('''
            INSERT INTO searches (query, location, engine)
            VALUES (?, ?, ?)
        ''', (query, location, engine))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_recent_searches(self, limit: int = 10) -> List[Dict]:
        """Get recent search history."""
        self.cursor.execute('''
            SELECT * FROM searches ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        return [self._row_to_dict(row) for row in self.cursor.fetchall()]

    def get_leads_by_search(self, search_id: int) -> List[Dict]:
        """Get all leads associated with a search ID."""
        self.cursor.execute('''
            SELECT * FROM businesses WHERE search_id = ? ORDER BY lead_score DESC
        ''', (search_id,))
        return [self._row_to_dict(row) for row in self.cursor.fetchall()]
    
    def get_all_businesses(self, limit: int = None) -> List[Dict]:
        """Get all businesses, optionally limited."""
        query = 'SELECT * FROM businesses ORDER BY lead_score DESC, discovered_date DESC'
        if limit:
            query += f' LIMIT {limit}'
        
        self.cursor.execute(query)
        return [self._row_to_dict(row) for row in self.cursor.fetchall()]
    
    def get_businesses_by_status(self, website_status: str) -> List[Dict]:
        """Get businesses by website status."""
        self.cursor.execute(
            'SELECT * FROM businesses WHERE website_status = ? ORDER BY lead_score DESC',
            (website_status,)
        )
        return [self._row_to_dict(row) for row in self.cursor.fetchall()]
    
    def add_demo(self, business_id: int, template: str, demo_url: str = None, local_path: str = None) -> int:
        """Record a generated demo."""
        self.cursor.execute('''
            INSERT INTO demos (business_id, template_used, demo_url, local_path)
            VALUES (?, ?, ?, ?)
        ''', (business_id, template, demo_url, local_path))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def add_outreach(self, business_id: int, method: str, notes: str = '') -> int:
        """Log an outreach attempt."""
        self.cursor.execute('''
            INSERT INTO outreach (business_id, method, status, notes)
            VALUES (?, ?, ?, ?)
        ''', (business_id, method, 'sent', notes))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_outreach_response(self, outreach_id: int, status: str, notes: str = ''):
        """Update outreach with response information."""
        self.cursor.execute('''
            UPDATE outreach 
            SET status = ?, response_received = 1, notes = ?
            WHERE id = ?
        ''', (status, notes, outreach_id))
        self.conn.commit()
    
    def get_outreach_history(self, business_id: int) -> List[Dict]:
        """Get all outreach attempts for a business."""
        self.cursor.execute(
            'SELECT * FROM outreach WHERE business_id = ? ORDER BY contact_date DESC',
            (business_id,)
        )
        return [self._row_to_dict(row) for row in self.cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """Get database statistics."""
        stats = {}
        
        # Total businesses
        self.cursor.execute('SELECT COUNT(*) as count FROM businesses')
        stats['total_businesses'] = self.cursor.fetchone()['count']
        
        # By website status
        self.cursor.execute('''
            SELECT website_status, COUNT(*) as count 
            FROM businesses 
            GROUP BY website_status
        ''')
        stats['by_status'] = {row['website_status']: row['count'] for row in self.cursor.fetchall()}
        
        # Demos created
        self.cursor.execute('SELECT COUNT(*) as count FROM demos')
        stats['demos_created'] = self.cursor.fetchone()['count']
        
        # Outreach attempts
        self.cursor.execute('SELECT COUNT(*) as count FROM outreach')
        stats['outreach_attempts'] = self.cursor.fetchone()['count']
        
        # Responses received
        self.cursor.execute('SELECT COUNT(*) as count FROM outreach WHERE response_received = 1')
        stats['responses_received'] = self.cursor.fetchone()['count']
        
        return stats
    
    def clear_test_data(self):
        """Clear all data (for testing only)."""
        self.cursor.execute('DELETE FROM outreach')
        self.cursor.execute('DELETE FROM demos')
        self.cursor.execute('DELETE FROM businesses')
        self.conn.commit()
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    # Test the database
    print("Testing database...")
    
    with Database() as db:
        # Add test business
        test_business = {
            'name': 'Test Restaurant',
            'category': 'restaurant',
            'location': 'Manchester UK',
            'address': '123 Test St',
            'phone': '+44 1234 567890',
            'rating': 4.5,
            'review_count': 50,
            'website': None,
            'website_status': 'no_website',
            'google_maps_url': 'https://maps.google.com/test',
            'lead_score': 85
        }
        
        business_id = db.add_business(test_business)
        print(f"✅ Added test business with ID: {business_id}")
        
        # Get statistics
        stats = db.get_statistics()
        print(f"📊 Statistics: {stats}")
        
        # Clean up
        db.clear_test_data()
        print("🧹 Cleaned up test data")
    
    print("✅ Database test complete!")
