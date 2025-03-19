import unittest
import csv
import os
import time
from Lab1 import Student, Professor, Course

class TestCheckMyGrades(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.student_file = '/Users/louisas/Documents/Data 200 - Python/Lab1/Student.csv'
        cls.professor_file = '/Users/louisas/Documents/Data 200 - Python/Lab1/Professor.csv'
        cls.course_file = '/Users/louisas/Documents/Data 200 - Python/Lab1/Course.csv'
        
        cls.student = Student(cls.student_file, "", "")
        with open(cls.student_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["email", "first_name", "last_name"])
            for i in range(1000):
                writer.writerow([f"student{i}@school.com", f"First{i}", f"Last{i}"])

        cls.professor = Professor(cls.professor_file, "", "", "", "")
        with open(cls.professor_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["email", "first_name", "last_name", "rank", "course_id"])
            for i in range(50):
                writer.writerow([f"prof{i}@school.com", f"ProfFirst{i}", f"ProfLast{i}", "Associate", f"C{i}"])
 
        cls.course = Course(cls.course_file, "", "")
        with open(cls.course_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["course_id", "course_name", "description"])
            for i in range(50):
                writer.writerow([f"C{i}", f"Course{i}", "A sample course"])

    def test_add_student(self):
        self.student.add_new_student("new_student@example.com", "New", "Student")
        self.assertTrue(self._student_exists("new_student@example.com"))

    def test_delete_student(self):
        self.student.delete_student("student500@school.com")
        self.assertFalse(self._student_exists("student500@school.com"))

    def test_modify_student(self):
        self.student.modify_student_record("student600@school.com", 1, "UpdatedName")
        print("Checking modification for student600@school.com:")
        print(self._student_exists("student600@school.com", "UpdatedName"))
        self.assertTrue(self._student_exists("student600@school.com", "UpdatedName"))

    def test_search_student_records(self):
        start_time = time.time()
        self.student.display_student_records()
        end_time = time.time()
        print(f"Search Time: {end_time - start_time:.6f} seconds")
    
    def test_sort_students(self):
        start_time = time.time()
        students = sorted(self._load_students(), key=lambda x: x[0])
        end_time = time.time()
        print(f"Sort Time: {end_time - start_time:.6f} seconds")
        self.assertTrue(all(students[i][0] <= students[i+1][0] for i in range(len(students)-1)))

    def _student_exists(self, email, first_name=None):
        with open(self.student.file_path, 'r') as file:
            file_contents = file.readlines() 
            for row in file_contents:
                if email in row:
                    return first_name is None or first_name in row
        return False

    def _load_students(self):
        students = []
        with open(self.student.file_path, 'r') as file:
            for line in file:
                students.append(line.strip().split(","))
        return students
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup test files"""
        with open(cls.student_file, 'w', newline='') as file:
            pass 
        with open(cls.professor_file, 'w', newline='') as file:
            pass  
        with open(cls.course_file, 'w', newline='') as file:
            pass

if __name__ == '__main__':
    unittest.main()