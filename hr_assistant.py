import psycopg2
import ollama
import re

conn = psycopg2.connect(
    host="localhost",
    database="hr_db",
    user="postgres",
    password="YOUR_PASSWORD"
)

cur = conn.cursor()

print("\nHR Assistant Started")
print("Type 'exit' to stop\n")

while True:

    query = input("Ask HR Query: ").lower()

    if query == "exit":
        print("\nHR Assistant Stopped")
        break

    # -------------------------
    # ATTENDANCE BELOW QUERY
    # -------------------------

    if "attendance below" in query:

        number = re.search(r'\d+', query)

        if number:

            limit = number.group()

            cur.execute("""
                SELECT employee_id,
                       full_name,
                       attendance_percentage
                FROM employees
                WHERE attendance_percentage < %s
                LIMIT 10
            """, (limit,))

            employees = cur.fetchall()

            if employees:

                data = ""

                for emp in employees:
                    data += f"""
                    Employee ID: {emp[0]}
                    Name: {emp[1]}
                    Attendance: {emp[2]}%

                    """

                response = ollama.chat(
                    model='gemma:2b',
                    messages=[
                        {
                            'role': 'user',
                            'content': f"""
                            HR Query:
                            {query}

                            Employee Data:
                            {data}

                            Summarize professionally.
                            """
                        }
                    ]
                )

                print("\nAI RESPONSE:\n")
                print(response['message']['content'])
                print()

            else:
                print("\nNo matching employees found\n")

    # -------------------------
    # TOP PERFORMERS
    # -------------------------

    elif "top performing" in query:

        cur.execute("""
            SELECT employee_id,
                   full_name,
                   performance_rating
            FROM employees
            ORDER BY performance_rating DESC
            LIMIT 5
        """)

        employees = cur.fetchall()

        data = ""

        for emp in employees:
            data += f"""
            Employee ID: {emp[0]}
            Name: {emp[1]}
            Performance Rating: {emp[2]}

            """

        response = ollama.chat(
            model='gemma:2b',
            messages=[
                {
                    'role': 'user',
                    'content': f"""
                    HR Query:
                    {query}

                    Employee Data:
                    {data}

                    Summarize professionally.
                    """
                }
            ]
        )

        print("\nAI RESPONSE:\n")
        print(response['message']['content'])
        print()

    # -------------------------
    # SINGLE EMPLOYEE QUERY
    # -------------------------

    else:

        match = re.search(r'\d+', query)

        if match:

            emp_id = match.group()

            cur.execute("""
                SELECT *
                FROM employees
                WHERE employee_id = %s
            """, (emp_id,))

            employee = cur.fetchone()

            if employee:

                data = f"""
                Employee Details:

                Employee ID: {employee[0]}
                Name: {employee[1]}
                Email: {employee[2]}
                Department: {employee[3]}
                Designation: {employee[4]}
                Attendance: {employee[5]}%
                Salary: {employee[6]}
                Joining Date: {employee[7]}
                """

                response = ollama.chat(
                    model='gemma:2b',
                    messages=[
                        {
                            'role': 'user',
                            'content': f"""
                            HR Query:
                            {query}

                            Employee Data:
                            {data}

                            Answer professionally.
                            """
                        }
                    ]
                )

                print("\nAI RESPONSE:\n")
                print(response['message']['content'])
                print()

            else:
                print("\nEmployee not found\n")

        else:
            print("\nQuery not understood\n")

cur.close()
conn.close()