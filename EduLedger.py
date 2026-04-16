import sqlite3 as sql
from pyfiglet import Figlet
import fontstyle as font
import time

class Color:
    def black(self, string):
        return f"\033[90m{string}\033[0m"
    
    def red(self, string):
        return f"\033[91m{string}\033[0m"
    
    def green(self, string):
        return f"\033[92m{string}\033[0m"
    
    def yellow(self, string):
        return f"\033[93m{string}\033[0m"
    
    def blue(self, string):
        return f"\033[94m{string}\033[0m"
    
    def magenta(self, string):
        return f"\033[95m{string}\033[0m"
    
    def cyan(self, string):
        return f"\033[96m{string}\033[0m"

    def white(self, string):
        return f"\033[97m{string}\033[0m"

class Style:
    def bold(self, string):
        return f"\033[1m{string}\033[0m"
    
    def italic(self, string):
        return f"\033[3m{string}\033[0m"
    
    def dim(self, string):
        return f"\033[2m{string}\033[0m"
    
    def underline(self, string):
        return f"\033[4m{string}\033[0m"
    
    def blink(self, string):
        return f"\033[5m{string}\033[0m"
    

color = Color()
style = Style()

x = Figlet(font='slant')
print(color.green("\n======================================================="))
banner = style.bold(color.yellow(x.renderText("EduLedger")))
print(banner)
print(color.green("======================================================="))

time.sleep(0.5)

# connecting to database
def connect():
    connection = sql.connect("students.db")
    time.sleep(0.5)
    print(color.magenta("Connected to students database."))
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
        print(color.green("✔️ Data Inserted Successfully!"))
    
    def update_data(self):
        cur = self.connection.cursor()
        try:
            student_id = int(input(font.apply("Enter student ID : "),'bold'))
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
    time.sleep(0.5)
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
                student_id = int(input("Enter student ID: "))
                student.display(student_id)
            except ValueError:
                print("❌ Invalid ID")

        elif choice == '3':
            try:
                db.update_data()
            except Exception as e:
                print(color.red("Error : ", e))

        elif choice == '4' or choice.lower() == 'exit':
            print(font.apply(color.yellow("Exiting..."),'bold'))
            break
        
        else:
            x = color.red("\n❌ Invalid choice")
            print(font.apply(x,'bold'))
    connection.close()

if __name__ == "__main__":
    main()