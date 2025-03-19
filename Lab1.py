import csv
import shutil
import getpass

class LoginUser():
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
        self.cipher = TextSecurity(4)
        self.file_path = '/Users/louisas/Documents/Data 200 - Python/Lab1/Login.csv'

    def login(self):
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if self.user_id in row[0]:
                    encrypted_input = self.cipher.encrypt(self.password)
                    decrypted_input = self.cipher.decrypt(encrypted_input)
                    decrypted_password = self.cipher.decrypt(row[1])
                    if decrypted_password == decrypted_input:
                        print("Login Successful!")
                        return True,row[0],row[1],row[2]
                    else:
                        print("Login failed - Incorrect password.")
                        return False,None,None,None
        print("Login failed - User not found.")

    def logout(self):
        return "Logging Out"
    
    def register_new_user(self, user_id, password, role):
        encrypted_password = self.cipher.encrypt(password)
        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, encrypted_password, role])
            print("Hello new user!")
            first_name = input("Please enter your first name: ")
            last_name = input("Please enter your last name: ")
            if role == 'student':
                student = Student('','','')
                student.add_new_student(user_id,first_name,last_name)
            if role == 'professor':
                professor = Professor('','','','','')
                professor.add_new_professor(user_id,first_name,last_name, '', '')
                
        print(f"User '{user_id}' registered successfully!")

    def change_password(self, user_id, old_password, new_password):
        users = []
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader) 
            users = list(reader)
        
        for user in users:
            if user[0] == user_id:  
                encrypted_old = self.cipher.encrypt(old_password)
                decrypted_old = self.cipher.decrypt(encrypted_old)
                decrypted_password = self.cipher.decrypt(user[1])
                
                if decrypted_password == decrypted_old:
                    user[1] = self.cipher.encrypt(new_password)
                    
                    with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        file.seek(0) 
                        writer.writerow(headers) 
                        writer.writerows(users)  

                    print("Password changed successfully!")
                    return True
                else:
                    print("Error - Incorrect original password.")
                    return False
        print("Error - User not found.")
        return False

class TextSecurity:
    def __init__(self, shift):
        self.shifter=shift
        self.s=self.shifter%26
  
    def _convert(self, text,s):
        result=""
        for i,ch in enumerate(text):     
             if (ch.isupper()):
                  result += chr((ord(ch) + s-65) % 26 + 65)
             else:
                  result += chr((ord(ch) + s-97) % 26 + 97)
        return  result
  
    def encrypt(self, text):
        return self._convert(text,self.shifter)
        
    def decrypt(self, text):
        return self._convert(text,26-self.s) 
            
