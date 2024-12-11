import pandas as pd
import sqlite3
from pathlib import Path

class EnergyDatabase:
    def __init__(self, db_name='energy_consumption.db'):
        self.db_path = Path(db_name)
        self.conn = None
        self.cursor = None
        
    def initialize(self):
        """Initialize database connection and table structure"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._setup_tables()
        self._initialize_lookup_data()
        
    def _setup_tables(self):
        """Set up database table structure"""
        # Base tables
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS location_data (
                loc_id INTEGER PRIMARY KEY,
                location_name TEXT UNIQUE NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS sector_data (
                sector_id INTEGER PRIMARY KEY,
                sector_name TEXT UNIQUE NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS fuel_types (
                fuel_id INTEGER PRIMARY KEY,
                fuel_name TEXT UNIQUE NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS commercial_usage (
                usage_id INTEGER PRIMARY KEY,
                location_ref INTEGER,
                sector_ref INTEGER,
                fuel_ref INTEGER,
                usage_amount REAL,
                FOREIGN KEY (location_ref) REFERENCES location_data(loc_id),
                FOREIGN KEY (sector_ref) REFERENCES sector_data(sector_id),
                FOREIGN KEY (fuel_ref) REFERENCES fuel_types(fuel_id)
            );
            
            CREATE TABLE IF NOT EXISTS residential_usage (
                usage_id INTEGER PRIMARY KEY,
                location_ref INTEGER,
                sector_ref INTEGER,
                fuel_ref INTEGER,
                usage_amount REAL,
                FOREIGN KEY (location_ref) REFERENCES location_data(loc_id),
                FOREIGN KEY (sector_ref) REFERENCES sector_data(sector_id),
                FOREIGN KEY (fuel_ref) REFERENCES fuel_types(fuel_id)
            );
        ''')
        
    def _initialize_lookup_data(self):
        """Initialize base data"""
        try:
            # Sector data
            sectors = [('Commercial',), ('Residential',)]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO sector_data (sector_name) VALUES (?)", 
                sectors
            )
            
            # Fuel type data
            fuels = ['Electricity', 'Gas', 'Coal', 'Oil', 'Bioenergy and waste*']
            for fuel in fuels:
                self.cursor.execute(
                    "INSERT OR IGNORE INTO fuel_types (fuel_name) VALUES (?)", 
                    (fuel,)
                )
            
            self.conn.commit()
        except Exception as e:
            print(f"Error initializing base data: {e}")
            raise
        
    def process_data(self):
        """Process CSV data and store in database"""
        # Read data files, set first column as index
        commercial = pd.read_csv('q2-IC.csv', index_col=0)
        residential = pd.read_csv('q2-domestic.csv', index_col=0)
        
        # Process location data
        locations = [(name,) for name in commercial.index]
        self.cursor.executemany(
            "INSERT OR IGNORE INTO location_data (location_name) VALUES (?)",
            locations
        )
        
        # Get reference IDs
        commercial_id = self.cursor.execute(
            "SELECT sector_id FROM sector_data WHERE sector_name='Commercial'"
        ).fetchone()[0]
        residential_id = self.cursor.execute(
            "SELECT sector_id FROM sector_data WHERE sector_name='Residential'"
        ).fetchone()[0]
        
        # Batch insert data
        self._insert_consumption_data(commercial, commercial_id, 'commercial_usage')
        self._insert_consumption_data(residential, residential_id, 'residential_usage')
        
    def _insert_consumption_data(self, df, sector_id, table_name):
        """Insert consumption data"""
        try:
            for location in df.index:
                # Get location_id
                loc_result = self.cursor.execute(
                    "SELECT loc_id FROM location_data WHERE location_name=?", 
                    (location,)
                ).fetchone()
                
                if not loc_result:
                    print(f"Warning: Location not found {location}")
                    continue
                    
                loc_id = loc_result[0]
                
                for fuel in df.columns:
                    # Get fuel_id
                    fuel_result = self.cursor.execute(
                        "SELECT fuel_id FROM fuel_types WHERE fuel_name=?", 
                        (fuel,)
                    ).fetchone()
                    
                    if not fuel_result:
                        print(f"Warning: Fuel type not found {fuel}")
                        continue
                        
                    fuel_id = fuel_result[0]
                    
                    # Insert data
                    self.cursor.execute(f'''
                        INSERT INTO {table_name} 
                        (location_ref, sector_ref, fuel_ref, usage_amount)
                        VALUES (?, ?, ?, ?)
                    ''', (loc_id, sector_id, fuel_id, df.loc[location, fuel]))
            
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting data: {e}")
            self.conn.rollback()
            raise
        
    def display_info(self):
        """Display database information and all data"""
        if self.db_path.exists():
            print(f"Database location: {self.db_path.absolute()}")
            print(f"Database size: {self.db_path.stat().st_size / 1024:.1f} KB")
            
            # Display record counts
            for table in ['commercial_usage', 'residential_usage']:
                count = self.cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                print(f"{table} record count: {count}")
                
                # Print all data
                print(f"\n{table} data:")
                rows = self.cursor.execute(f"""
                    SELECT l.location_name, s.sector_name, f.fuel_name, u.usage_amount 
                    FROM {table} u
                    JOIN location_data l ON u.location_ref = l.loc_id
                    JOIN sector_data s ON u.sector_ref = s.sector_id 
                    JOIN fuel_types f ON u.fuel_ref = f.fuel_id
                    ORDER BY l.location_name, f.fuel_name
                """).fetchall()
                
                for row in rows:
                    print(f"Location: {row[0]}, Sector: {row[1]}, Fuel Type: {row[2]}, Usage: {row[3]}")
                print()
        else:
            print("Database file not found")
            
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

def main():
    db = EnergyDatabase()
    db.initialize()
    db.process_data()
    db.display_info()
    db.close()

if __name__ == "__main__":
    main()