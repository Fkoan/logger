import sqlite3
import csv

conn = sqlite3.connect("students.db")
c = conn.cursor()

# Create table matching your CSV structure
c.execute("""CREATE TABLE IF NOT EXISTS students(
    matric TEXT PRIMARY KEY,
    name TEXT,
    department TEXT
)""")

# Read from CSV and insert
with open(r"C:\Users\nueltaj\Programming\logger\attendance.csv", "r", encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header row
    
    for row in csv_reader:
        # Your CSV: [S/N, Name, Department, Matric_no, empty]
        # We want: [Matric_no, Name, Department]
        if len(row) >= 4 and row[3].strip():  # Make sure matric exists
            serial = row[0]
            name = row[1].strip()
            department = row[2].strip()
            matric = row[3].strip()
            
            c.execute("INSERT OR IGNORE INTO students VALUES(?,?,?)", 
                     (matric, name, department))

conn.commit()
conn.close()

print("Student database created successfully!")
print("Students imported from attendance.csv")