class Student():
    def __init__(self, email_address, first_name, last_name):
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.students = []
        self.file_path = '/Users/louisas/Documents/Data 200 - Python/Lab1/Student.csv'

    def display_student_records(self):
        print("Displaying student records...")
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) #skip header
            for row in reader:
                student = Student(
                    email_address=row[0],
                    first_name=row[1],
                    last_name=row[2],
                )
                self.students.append(student)
        if self.students:
            for student in self.students:
                print(f"Email: {student.email_address}, Name: {student.first_name} {student.last_name}")
        else:
            print("No student records found.")

    def add_new_student(self, email_address, first_name, last_name):
        new_student = [email_address, first_name, last_name]

        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_student)
        
        print(f"New student: '{self.first_name} {self.last_name}' added.")

    def delete_student(self, email_address):
        students = []
        try:
            with open(self.file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 0 and row[0] != email_address: 
                        students.append(row)

            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(students) 

            print(f"Student with email {email_address} has been deleted.")
        
        except Exception as e:
            print(f"Error deleting student: {e}")

    def modify_student_record(self, student_email, field_index, new_value):
        records = []
        
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            records.append(header) 

            for row in reader:
                if len(row) > 0 and row[0] == student_email:
                    if 0 <= field_index < len(row):  
                        row[field_index] = new_value  
                    else:
                        print(f"Invalid field index: {field_index}")
                        return
                records.append(row)

        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(records)
            file.flush() 

        print(f"Record for {student_email} updated successfully!")

    def sort_students_by_email(self):
        students = []
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if len(row) > 0:
                    students.append((row[0], row[1], row[2]))
        
        sorted_students = sorted(students, key=lambda x: x[0], reverse=False)
        
        print("\nStudents sorted by email:")
        for student in sorted_students:
            print(f"Email: {student[0]}, First Name: {student[1]}, Last Name: {student[2]}")

class Professor():
    def __init__(self, email_address, first_name, last_name, rank, course_id):
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.rank = rank
        self.course_id = course_id
        self.professors = []
        self.file_path = '/Users/louisas/Documents/Data 200 - Python/Lab1/Professor.csv'

    def display_professors(self):
        print("Displaying professor records...")
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) #skip header
            for row in reader:
                professor = Professor(
                    email_address=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    rank=row[3],
                    course_id=row[4],
                )
                self.professors.append(professor)
        if self.professors:
            for professor in self.professors:
                print(f"Email: {professor.email_address}, Name: {professor.first_name} {professor.last_name}, "
                      f"Rank: {professor.rank}, Course ID: {professor.course_id}")
        else:
            print("No professor records found.")

    def add_new_professor(self, email_address, first_name, last_name, rank, course_id):
        new_professor = [email_address, first_name, last_name, rank, course_id]

        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_professor)
            file.flush()  # Ensures data is immediately written to disk

        print(f"New professor added.")


    def delete_professor(self, email_address):
        professors = []
        try:
            with open(self.file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 0 and row[0] != email_address:  
                        professors.append(row)

            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(professors)  

            print(f"Professor with email {email_address} has been deleted.")
        
        except Exception as e:
            print(f"Error deleting professor: {e}")

    def modify_professor(self, pemail, field_index, new_value):
        records = []
        
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader) 
            records.append(header)  

            for row in reader:
                if len(row) > 0 and row[0] == pemail:  
                    if 0 <= field_index < len(row):  
                        row[field_index] = new_value  
                    else:
                        print(f"Invalid field index: {field_index}")
                        return
                records.append(row)

        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(records)

        print(f"Record for {pemail} updated successfully!")

    def get_professor_course_ids(self, pemail):
        courses = []

        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                if len(row) > 0 and row[0] == pemail: 
                    cid = row[4] 
                    courses.append(cid)   

        return courses

    def find_student_professors(self, course_ids):
        professor_details = []  

        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  

            for row in reader:
                if len(row) > 0 and row[4] in course_ids: 
                    pemail, fname, lname, rank, cid = row[0], row[1], row[2], row[3], row[4]  
                    professor_details.append(f"Email: {pemail}, Name: {fname} {lname}, Rank: {rank}, Teaches: {cid}")

        return professor_details

class Course():
    def __init__(self, course_id, course_name, description):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        self.courses = []
        self.file_path = '/Users/louisas/Documents/Data 200 - Python/Lab1/Course.csv'

    def display_courses(self):
        print("Displaying course records...")
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) #skip header
            for row in reader:
                course = Course(
                    course_id=row[0],
                    course_name=row[1],
                    description=row[2]
                )
                self.courses.append(course)
        if self.courses:
            for course in self.courses:
                print(f"Course id: {course.course_id}, Course Name: {course.course_name}, Description: {course.description}, ")
        else:
            print("No course records found.")

    def add_new_course(self, course_id, course_name, description):
        new_course = [course_id, course_name, description]

        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_course)
        
        print(f"New course: '{self.course_id} - {self.course_name}' added.")

    def delete_course(self, course_id):
        """Deletes a course from the CSV file."""
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        with open(self.file_path, 'w') as file:
            for line in lines:
                if not line.startswith(course_id):  # Exclude the deleted course
                    file.write(line)

    def modify_course(self, cid, field_index, new_value):
        records = []
        
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader) 
            records.append(header)  

            for row in reader:
                if len(row) > 0 and row[0] == cid:  
                    if 0 <= field_index < len(row):  
                        row[field_index] = new_value  
                    else:
                        print(f"Invalid field index: {field_index}")
                        return
                records.append(row)

        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(records)

        print(f"Record for {cid} updated successfully!")        

    def find_student_courses(self, course_ids):
        course_details = []

        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader) 

            for row in reader:
                if len(row) > 0 and row[0] in course_ids:
                    cid, cname, description = row[0], row[1], row[2] 
                    course_details.append(f"Course: {cid} - {cname}, Description: {description}")

        return course_details

    def show_courses_by_professor(self, course_ids):
        course_details = []

        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader) 

            for row in reader:
                if len(row) > 0 and row[0] in course_ids:
                    cid, cname, description = row[0], row[1], row[2] 
                    course_details.append(f"Course: {cid} - {cname}, Description: {description}")
        return course_details

