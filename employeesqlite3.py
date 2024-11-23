import sqlite3

class Employee:
    def __init__(self, emp_id, name, department, salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary = salary

    def display_details(self):
        print(f"Employee ID: {self.emp_id}")
        print(f"Name: {self.name}")
        print(f"Department: {self.department}")
        print(f"Salary: ${self.salary:,.2f}")

class EmployeeManagementSystem:
    def __init__(self):
        self.conn = sqlite3.connect('employee_management.sqlite3')  # Connect to SQLite database or creates a new database
        self.cursor = self.conn.cursor()
        self.create_employee_table()  # Ensure table exists
        self.auto_id = self.get_auto_id()  # Get the last employee ID

    def create_employee_table(self):
        # Create the employee table if it doesn't exist
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
        ''')
        self.conn.commit()   #stores data permanently

    def get_auto_id(self):
        # Fetch the highest emp_id to determine the next auto_id
        self.cursor.execute("SELECT MAX(emp_id) FROM employees")
        result = self.cursor.fetchone()
        return result[0] + 1 if result[0] else 1

    def add_employee(self):
        print("\nEnter employee details:")
        name = input("Enter Name: ")
        department = input("Enter Department: ")
        salary = float(input("Enter Salary: "))

        # Insert the new employee into the database
        self.cursor.execute('''
        INSERT INTO employees (emp_id, name, department, salary)
        VALUES (?, ?, ?, ?)
        ''', (self.auto_id, name, department, salary))
        self.conn.commit()

        print(f"Employee added successfully with ID: {self.auto_id}")
        self.auto_id += 1  # Increment auto_id for the next employee

    def filter_by_department(self, department):
        # Filter employees by department
        self.cursor.execute("SELECT * FROM employees WHERE department = ?", (department,))
        rows = self.cursor.fetchall()
        return [Employee(emp_id=row[0], name=row[1], department=row[2], salary=row[3]) for row in rows]

    def filter_by_salary_range(self, min_salary, max_salary):
        # Filter employees by salary range
        self.cursor.execute("SELECT * FROM employees WHERE salary BETWEEN ? AND ?", (min_salary, max_salary))
        rows = self.cursor.fetchall()
        return [Employee(emp_id=row[0], name=row[1], department=row[2], salary=row[3]) for row in rows]

    def view_employees(self):
        # Fetch all employees and display them
        self.cursor.execute("SELECT * FROM employees")
        rows = self.cursor.fetchall()
        if rows:
            print("\nEmployee Details:")
            for row in rows:
                emp = Employee(emp_id=row[0], name=row[1], department=row[2], salary=row[3])
                emp.display_details()
        else:
            print("\nNo employees found!")

    def view_filtered_employees(self):
        print("\nView Employees By:")
        print("1. Department")
        print("2. Salary Range")
        filter_choice = input("Enter 1 or 2 to filter: ").strip()

        if filter_choice == '1':
            department = input("Enter department to filter by: ").strip()
            filtered_employees = self.filter_by_department(department)
            self.display_filtered_employees(filtered_employees)

        elif filter_choice == '2':
            try:
                min_salary = float(input("Enter minimum salary: "))
                max_salary = float(input("Enter maximum salary: "))
                filtered_employees = self.filter_by_salary_range(min_salary, max_salary)
                self.display_filtered_employees(filtered_employees)
            except ValueError:
                print("Invalid salary input. Please enter numeric values.")
        else:
            print("Invalid choice for filtering option.")

    def display_filtered_employees(self, employees):
        if employees:
            print("\nFiltered Employee Details:")
            for employee in employees:
                employee.display_details()
        else:
            print("No employees found matching the criteria.")

    def update_employee(self):
        emp_id = int(input("\nEnter the Employee ID to update: "))
        employee = self.search_employee(emp_id)

        if employee:
            print(f"Updating details for Employee ID: {emp_id}")
            employee.name = input(f"Enter new name (Current: {employee.name}): ") or employee.name
            employee.department = input(f"Enter new department (Current: {employee.department}): ") or employee.department
            salary = input(f"Enter new salary (Current: {employee.salary}): ")
            employee.salary = float(salary) if salary else employee.salary

            # Update the employee in the database
            self.cursor.execute('''
            UPDATE employees SET name = ?, department = ?, salary = ? WHERE emp_id = ?
            ''', (employee.name, employee.department, employee.salary, emp_id))
            self.conn.commit()

            print("Employee details updated successfully!")
        else:
            print(f"No employee found with ID: {emp_id}")

    def delete_employee(self):
        emp_id = int(input("\nEnter the Employee ID to delete: "))
        employee = self.search_employee(emp_id)

        if employee:
            self.cursor.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
            self.conn.commit()
            print(f"Employee with ID {emp_id} deleted successfully!")
        else:
            print(f"No employee found with ID: {emp_id}")

    def search_employee(self, emp_id):
        self.cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
        row = self.cursor.fetchone()
        if row:
            return Employee(emp_id=row[0], name=row[1], department=row[2], salary=row[3])
        return None

    def calculate_average_salary_by_department(self):
        department = input("Enter department to calculate average salary: ").strip()

        # Filter employees by department
        filtered_employees = self.filter_by_department(department)

        if filtered_employees:
            total_salary = sum(emp.salary for emp in filtered_employees)
            average_salary = total_salary / len(filtered_employees)
            print(f"\nAverage Salary for department {department}: ${average_salary:,.2f}")
        else:
            print(f"No employees found in the department {department}.")

    def close_connection(self):
        self.conn.close()

# Main function to interact with the system
def main():
    system = EmployeeManagementSystem()

    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. View Employees by Criteria")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Search Employee")
        print("7. Calculate Average Salary by Department")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            system.add_employee()
        elif choice == '2':
            system.view_employees()
        elif choice == '3':
            system.view_filtered_employees()
        elif choice == '4':
            system.update_employee()
        elif choice == '5':
            system.delete_employee()
        elif choice == '6':
            emp_id = int(input("\nEnter Employee ID to search: "))
            employee = system.search_employee(emp_id)
            if employee:
                employee.display_details()
            else:
                print(f"No employee found with ID: {emp_id}")
        elif choice == '7':
            system.calculate_average_salary_by_department()
        elif choice == '8':
            print("Exiting the system. Goodbye!")
            system.close_connection()  # Close the database connection before exiting
            break
        else:
            print("Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    main()
