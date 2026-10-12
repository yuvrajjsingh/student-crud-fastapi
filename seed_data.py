"""Insert safe, fictional sample records for a quick demo. Run: python seed_data.py"""
from app.database import connect_db, initialize_database

SAMPLE_STUDENTS = [
    ("Aarav Sharma", "2005-08-17", "aarav@example.com", "9000000001", "B.Tech CSE", "Lucknow, Uttar Pradesh", "2024-08-01"),
    ("Diya Verma", "2006-02-11", "diya@example.com", "9000000002", "BCA", "Kanpur, Uttar Pradesh", "2024-08-01"),
    ("Kabir Singh", "2004-12-23", None, "9000000003", "B.Tech IT", "Prayagraj, Uttar Pradesh", "2023-08-01"),
]


def main() -> None:
    initialize_database()
    conn = connect_db()
    try:
        existing = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        if existing:
            print(f"Database already contains {existing} student(s); no sample data inserted.")
            return
        conn.executemany(
            """INSERT INTO students (name, date_of_birth, email, phone, course, address, enrollment_date)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            SAMPLE_STUDENTS,
        )
        conn.commit()
        print(f"Inserted {len(SAMPLE_STUDENTS)} fictional sample students.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