class Grade():
    def __init__(self, email_address, course_id, grade, mark):
        self.email_address = email_address
        self.course_id = course_id
        self.grade = grade
        self.mark = mark
        self.file_path = '/Users/louisas/Documents/Data 200 - Python/Lab1/Grades.csv'

    def add_grade(self, semail, cid, sgrade, smark):
        new_grade = [semail, cid, sgrade, smark]

        with open(self.file_path, mode='a', newline=' ', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_grade)
        
        print(f"New grade: '{sgrade} - {smark}' added for student email '{semail}' taking course '{cid}'.")

    def delete_grade(self, semail, cid):
        grades = []
        try:
            with open(self.file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 0 and row[0] != semail and row[1] != cid:  
                        grades.append(row)

            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(grades)  

            print(f"Grade for student email '{semail}' taking course '{cid}' has been deleted.")
        
        except Exception as e:
            print(f"Error deleting professor: {e}")

    def modify_grade(self, student_email, cid, field_index, new_value):
        records = []
        
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader) 
            records.append(header) 

            for row in reader:
                if len(row) > 0 and row[0] == student_email and row[1] == cid: 
                    if 0 <= field_index < len(row):
                        row[field_index] = new_value
                    else:
                        print(f"Invalid field index: {field_index}")
                        return
                records.append(row)

        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(records)

        print(f"Record for {student_email}, {cid} updated successfully!")

    def find_student_grades(self, student_email):
        grades = []
        course_ids = [] 

        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                if len(row) > 0 and row[0] == student_email: 
                    course, grade, mark = row[1], row[2], row[3]  
                    grades.append((course, grade, mark)) 
                    course_ids.append(course)  

        return grades, course_ids

    def grades_by_course(self, cid):
        grades = []
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                if len(row) > 0 and row[1] == cid:
                    student_id,cid,grade,mark = row[0], row[1], row[2], row[3]
                    grades.append((student_id,grade,mark))
        if grades:
            for grade in grades:
                student_id,grade,mark = grade
                print(f"Student: {student_id}, Grade: {grade}, Mark: {mark}")
        else:
            print("No course records found.")

    def average_grade_by_course(self, cid):
        grades = []
        marks = []
        count = 0
        count_a = 0
        count_b = 0
        count_c = 0
        count_d = 0
        count_f = 0
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                if len(row) > 0 and row[1] == cid:
                    grade,mark = row[2], row[3]
                    grades.append(grade)
                    marks.append(mark)
                    count += 1
          
        for grade in grades:
            if grade == 'A':
                count_a += 1
            if grade == 'B':
                count_b += 1
            if grade == 'C':
                count_c += 1
            if grade == 'D':
                count_d += 1
            if grade == 'F':
                count_f += 1
        
        int_marks = [int(mark) for mark in marks]
        avg = sum(int_marks)/len(int_marks)

        print(f"\n{cid}")
        print(f"The average mark is: {avg:.2f}")
        print(f"The number of A's recieved is: {count_a}")
        print(f"The number of B's recieved is: {count_b}")
        print(f"The number of C's recieved is: {count_c}")
        print(f"The number of D's recieved is: {count_d}")
        print(f"The number of F's recieved is: {count_f}")

    def sort_students_by_mark(self):
        grades = []
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if len(row) > 3:
                    grades.append((row[0], row[1], row[2], int(row[3])))
        
        sorted_grades = sorted(grades, key=lambda x: x[3], reverse=True)
        
        print("\nStudents sorted by marks:")
        for student in sorted_grades:
            print(f"Student: {student[0]}, Course: {student[1]}, Grade: {student[2]}, Mark: {student[3]}") 

def get_new_student_details():
    email_address = input("Please enter the email address of the new student: ")
    first_name = input("Please enter the first name of the new student: ")
    last_name = input("Please enter the last name of the new student: ")
    return email_address.strip(), first_name.strip(), last_name.strip()

def get_new_professor_details():
    email_address = input("Please enter the email address of the new professor: ")
    first_name = input("Please enter the first name of the new professor: ")
    last_name = input("Please enter the last name of the new professor: ")
    rank = input("Please enter the rank of the new professor: ")
    course_id = input("Please enter the new professor's course id: ")
    return email_address.strip(), first_name.strip(), last_name.strip(), rank.strip(), course_id.strip()

