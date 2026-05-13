from faker import Faker
import random
import psycopg2

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    database="hr_db",
    user="postgres",
    password="YOUR_PASSWORD"
)

cur = conn.cursor()

departments = [
    "HR", "IT", "Finance", "Marketing",
    "Sales", "Operations"
]

designations = [
    "Manager", "Analyst", "Engineer",
    "Executive", "Intern"
]

for _ in range(11000):

    name = fake.name()
    email = fake.email()

    department = random.choice(departments)
    designation = random.choice(designations)

    attendance = round(random.uniform(60, 100), 2)

    salary = random.randint(25000, 120000)

    joining_date = fake.date_between(
        start_date='-5y',
        end_date='-1d'
    )

    cur.execute("""
        INSERT INTO employees (
            full_name,
            email,
            department,
            designation,
            attendance_percentage,
            salary,
            joining_date
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        name,
        email,
        department,
        designation,
        attendance,
        salary,
        joining_date
    ))

conn.commit()

cur.close()
conn.close()

print("11000 fake employee records inserted!")