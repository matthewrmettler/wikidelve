import sqlite3
import os

DATABASE_NAME = "test.db"

def create_database():
    with open(DATABASE_NAME, 'w') as f:
        pass

    creation_query = """
    CREATE TABLE entity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wiki_id INTEGER NOT NULL,
        name text NOT NULL
    );

    CREATE UNIQUE INDEX idx_entity_wiki_id
    ON entity (wiki_id);

    CREATE TABLE entity_associations (
        entity_id INTEGER PRIMARY KEY,
        associated_ids text NOT NULL
    );
    
    CREATE TABLE lists (
        list_id INTEGER PRIMARY KEY,
        list_name text NOT NULL
    );
    
    CREATE TABLE list_associations (
        list_id INTEGER PRIMARY KEY,
        entity_id text NOT NULL
    );
    
    
    """

    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(creation_query)
    conn.commit()
    conn.close()


def seed_database():
    pass


def test_database():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Do this instead
    t = ('RHAT',)
    c.execute('SELECT * FROM stocks WHERE symbol=?', t)
    print(c.fetchone())

    # Larger example that inserts many records at a time
    purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
                 ]
    c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)