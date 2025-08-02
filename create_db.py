import sqlite3

# Create or connect to DB
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Create student table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    fingerprint_id TEXT UNIQUE NOT NULL
)
""")

# Create attendance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

# Insert sample students
students = [
    ('Aakash', 'fp001'),
    ('Neha', 'fp002'),
    ('Ravi', 'fp003')
]

for student in students:
    try:
        cursor.execute("INSERT INTO students (name, fingerprint_id) VALUES (?, ?)", student)
    except:
        pass  # Ignore duplicates

conn.commit()
conn.close()
