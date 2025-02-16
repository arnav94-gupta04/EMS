import streamlit as st
from db import get_connection
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests

def employee_login():
    if 'employee_logged_in' not in st.session_state:
        st.session_state['employee_logged_in'] = False
    if not st.session_state['employee_logged_in']:
        st.header('Enter Employee Credentials')
        emp_id = st.number_input("Enter Employee ID:", min_value=1, step=1)
        password = st.text_input("Enter Password:", type="password")
        if st.button("Login"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM emp_login WHERE id = ?", (emp_id,))
            row = cur.fetchone()
            if row and row["password"] == password:
                st.session_state['employee_logged_in'] = True
                st.session_state['employee_id'] = emp_id
                st.rerun()
            else:
                st.error("Wrong ID or password. Try again.")
            conn.close()

def run_employee():
    employee_login()
    if st.session_state.get('employee_logged_in'):
        st.sidebar.subheader("Employee Menu")
        choice = st.sidebar.selectbox('Choose', ("Employee's info", 'Leave Monitoring', 'About', 'Attendance', 'Payroll'))
        if choice == "Employee's info":
            employee_info()
        elif choice == 'Leave Monitoring':
            employee_leave_monitoring()
        elif choice == 'About':
            employee_about()
        elif choice == 'Attendance':
            employee_attendance()
        elif choice == 'Payroll':
            employee_payroll()

def employee_info():
    st.subheader("Employee Information")
    category = st.sidebar.selectbox('Category', ('Display', 'Modify'))
    conn = get_connection()
    cur = conn.cursor()
    emp_id = st.session_state.get('employee_id')
    if category == 'Display':
        option = st.selectbox('Choose', ('All', 'Personal', 'Professional', 'Branch'))
        if option == 'All':
            query = """
                SELECT e.id, e.First_Name, e.Last_Name, e.Gender, e.Email_id, e.Age, e.Marital_Status,
                       j.Position, j.Department, j.Branch, j.Years_of_Experience, j.Salary, j.Emp_Satisfaction, j.Performance_Score
                FROM emp e JOIN job j ON e.id = j.id WHERE e.id = ?
            """
            cur.execute(query, (emp_id,))
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
            st.dataframe(df)
        elif option == 'Personal':
            cur.execute("SELECT * FROM emp WHERE id = ?", (emp_id,))
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
            st.dataframe(df)
        elif option == 'Professional':
            cur.execute("SELECT * FROM job WHERE id = ?", (emp_id,))
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
            st.dataframe(df)
        elif option == 'Branch':
            cur.execute("SELECT Branch, Position, Department, COUNT(id) as 'Total Employees' FROM job WHERE id = ? GROUP BY Branch, Position, Department", (emp_id,))
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
            st.dataframe(df)
    elif category == 'Modify':
        sub_category = st.selectbox('Select', ('Personal', 'Professional'))
        if sub_category == 'Personal':
            field = st.selectbox('Choose field to update', ('AGE', 'MARITAL_STATUS'))
            if field == 'AGE':
                new_age = st.number_input('New Age:', min_value=0, step=1)
                if st.button('Update Age'):
                    cur.execute("UPDATE emp SET Age = ? WHERE id = ?", (new_age, emp_id))
                    conn.commit()
                    st.success("Age updated successfully.")
            else:
                new_status = st.text_input('New Marital Status:')
                if st.button('Update Marital Status'):
                    cur.execute("UPDATE emp SET Marital_Status = ? WHERE id = ?", (new_status, emp_id))
                    conn.commit()
                    st.success("Marital Status updated successfully.")
        else:
            field = st.selectbox('Choose field to update', ('POSITION', 'DEPARTMENT', 'BRANCH', 'YEARS_OF_EXPERIENCE', 'SALARY', 'EMP_SATISFACTION', 'SCORE'))
            if field == 'POSITION':
                new_value = st.text_input('New Job Position:')
                button_label = 'Update Position'
                query = "UPDATE job SET Position = ? WHERE id = ?"
            elif field == 'DEPARTMENT':
                new_value = st.text_input('New Department:')
                button_label = 'Update Department'
                query = "UPDATE job SET Department = ? WHERE id = ?"
            elif field == 'BRANCH':
                new_value = st.text_input('New Branch:')
                button_label = 'Update Branch'
                query = "UPDATE job SET Branch = ? WHERE id = ?"
            elif field == 'YEARS_OF_EXPERIENCE':
                new_value = st.number_input('New Years of Experience:', min_value=0, step=1)
                button_label = 'Update Experience'
                query = "UPDATE job SET Years_of_Experience = ? WHERE id = ?"
            elif field == 'SALARY':
                new_value = st.number_input('New Salary:', min_value=0.0, format="%.2f")
                button_label = 'Update Salary'
                query = "UPDATE job SET Salary = ? WHERE id = ?"
            elif field == 'EMP_SATISFACTION':
                new_value = st.number_input('New Employee Satisfaction:', min_value=0.0, format="%.2f")
                button_label = 'Update Satisfaction'
                query = "UPDATE job SET Emp_Satisfaction = ? WHERE id = ?"
            elif field == 'SCORE':
                new_value = st.text_input('New Performance Score:')
                button_label = 'Update Score'
                query = "UPDATE job SET Performance_Score = ? WHERE id = ?"
            if st.button(button_label):
                cur.execute(query, (new_value, emp_id))
                conn.commit()
                st.success("Update successful.")
    conn.close()

def employee_leave_monitoring():
    st.subheader("Leave Monitoring")
    option = st.selectbox("Select", ('View', 'Apply'))
    conn = get_connection()
    cur = conn.cursor()
    emp_id = st.session_state.get('employee_id')
    if option == 'Apply':
        st.write("Choose the leave type: Casual leave, Sick leave, Maternity/Paternity Leave, Others")
        reg_no = st.number_input('Enter the RegNo:', min_value=1, step=1)
        leave_type = st.text_input('Enter leave type:')
        from_date = st.date_input('From date:')
        to_date = st.date_input('To date:')
        if st.button('Apply'):
            cur.execute(
                "UPDATE adm_ap SET id = ?, leave_type = ?, From_date = ?, To_date = ? WHERE RegNo = ?",
                (emp_id, leave_type, str(from_date), str(to_date), reg_no)
            )
            conn.commit()
            st.success("Leave applied successfully. Waiting for approval.")
    elif option == 'View':
        cur.execute("SELECT * FROM adm_ap WHERE id = ?", (emp_id,))
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        st.dataframe(df)
    conn.close()

def employee_about():
    st.subheader("Analytics")
    conn = get_connection()
    cur = conn.cursor()
    if st.checkbox("Employees by Branches"):
        cur.execute("SELECT Branch, COUNT(id) as Total_employees FROM job GROUP BY Branch")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        st.table(df)
    if st.checkbox("Employees by department"):
        cur.execute("SELECT Department, COUNT(id) as Total_employees FROM job GROUP BY Department")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        st.bar_chart(df.set_index("Department"))
    if st.checkbox("Employees by Gender"):
        cur.execute("SELECT * FROM emp WHERE id = ?", (st.session_state.get('employee_id'),))
        row = cur.fetchone()
        if row:
            gender = row["Gender"]
            pie = px.pie(names=[gender], values=[1])
            st.plotly_chart(pie)
    if st.checkbox("Employees by job roles"):
        cur.execute("SELECT * FROM job WHERE id = ?", (st.session_state.get('employee_id'),))
        row = cur.fetchone()
        if row:
            pie = px.pie(names=[row["Position"]], values=[1])
            st.plotly_chart(pie)
    if st.checkbox("Job experience and Salary range"):
        cur.execute("SELECT * FROM job WHERE id = ?", (st.session_state.get('employee_id'),))
        row = cur.fetchone()
        if row:
            st.write(f"Years of Experience: {row['Years_of_Experience']}, Salary: {row['Salary']}")
    if st.checkbox("Employees by Performance Score"):
        cur.execute("SELECT Performance_Score FROM job WHERE id = ?", (st.session_state.get('employee_id'),))
        row = cur.fetchone()
        if row:
            st.write(f"Performance Score: {row['Performance_Score']}")
    conn.close()

def get_geolocation():
    """Fetch geolocation automatically using an external API."""
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        return data["loc"]  # Returns "latitude,longitude"
    except Exception as e:
        st.error("Could not retrieve location.")
        return None
    
def employee_attendance():
    st.subheader("Attendance")
    option = st.selectbox("Choose", ('View my attendance report', 'Fill my attendance report'))
    
    # Retrieve the logged in employee ID from session state
    emp_id = st.session_state.get('employee_id')
    
    if option == 'View my attendance report':
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM log_emp WHERE id = ?", (emp_id,))
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        st.dataframe(df)
        conn.close()
    else:
        # Capture current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.write("Current timestamp:", timestamp)
        
        # Capture a selfie using the built-in camera widget
        selfie = st.camera_input("Take a selfie for attendance")
        
        geo_coords = get_geolocation()
        if geo_coords:
            st.write(f"Detected Location: {geo_coords}")
        
        # Additional attendance details
        date_today = st.date_input("Enter today's date:")
        finishing_time = st.text_input("Enter finishing time:")
        
        if st.button("Log Attendance"):
            # Convert the selfie to bytes if captured
            selfie_bytes = selfie.getvalue() if selfie is not None else None
            
            # Insert attendance record including timestamp, selfie, and geo-coordinates
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO log_emp (in_time, id, date, out_time, selfie, geo_coords) VALUES (?,?,?,?,?,?)",
                (timestamp, emp_id, str(date_today), finishing_time, selfie_bytes, geo_coords)
            )
            conn.commit()
            conn.close()
            st.success("Attendance logged successfully!")

def employee_payroll():
    st.subheader("Payroll")
    conn = get_connection()
    cur = conn.cursor()
    emp_id = st.session_state.get('employee_id')
    option = st.selectbox("Choose", ('View',))
    if option == 'View':
        query = """
            SELECT e.id, e.First_Name, e.Last_Name, e.Age, j.Position, j.Department, j.Branch,
                   p.Year, p.Week, p.Grosspay, p.Regularpay, p.Overtime_hours, p.Overtimepay
            FROM emp e 
            JOIN job j ON e.id = j.id 
            JOIN p_roll p ON e.id = p.id
            WHERE e.id = ?
        """
        cur.execute(query, (emp_id,))
        rows = cur.fetchall()
        if rows:
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
            st.dataframe(df)
        else:
            st.write("No payroll records found.")
    conn.close()
