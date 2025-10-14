# setup_database.py
import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker to generate fake data
fake = Faker()

# Connect to (or create) the SQLite database
conn = sqlite3.connect('sales_db.sqlite')
cursor = conn.cursor()

# --- Create clients table ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS clients (
    client_id TEXT PRIMARY KEY,
    client_name TEXT NOT NULL,
    industry TEXT
)
''')

# --- Create sales table ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    sale_id TEXT PRIMARY KEY,
    client_id TEXT,
    sale_amount REAL,
    sale_date TEXT,
    FOREIGN KEY (client_id) REFERENCES clients (client_id)
)
''')

# --- Populate clients table with 10 fake clients ---
clients_data = []
for _ in range(10):
    client_id = fake.uuid4()[:8]
    clients_data.append((client_id, fake.company(), fake.bs()))

cursor.executemany('INSERT OR IGNORE INTO clients (client_id, client_name, industry) VALUES (?, ?, ?)', clients_data)

# --- Populate sales table with 50 fake sales from the last 90 days ---
sales_data = []
client_ids = [row[0] for row in clients_data]
end_date = datetime.now()
start_date = end_date - timedelta(days=90)

for _ in range(50):
    sales_data.append((
        fake.uuid4()[:8],
        random.choice(client_ids),
        round(random.uniform(1000.0, 50000.0), 2),
        fake.date_between(start_date=start_date, end_date=end_date).isoformat()
    ))

cursor.executemany('INSERT OR IGNORE INTO sales (sale_id, client_id, sale_amount, sale_date) VALUES (?, ?, ?, ?)', sales_data)

# --- Commit changes and close the connection ---
conn.commit()
conn.close()

print("Database 'sales_db.sqlite' created and populated successfully!")