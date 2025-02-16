import streamlit as st
from db import get_connection
import pandas as pd
import plotly.express as px
from datetime import datetime

def admin_login():
    if 'admin_logged_in' not in st.session_state:
        st.session_state['admin_logged_in'] = False

    if not st.session_state['admin_logged_in']:
        st.header('Enter Admin Credentials')
        username = st.text_input("Enter Username:")
        password = st.text_input("Enter Password:", type="password")
        if st.button("Login"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM admin_login")
            rows = cur.fetchall()
            for row in rows:
                if row["username"] == username and row["password"] == password:
                    st.session_state['admin_logged_in'] = True
                    st.rerun()
                    return
            st.error("Wrong username or password. Try again.")
            conn.close()

def run_admin():
    admin_login()
    if st.session_state.get('admin_logged_in'):
        st.sidebar.subheader("Admin Menu")
        choice = st.sidebar.selectbox('Choose', ('Search', "Employee's info", 'Leave Monitoring', 'About', 'Attendance', 'Payroll'))
        if choice == "Employee's info":
            admin_employee_info()
        elif choice == "Search":
            admin_search()
        elif choice == "Leave Monitoring":
            admin_leave_monitoring()
        elif choice == "About":
            admin_about()
        elif choice == "Attendance":
            admin_attendance()
        elif choice == "Payroll":
            admin_payroll()

def admin_employee_info():
    st.subheader("Employee Information")
    category = st.sidebar.selectbox('Category', ('Display', 'Modify'))
    if category == 'Display':
        option = st.selectbox('Choose', ('All', 'Personal', 'Professional', 'Branch'))
        conn = get_connection()
        cur = conn.cursor()
        if option == 'All':
            query = """
                SELECT e.id, e.First_Name, e.Last_Name, e.Gender, e.Email_id, e.Age, e.Marital_Status,
                       j.Position, j.Department, j.Branch, j.Years_of_Experience, j.Salary, j.Emp_Satisfaction, j.Performance_Score
                FROM emp e JOIN job j ON e.id = j.id ORDER BY e.id
            """
            cur.execute(query)
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
            st.dataframe(df)
        elif option == 'Personal':
            cur.execute("SELECT * FROM emp ORDER BY id")
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
            st.dataframe(df)
        elif option == 'Professional':
            cur.execute("SELECT * FROM job ORDER BY id")
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
            st.dataframe(df)
        elif option == 'Branch':
            query = """
                SELECT Branch, Position, Department, COUNT(id) as "Total Employees"
                FROM job GROUP BY Branch, Position, Department ORDER BY Branch
            """
            cur.execute(query)
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
            st.dataframe(df)
        conn.close()
    elif category == 'Modify':
        sub_category = st.selectbox('Select', ('Personal', 'Professional'))
        if sub_category == 'Personal':
            action = st.selectbox('Choose', ('Add an employee', 'Remove an employee', "Change/update"))
            conn = get_connection()
            cur = conn.cursor()
            if action == 'Add an employee':
                st.write("Enter employee details:")
                emp_id = st.number_input('ID of employee:', min_value=1, step=1)
                first_name = st.text_input('First Name:')
                last_name = st.text_input('Last Name:')
                gender = st.text_input('Gender:')
                email = st.text_input('Email ID:')
                age = st.number_input('Age:', min_value=0, step=1)
                marital_status = st.text_input('Marital Status:')
                dob = st.text_input('Enter DOB (e.g., 01 Jan 2000):')
                if st.button('Add'):
                    cur.execute(
                        "INSERT INTO emp (id, First_Name, Last_Name, Gender, Email_id, Age, Marital_Status, DOB) VALUES (?,?,?,?,?,?,?,?)",
                        (emp_id, first_name, last_name, gender, email, age, marital_status, dob)
                    )
                    conn.commit()
                    st.success("Employee added successfully.")
            elif action == 'Remove an employee':
                emp_id = st.number_input('Enter employee ID to remove:', min_value=1, step=1)
                if st.button('Remove'):
                    cur.execute("DELETE FROM emp WHERE id = ?", (emp_id,))
                    conn.commit()
                    st.success("Employee removed successfully.")
            elif action == "Change/update":
                update_field = st.selectbox('Choose field to update', ('AGE', 'MARITAL_STATUS'))
                emp_id = st.number_input('Employee ID for update:', min_value=1, step=1)
                if update_field == 'AGE':
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
            conn.close()
        else:  # Professional modifications
            action = st.selectbox('Choose', ('Add an employee', 'Remove an employee', "Change/update an employee's info"))
            conn = get_connection()
            cur = conn.cursor()
            if action == 'Add an employee':
                st.write("Enter job details:")
                emp_id = st.number_input('ID:', min_value=1, step=1)
                position = st.text_input('Job Position:')
                department = st.text_input('Department:')
                branch = st.text_input('Branch:')
                years_of_exp = st.number_input('Years of Experience:', min_value=0, step=1)
                salary = st.number_input('Salary:', min_value=0.0, format="%.2f")
                emp_satisfaction = st.number_input('Employee Satisfaction:', min_value=0.0, format="%.2f")
                performance_score = st.text_input('Performance Score:')
                if st.button('Add'):
                    cur.execute(
                        "INSERT INTO job (id, Position, Department, Branch, Years_of_Experience, Salary, Emp_Satisfaction, Performance_Score) VALUES (?,?,?,?,?,?,?,?)",
                        (emp_id, position, department, branch, years_of_exp, salary, emp_satisfaction, performance_score)
                    )
                    conn.commit()
                    st.success("Job details added successfully.")
            elif action == 'Remove an employee':
                emp_id = st.number_input('Enter employee ID to remove from job records:', min_value=1, step=1)
                if st.button('Remove'):
                    cur.execute("DELETE FROM job WHERE id = ?", (emp_id,))
                    conn.commit()
                    st.success("Job record removed successfully.")
            else:
                field = st.selectbox('Choose field to update', ('POSITION', 'DEPARTMENT', 'BRANCH', 'YEARS_OF_EXPERIENCE', 'SALARY', 'EMP_SATISFACTION', 'SCORE'))
                emp_id = st.number_input('Employee ID for update:', min_value=1, step=1)
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

def admin_search():
    st.subheader("Search Employee Information")
    conn = get_connection()
    cur = conn.cursor()
    if st.checkbox("Employee ID, First and Last Name"):
        cur.execute("SELECT id, First_Name, Last_Name FROM emp")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        st.dataframe(df)
    if st.toggle("Using Employee ID"):
        field = st.selectbox("Select field", ('Salary','Department','Branch','Age','Job role','Date of Birth','Experience','Job Satisfaction & Performance Score','Payroll Details'))
        emp_id = st.number_input("Enter Employee ID:", min_value=1, step=1)
        if field == 'Salary':
            cur.execute("SELECT Salary FROM job WHERE id = ?", (emp_id,))
        elif field == 'Department':
            cur.execute("SELECT Department FROM job WHERE id = ?", (emp_id,))
        elif field == 'Branch':
            cur.execute("SELECT Branch FROM job WHERE id = ?", (emp_id,))
        elif field == 'Age':
            cur.execute("SELECT Age FROM emp WHERE id = ?", (emp_id,))
        elif field == 'Job role':
            cur.execute("SELECT Position FROM job WHERE id = ?", (emp_id,))
        elif field == 'Date of Birth':
            cur.execute("SELECT DOB as Date_of_Birth FROM emp WHERE id = ?", (emp_id,))
        elif field == 'Experience':
            cur.execute("SELECT Years_of_Experience as Experience_in_years FROM job WHERE id = ?", (emp_id,))
        elif field == 'Job Satisfaction & Performance Score':
            cur.execute("SELECT Emp_Satisfaction as Job_Satisfaction, Performance_Score FROM job WHERE id = ?", (emp_id,))
        elif field == 'Payroll Details':
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
            st.table(df)
        else:
            st.write("No data found for the given Employee ID.")
    if st.toggle("Using Employee's Names"):
        field = st.selectbox("Select field", ('Salary','Department','Branch','Age','Job role','Date of Birth','Experience','Job Satisfaction & Performance Score','Payroll Details'))
        first_name = st.text_input("Enter First Name:")
        last_name = st.text_input("Enter Last Name:")
        if field == 'Salary':
            query = """
                SELECT j.Salary FROM job j 
                JOIN emp e ON j.id = e.id 
                WHERE e.First_Name = ? AND e.Last_Name = ?
            """
            cur.execute(query, (first_name, last_name))
        elif field == 'Department':
            query = """
                SELECT j.Department FROM job j 
                JOIN emp e ON j.id = e.id 
                WHERE e.First_Name = ? AND e.Last_Name = ?
            """
            cur.execute(query, (first_name, last_name))
        elif field == 'Branch':
            query = """
                SELECT j.Branch FROM job j 
                JOIN emp e ON j.id = e.id 
                WHERE e.First_Name = ? AND e.Last_Name = ?
            """
            cur.execute(query, (first_name, last_name))
        elif field == 'Age':
            query = "SELECT Age FROM emp WHERE First_Name = ? AND Last_Name = ?"
            cur.execute(query, (first_name, last_name))
        elif field == 'Job role':
            query = """
                SELECT j.Position FROM job j 
                JOIN emp e ON j.id = e.id 
                WHERE e.First_Name = ? AND e.Last_Name = ?
            """
            cur.execute(query, (first_name, last_name))
        elif field == 'Date of Birth':
            query = "SELECT DOB as Date_of_Birth FROM emp WHERE First_Name = ? AND Last_Name = ?"
            cur.execute(query, (first_name, last_name))
        elif field == 'Experience':
            query = """
                SELECT j.Years_of_Experience as Experience_in_years FROM job j 
                JOIN emp e ON j.id = e.id 
                WHERE e.First_Name = ? AND e.Last_Name = ?
            """
            cur.execute(query, (first_name, last_name))
        elif field == 'Job Satisfaction & Performance Score':
            query = """
                SELECT j.Emp_Satisfaction as Job_Satisfaction, j.Performance_Score FROM job j 
                JOIN emp e ON j.id = e.id 
                WHERE e.First_Name = ? AND e.Last_Name = ?
            """
            cur.execute(query, (first_name, last_name))
        elif field == 'Payroll Details':
            query = """
                SELECT j.id, e.First_Name, e.Last_Name, e.Age, j.Position, j.Department, j.Branch,
                       p.Year, p.Week, p.Grosspay, p.Regularpay, p.Overtime_hours, p.Overtimepay
                FROM emp e 
                JOIN job j ON e.id = j.id 
                JOIN p_roll p ON e.id = p.id
                WHERE e.First_Name = ? AND e.Last_Name = ?
            """
            cur.execute(query, (first_name, last_name))
        rows = cur.fetchall()
        if rows:
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
            st.table(df)
        else:
            st.write("No data found for the given Employee Name.")
    conn.close()

def admin_leave_monitoring():
    st.subheader("Leave Monitoring")
    option = st.selectbox("Select", ('View', 'Approve'))
    conn = get_connection()
    cur = conn.cursor()
    if option == 'View':
        cur.execute("SELECT * FROM adm_ap")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        st.dataframe(df)
    elif option == 'Approve':
        reg_no = st.number_input("Enter the RegNo. for approval:", min_value=1, step=1)
        status = st.text_input("Enter 'Yes' for approval or 'No' for disapproval:")
        if st.button("Approve/Disapprove"):
            cur.execute("UPDATE adm_ap SET ApprovalStatus = ? WHERE RegNo = ?", (status, reg_no))
            conn.commit()
            st.success("Approval status updated.")
    conn.close()

def admin_about():
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
        cur.execute("SELECT * FROM emp")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        if 'Gender' in df.columns:
            gender_counts = df['Gender'].value_counts()
            labels = gender_counts.index.tolist()
            values = gender_counts.values.tolist()
            pie = px.pie(values=values, names=labels)
            st.plotly_chart(pie)
    if st.checkbox("Employees by job roles"):
        cur.execute("SELECT * FROM job")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        if 'Position' in df.columns:
            pos_counts = df['Position'].value_counts()
            labels = pos_counts.index.tolist()
            values = pos_counts.values.tolist()
            pie = px.pie(values=values, names=labels)
            st.plotly_chart(pie)
    if st.checkbox("Job experience and Salary range"):
        cur.execute("SELECT * FROM job")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        if 'Years_of_Experience' in df.columns and 'Salary' in df.columns:
            st.scatter_chart(df.set_index('Years_of_Experience')[['Salary']])
    if st.checkbox("Employees by Performance Score"):
        cur.execute("SELECT Performance_Score, COUNT(id) as Number_of_Employees FROM job GROUP BY Performance_Score")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        st.bar_chart(df.set_index("Performance_Score"))
    conn.close()

def admin_attendance():
    st.subheader("Attendance Report")
    option = st.selectbox("Choose", ('View attendance report',))
    if option == 'View attendance report':
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM log_emp")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        st.dataframe(df)
        conn.close()

def admin_payroll():
    st.subheader("Payroll")
    option = st.selectbox("Choose", ('View & Approve', 'Display Payroll Report'))
    conn = get_connection()
    cur = conn.cursor()
    if option == 'View & Approve':
        query = """
            SELECT e.id, e.First_Name, e.Last_Name, e.Age, j.Position, j.Department, j.Branch,
                   p.Year, p.Week, p.Grosspay, p.Regularpay, p.Overtime_hours, p.Overtimepay
            FROM emp e 
            JOIN job j ON e.id = j.id 
            JOIN p_roll p ON e.id = p.id
            ORDER BY e.id
        """
        cur.execute(query)
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        st.dataframe(df)
        radio_choice = st.radio("View the rate of pay employee id wise", ['View'])
        if radio_choice == 'View':
            emp_id = st.text_input("Enter Employee ID:")
            if emp_id:
                cur.execute("SELECT * FROM rate_of_pay_emp WHERE id = ?", (emp_id,))
                rows = cur.fetchall()
                if rows:
                    df_rate = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
                    st.dataframe(df_rate)
                else:
                    st.write("No rate information found for this employee.")
            if st.toggle("Enter"):
                emp_id = st.number_input("Enter Employee ID:", min_value=1, step=1)
                year = st.number_input("Enter Year:", min_value=2000, step=1)
                week = st.number_input("Enter Week Number:", min_value=1, step=1)
                time_worked = st.number_input("Total Hours Worked:", min_value=0.0, format="%.2f")
                rate = st.number_input("Enter Rate of Pay:", min_value=0.0, format="%.2f")
                if st.button("Submit Payroll"):
                    if time_worked < 40:
                        grosspay = rate * time_worked
                        regularpay = rate * 40
                        overtime_hours = 0
                        overtimepay = 0
                    else:
                        regularpay = rate * 40
                        overtime_hours = time_worked - 40
                        overtimepay = round(rate * 1.5 * overtime_hours, 2)
                        grosspay = regularpay + overtimepay
                    cur.execute(
                        "INSERT INTO p_roll (id, Year, Week, Grosspay, Regularpay, Overtime_hours, Overtimepay) VALUES (?,?,?,?,?,?,?)",
                        (emp_id, year, week, grosspay, regularpay, overtime_hours, overtimepay)
                    )
                    conn.commit()
                    st.success("Payroll record inserted successfully.")
    elif option == 'Display Payroll Report':
        query = """
            SELECT e.id, e.First_Name, e.Last_Name, e.Age, j.Position, j.Department, j.Branch,
                   p.Year, p.Week, p.Grosspay, p.Regularpay, p.Overtime_hours, p.Overtimepay
            FROM emp e 
            JOIN job j ON e.id = j.id 
            JOIN p_roll p ON e.id = p.id
        """
        cur.execute(query)
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        st.dataframe(df)
    conn.close()
