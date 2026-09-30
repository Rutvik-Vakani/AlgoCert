import sqlite3


DATABASE = "database/algocert.db"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            certificate_id TEXT UNIQUE NOT NULL,
            student_name TEXT NOT NULL,
            course TEXT NOT NULL,
            certificate_hash TEXT NOT NULL,
            transaction_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add transaction_id to an existing database if the column is missing.
    cursor.execute("PRAGMA table_info(certificates)")
    columns = [row[1] for row in cursor.fetchall()]

    if "transaction_id" not in columns:
        cursor.execute("""
            ALTER TABLE certificates
            ADD COLUMN transaction_id TEXT
        """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("AlgoCert database updated successfully.")