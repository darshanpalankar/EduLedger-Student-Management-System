from pyfiglet import Figlet
import sqlite3 as sql
import time
import stylizer
    
color = stylizer.Color()
style = stylizer.Style()

# Banner
x = Figlet(font='slant')
banner = color.yellow(x.renderText("EduLedger"))

print(color.green("\n======================================================="))
print(banner)
print(color.green("======================================================="))

time.sleep(0.5)

# connecting to database
def connect():
    connection = sql.connect("students.db")
    time.sleep(0.5)
    print(style.italic(color.magenta("Connected..!!!")))
    return connection

# Class Database
class DataBase:
    def __init__(self, connection):
        self.connection = connection

    def create_table(self):
        cur = self.connection.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS Students(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Age INTEGER NOT NULL
            )"""
        )
        self.connection.commit()

    def insert_data(self):
        cur = self.connection.cursor()
        try:
            name = input(color.blue("Enter student name: "))
            age = int(input(color.blue("Enter student age: ")))
        except ValueError:
            print(color.red("Enter valid student information!"))
            return
        cur.execute("INSERT INTO Students(Name, Age) VALUES(?, ?)", (name, age))
       
        self.connection.commit()
        print(color.green("✔️  Data Inserted Successfully!"))
    
    def update_data(self):
        cur = self.connection.cursor()
        try:
            student_id = int(input(style.bold("Enter student ID : ")))
            name = input("Enter name of the student : ")
            age = int(input("Enter age of the student : "))
            cur.execute(f'''
                        UPDATE INTO Students SET (Name, Age) VALUES(name, age) WHERE ID = {student_id}
                    ''')
            print(f"Data updated!")
            self.connection.commit()
        except Exception as e:
            print("Invalid Student ID!")
        except ValueError:
            print("Invalid Student ID!")
    
    def delete_row(self, student_id):
        cur = self.connection.cursor()
        cur.execute(f'''ALTER TABLE Students DELETE ROW WHERE ID = ?,{student_id}''')
        print(f"{student_id} ID is deleted!")
        self.connection.commit()

    def drop_table(self):
        cur = self.connection.cursor()
        cur.execute("DROP TABLE IF EXISTS Students")
        print(color.green("Table is deleted successfully!"))
        self.connection.commit()
    
# Class students
class Student:
    def __init__(self, connection):
        self.connection = connection

    def student_rows(self):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM Students")
        return cur.fetchall()

    def search_student(self):
        cur = self.connection.cursor()
        try:
            name = input("Enter student name: ")

            cur.execute(f"SELECT * FROM students WHERE name = {name}")
            result = cur.fetchall()

            for row in result:
                print(row)

        except Exception as e:
            print("Error:", e)

    def display(self, student_id):
        cur = self.connection.cursor()
        cur.execute(
            "SELECT ID, Name, Age FROM Students WHERE ID = ?",
            (student_id,),
        )
        row = cur.fetchone()

        if row is None:
            print(color.red(f"No student found with ID {student_id}."))
            return

        print(color.cyan(f"Student ID : {row[0]}"))
        print(color.cyan(f"Name : {row[1]}"))
        print(color.cyan(f"Age : {row[2]}"))

def main():
    connection = connect()
    db = DataBase(connection)
    db.create_table()

    student = Student(connection)

    while True:
        print(color.cyan("\n1. Insert Student Info"))
        print(color.cyan("2. Display Student Info"))
        print(color.cyan("3. Update Student Info"))
        print(color.cyan("4. Delete Student Info"))
        print(color.cyan("5. Search Student"))
        print(color.cyan("6. Exit"))

        choice = input(color.green("\nEnter choice: "))

        if choice == '1':
            db.insert_data()

        elif choice == '2':
            try:
                student_id = int(input(color.yellow("Enter student ID: ")))
                student.display(student_id)
            except ValueError:
                print("❌ Invalid ID")

        elif choice == '3':
            try:
                db.update_data()
            except Exception as e:
                print(color.red("Error : ", e))
        
        elif choice == '4':
            try:
                student_id = int(input(color.yellow("Enter student ID: ")))
                db.delete_row(student_id)
            except Exception as e:
                print(color.red("Error : Student not found!"))

        elif choice == '5':
            try:
                student.search_student()
            except Exception as e:
                print(color.red("Error : ", e))

        elif choice == '6' or choice.lower() == 'exit':
            print(style.bold(color.yellow("Exiting...")))
            break
        
        else:
            x = color.red("\n❌ Invalid choice")
            print(style.bold(x))
            print("Please enter choice number!")
    connection.close()

if __name__ == "__main__":
    main()