def get_new_course_details():
    course_id = input("Please enter the new course's id: ")
    course_name = input("Please enter the new course's name: ")
    description = input("Please enter the new course's description: ")
    return course_id.strip(), course_name.strip(), description.strip()

def get_grade():
    grade = input("Please enter the student's grade: ")
    mark = input("Please enter the student's mark: ")
    return grade.strip(), mark.strip()

def get_student_email():
    student_email = input("Please enter the student's email: ")
    return student_email

def get_professor_email():
    professor_email = input("Please enter the professor's email: ")
    return professor_email

def get_course_id():
    cid = input("Please enter the course id: ")
    return cid

def select_student_field():
    print("\nModify Student")
    print("1. Email")
    print("2. First Name")
    print("3. Last Name")
    choice = input("Select the field you would like to modify: ")
    if choice == '1':
        return 0
    if choice == '2':
        return 1
    if choice == '3':
        return 2
    else:
        print("Error - Invalid selection.")

def select_professor_field():
    print("\nModify Professor")
    print("1. Email")
    print("2. First Name")
    print("3. Last Name")
    print("4. Rank")
    print("5. Course id")
    choice = input("Select the field you would like to modify: ")
    if choice == '1':
        return 0
    if choice == '2':
        return 1
    if choice == '3':
        return 2
    if choice == '4':
        return 3
    if choice == '5':
        return 4
    else:
        print("Error - Invalid selection.")

def select_course_field():
    print("\nModify Course")
    print("1. Course id")
    print("2. Course Name")
    print("3. Description")
    choice = input("Select the field you would like to modify: ")
    if choice == '1':
        return 0
    if choice == '2':
        return 1
    if choice == '3':
        return 2
    else:
        print("Error - Invalid selection.")

def select_grade_field():
    print("\nModify Grade")
    print("1. Student email")
    print("2. Course id")
    print("3. Grade")
    print("4. Mark")
    choice = input("Select the field you would like to modify: ")
    if choice == '1':
        return 0
    if choice == '2':
        return 1
    if choice == '3':
        return 2
    if choice == '4':
        return 3
    else:
        print("Error - Invalid selection.")

def get_new_value():
    value = input("Please enter the new value: ")
    return value

def get_new_user():
    email = input("Please enter the new user's email: ")
    password = getpass.getpass("Please enter the new user's password: ")
    role = input("Please enter the new user's role: ")
    return email, password, role


