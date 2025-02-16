from db import get_connection

def insert_dummy_data():
    conn = get_connection()
    cur = conn.cursor()

    # ----- Admin Login (default admin already inserted in init_db.py) -----
    # You may add additional admin users if desired.
    cur.execute("INSERT OR IGNORE INTO admin_login (username, password) VALUES (?, ?)", 
                ("superadmin", "supersecret"))

    # ----- Employee Personal Details -----
    dummy_emps = [
        (1, "Alice", "Smith", "Female", "alice@example.com", 30, "Single", "01 Jan 1993"),
        (2, "Bob", "Johnson", "Male", "bob@example.com", 35, "Married", "15 Feb 1988"),
        (3, "Charlie", "Brown", "Male", "charlie@example.com", 28, "Single", "20 Mar 1995"),
        (4, "Dana", "White", "Female", "dana@example.com", 40, "Married", "10 Apr 1983")
    ]
    for emp in dummy_emps:
        cur.execute(
            "INSERT OR IGNORE INTO emp (id, First_Name, Last_Name, Gender, Email_id, Age, Marital_Status, DOB) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            emp
        )

    # ----- Employee Job Details -----
    dummy_jobs = [
        (1, "Manager", "HR", "New York", 10, 80000.0, 4.5, "A"),
        (2, "Developer", "IT", "San Francisco", 8, 90000.0, 4.2, "B"),
        (3, "Analyst", "Finance", "Chicago", 5, 70000.0, 4.0, "B"),
        (4, "Designer", "Marketing", "Los Angeles", 6, 75000.0, 4.3, "A")
    ]
    for job in dummy_jobs:
        cur.execute(
            "INSERT OR IGNORE INTO job (id, Position, Department, Branch, Years_of_Experience, Salary, Emp_Satisfaction, Performance_Score) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            job
        )

    # ----- Leave Applications / Approvals -----
    dummy_leaves = [
        (1, 1, "Casual Leave", "2023-05-01", "2023-05-03", "Pending"),
        (2, 2, "Sick Leave", "2023-06-10", "2023-06-12", "Approved")
    ]
    for leave in dummy_leaves:
        cur.execute(
            "INSERT OR IGNORE INTO adm_ap (RegNo, id, leave_type, From_date, To_date, ApprovalStatus) VALUES (?, ?, ?, ?, ?, ?)",
            leave
        )

    # ----- Attendance Logs -----
    dummy_logs = [
        ("09:00:00", 1, "2023-07-01", "17:00:00"),
        ("09:15:00", 2, "2023-07-01", "17:15:00"),
        ("09:30:00", 3, "2023-07-01", "17:30:00"),
        ("09:45:00", 4, "2023-07-01", "17:45:00")
    ]
    for log in dummy_logs:
        cur.execute(
            "INSERT OR IGNORE INTO log_emp (in_time, id, date, out_time) VALUES (?, ?, ?, ?)",
            log
        )

    # ----- Payroll Records -----
    dummy_payroll = [
        (1, 2023, 27, 1600.0, 1500.0, 5.0, 100.0),
        (2, 2023, 27, 1700.0, 1600.0, 5.0, 100.0),
        (3, 2023, 27, 1400.0, 1300.0, 4.0, 100.0),
        (4, 2023, 27, 1500.0, 1400.0, 4.0, 100.0)
    ]
    for pr in dummy_payroll:
        cur.execute(
            "INSERT OR IGNORE INTO p_roll (id, Year, Week, Grosspay, Regularpay, Overtime_hours, Overtimepay) VALUES (?, ?, ?, ?, ?, ?, ?)",
            pr
        )

    # ----- Employee Login Credentials -----
    dummy_emp_login = [
        (1, "password"),
        (2, "password"),
        (3, "password"),
        (4, "password")
    ]
    for login in dummy_emp_login:
        cur.execute(
            "INSERT OR IGNORE INTO emp_login (id, password) VALUES (?, ?)",
            login
        )

    # ----- Rate of Pay -----
    dummy_rate = [
        (1, 20.0),
        (2, 22.0),
        (3, 18.0),
        (4, 25.0)
    ]
    for rate_data in dummy_rate:
        cur.execute(
            "INSERT OR IGNORE INTO rate_of_pay_emp (id, rate) VALUES (?, ?)",
            rate_data
        )

    conn.commit()
    conn.close()
    print("Dummy data inserted successfully.")

if __name__ == "__main__":
    insert_dummy_data()
