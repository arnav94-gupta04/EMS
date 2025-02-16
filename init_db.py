from db import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Create table for admin login
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin_login (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    """)

    # Create table for employee personal details
    cur.execute("""
    CREATE TABLE IF NOT EXISTS emp (
        id INTEGER PRIMARY KEY,
        First_Name TEXT NOT NULL,
        Last_Name TEXT NOT NULL,
        Gender TEXT,
        Email_id TEXT,
        Age INTEGER,
        Marital_Status TEXT,
        DOB TEXT
    )
    """)

    # Create table for employee job details
    cur.execute("""
    CREATE TABLE IF NOT EXISTS job (
        id INTEGER PRIMARY KEY,
        Position TEXT,
        Department TEXT,
        Branch TEXT,
        Years_of_Experience INTEGER,
        Salary REAL,
        Emp_Satisfaction REAL,
        Performance_Score TEXT
    )
    """)

    # Create table for leave applications/approvals
    cur.execute("""
    CREATE TABLE IF NOT EXISTS adm_ap (
        RegNo INTEGER PRIMARY KEY,
        id INTEGER,
        leave_type TEXT,
        From_date TEXT,
        To_date TEXT,
        ApprovalStatus TEXT
    )
    """)

    # Create table for attendance logs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS log_emp (
        in_time TEXT,
        id INTEGER,
        date TEXT,
        out_time TEXT
        selfie BLOB,         -- new column for storing the selfie image (as binary)
        geo_coords TEXT 
    )
    """)

    # Create table for payroll records
    cur.execute("""
    CREATE TABLE IF NOT EXISTS p_roll (
        id INTEGER,
        Year INTEGER,
        Week INTEGER,
        Grosspay REAL,
        Regularpay REAL,
        Overtime_hours REAL,
        Overtimepay REAL,
        PRIMARY KEY (id, Year, Week)
    )
    """)

    # Create table for employee login credentials
    cur.execute("""
    CREATE TABLE IF NOT EXISTS emp_login (
        id INTEGER PRIMARY KEY,
        password TEXT NOT NULL
    )
    """)

    # Create table for rate of pay (for payroll calculations)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS rate_of_pay_emp (
        id INTEGER PRIMARY KEY,
        rate REAL
    )
    """)

    # Insert default admin login if not exists
    cur.execute("SELECT * FROM admin_login WHERE username = ?", ("admin",))
    if not cur.fetchone():
        cur.execute("INSERT INTO admin_login (username, password) VALUES (?, ?)", ("admin", "admin"))

    # Insert default employee login (for example, employee id 1)
    cur.execute("SELECT * FROM emp_login WHERE id = ?", (1,))
    if not cur.fetchone():
        cur.execute("INSERT INTO emp_login (id, password) VALUES (?, ?)", (1, "password"))

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