def checkmygrade_main_menu():
    while True:
        columns = shutil.get_terminal_size().columns
        print("================================".center(columns))
        print("Welcome to CheckMyGrade".center(columns))
        print("================================".center(columns))
        print("\n CheckMyGrade Main Menu:")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        choice = input("Please select an option: ")
        if choice == '1':
            print("Executing option 1...")
            email_address = input("Enter your email address: ")
            password = getpass.getpass("Enter your password: ")
            login1=LoginUser(email_address.strip(),password.strip())
            status,user_id,password,role=login1.login()
            if status:
                print("Logging in...")
                if role == 'student':
                    student1 = Student('','','')
                    while True:
                        print("================================".center(columns))
                        print("Welcome to CheckMyGrade".center(columns))
                        print("================================".center(columns))
                        print("\n CheckMyGrade Student Main Menu:")
                        print("1. Update personal details")
                        print("2. Update password")
                        print("3. View grades")
                        print("4. View course details")
                        print("5. View professor details")
                        print("6. Exit")
                        choice = input("Please select an option: ")
                        if choice == '1':
                            print("\nUpdating personal details...")
                            semail = login1.user_id
                            field = select_student_field()
                            new_value = get_new_value()
                            student = Student('','','')
                            student.modify_student_record(semail, field, new_value)
                        if choice == '2':
                            new_password = getpass.getpass("Please enter your new password: ")
                            email = login1.user_id
                            old_password = login1.password
                            login1.change_password(email, old_password, new_password)
                        if choice == '3':
                            print("\nDisplaying Grades...")
                            grade = Grade('','','','')
                            student_email = login1.user_id
                            grade_list, course_ids = grade.find_student_grades(student_email)
                            if grade_list:
                                print(f"Grades for {student_email}:")
                                for course, grade, mark in grade_list:
                                    print(f"Course: {course}, Grade: {grade}, Mark: {mark}")
                            else:
                                print(f"No grades found for {student_email}.")
                        if choice == '4':
                            print("\nDisplaying Courses...")
                            grade = Grade('','','','')
                            student_email = login1.user_id
                            grade_list, course_ids = grade.find_student_grades(student_email) 
                            if course_ids:
                                course = Course('','','') 
                                course_details = course.find_student_courses(course_ids) 
                                if course_details:
                                    print(f"Courses for {student_email}:")
                                    for details in course_details:
                                        print(details)
                                else:
                                    print(f"No courses found for {student_email}.")
                            else:
                                print(f"No courses found for {student_email}.")
                        if choice == '5':
                            print("\nDisplaying Professors...")
                            grade = Grade('','','','')
                            student_email = login1.user_id
                            grade_list, course_ids = grade.find_student_grades(student_email)
                            if course_ids:
                                professor = Professor('','','','','')
                                professor_details = professor.find_student_professors(course_ids)
                                if professor_details:
                                    print(f"Professors for {student_email}:")
                                    for details in professor_details:
                                        print(details)
                                else:
                                    print(f"No professors found for {student_email}.")
                            else:
                                print(f"No professors found for {student_email}.")
                        if choice == '6':
                            print("\nLogging Out...")
                            break
                if role == 'professor':
                    while True:
                        print("================================".center(columns))
                        print("Welcome to CheckMyGrade".center(columns))
                        print("================================".center(columns))
                        print("\n CheckMyGrade Professor Main Menu:")
                        print("1. Update personal details")
                        print("2. Update password")
                        print("3. Add/delete/modify student")
                        print("4. Add/delete/modify grade")
                        print("5. View courses")
                        print("6. View course statistics")
                        print("7. Exit")
                        choice = input("Please select an option: ")
                        if choice == '1':
                            print("\nUpdating personal details...")
                            pemail = login1.user_id
                            field = select_professor_field()
                            new_value = get_new_value()
                            professor = Professor('','','','','')
                            professor.modify_professor(pemail, field, new_value)
                        if choice == '2':
                            new_password = getpass.getpass("Please enter your new password: ")
                            email = login1.user_id
                            old_password = login1.password
                            login1.change_password(email, old_password, new_password)
                        if choice == '3':
                            print("\n1. Add Student")
                            print("2. Delete Student")
                            print("3. Modify Student")
                            choice = input("Please select an option: ")
                            if choice == '1':
                                print("\nAdding new student...")
                                semail, sfirst, slast = get_new_student_details()
                                student = Student(semail, sfirst, slast)
                                student.add_new_student(semail, sfirst, slast)
                            elif choice == '2':
                                print("\nDeleting student...")
                                semail = get_student_email()
                                student = Student('','','')
                                student.delete_student(semail)
                            elif choice == '3':
                                print("\nModifying student record...")
                                semail = get_student_email()
                                field = select_student_field()
                                new_value = get_new_value()
                                student = Student('','','')
                                student.modify_student_record(semail, field, new_value)
                        if choice == '4':
                            print("\n1. Add Grade")
                            print("2. Delete Grade")
                            print("3. Modify Grade")
                            choice = input("Please select an option: ")
                            if choice == '1':
                                print("Adding grade...")
                                semail = get_student_email()
                                cid = get_course_id()
                                sgrade, smark = get_grade()
                                grade = Grade('','','','')
                                grade.add_grade(semail,cid,sgrade,smark)
                            elif choice == '2':
                                print("\nDeleting grade...")
                                semail = get_student_email()
                                cid = get_course_id()
                                grade = Grade('','','','')
                                grade.delete_grade(semail,cid)
                            elif choice == '3':
                                print("\nModifying grade record...")
                                semail = get_student_email()
                                cid = get_course_id()
                                field = select_grade_field()
                                new_value = get_new_value()
                                grade = Grade('','','','')
                                grade.modify_grade(semail, cid, field, new_value)
                        if choice == '5':
                            print("\nDisplaying Courses...")
                            pemail = login1.user_id
                            professor = Professor('', '', '', '', '')
                            course_ids = professor.get_professor_course_ids(pemail) 
                            if course_ids:
                                course = Course('','','') 
                                course_details = course.show_courses_by_professor(course_ids) 
                                if course_details:
                                    print(f"Courses taught by {pemail}:")
                                    for details in course_details:
                                        print(details)
                                else:
                                    print(f"No courses found for {pemail}.")
                            else:
                                print(f"No courses found for {pemail}.")
                        if choice == '6':
                            cid = input("Please enter the id of the course you would like to view: ")
                            grade = Grade('','','','')
                            grade.average_grade_by_course(cid)
                        if choice == '7':
                            print("\nLogging Out...")
                            break
                if role == 'admin':
                    while True:
                        print("================================".center(columns))
                        print("Welcome to CheckMyGrade".center(columns))
                        print("================================".center(columns))
                        print("\n CheckMyGrade Admin Main Menu:")
                        print("1. View all professor records")
                        print("2. View all course records")
                        print("3. View all student records")
                        print("4. Add/delete/modify professor")
                        print("5. Add/delete/modify course")
                        print("6. Add/delete/modify student")
                        print("7. View grades by course")
                        print("8. View students sorted by mark")
                        print("9. View students sorted by email")
                        print("10. Exit")
                        choice = input("Please select an option: ")
                        if choice == '1':
                            professor1 = Professor('', '', '', '', '')
                            professor1.display_professors()
                        if choice == '2':
                            course1 = Course('', '', '')
                            course1.display_courses()
                        if choice == '3':
                            student1 = Student('', '', '')
                            student1.display_student_records()
                        if choice == '4':
                            print("\n1. Add Professor")
                            print("2. Delete Professor")
                            print("3. Modify Professor")
                            choice = input("Please select an option: ")
                            if choice == '1':
                                print("\nAdding new professor...")
                                pemail, pfirst, plast, prank, pcourseid = get_new_professor_details()
                                professor = Professor(pemail, pfirst, plast, prank, pcourseid)
                                professor.add_new_professor(pemail, pfirst, plast, prank, pcourseid)
                            elif choice == '2':
                                print("\nDeleting professor...")
                                pemail = get_professor_email()
                                professor = Professor('','','','','')
                                professor.delete_professor(pemail)
                            elif choice == '3':
                                print("\nModifying professor record...")
                                pemail = get_professor_email()
                                field = select_professor_field()
                                new_value = get_new_value()
                                professor = Professor('','','','','')
                                professor.modify_professor(pemail, field, new_value)
                        if choice == '5':
                            print("\n1. Add Course")
                            print("2. Delete Course")
                            print("3. Modify Course")
                            choice = input("Please select an option: ")
                            if choice == '1':
                                print("\nAdding new course...")
                                cid, cname, cdescription = get_new_course_details()
                                course = Course(cid, cname, cdescription)
                                course.add_new_course(cid, cname, cdescription)
                            elif choice == '2':
                                print("\nDeleting course...")
                                cid = get_course_id()
                                course = Course('','','')
                                course.delete_course(cid)
                            elif choice == '3':
                                print("\nModifying course record...")
                                cid = get_course_id()
                                field = select_course_field()
                                new_value = get_new_value()
                                course = Course('','','')
                                course.modify_course(cid, field, new_value)
                        if choice == '6':
                            print("\n1. Add Student")
                            print("2. Delete Student")
                            print("3. Modify Student")
                            choice = input("Please select an option: ")
                            if choice == '1':
                                print("\nAdding new student...")
                                semail, sfirst, slast = get_new_student_details()
                                student = Student(semail, sfirst, slast)
                                student.add_new_student(semail, sfirst, slast)
                            elif choice == '2':
                                print("\nDeleting student...")
                                semail = get_student_email()
                                student = Student('','','')
                                student.delete_student(semail)
                            elif choice == '3':
                                print("\nModifying student record...")
                                semail = get_student_email()
                                field = select_student_field()
                                new_value = get_new_value()
                                student = Student('','','')
                                student.modify_student_record(semail, field, new_value)
                        if choice == '7':
                            cid = input("Please enter the id of the course you would like to view: ")
                            grade = Grade('','','','')
                            grade.grades_by_course(cid)
                        if choice == '8':
                            grade = Grade('','','','')
                            grade.sort_students_by_mark()
                        if choice == '9':
                            student = Student('','','')
                            student.sort_students_by_email()
                        if choice == '10':
                            print("\nLogging Out...")
                            break
        if choice == '2':
            print("Signup for Check My Grade:")
            email, password, role = get_new_user()
            login = LoginUser('','')
            login.register_new_user(email,password,role)
        if choice == '3':
            print("Exiting app... Goodbye!")
            break

if __name__ == '__main__':
    checkmygrade_main_menu()

    