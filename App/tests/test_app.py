from flask import jsonify
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Staff, Employer
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass", "bob@example.com", "Bob", "Frank") #added more attributes to this test
        assert user.username == "bob"
        assert user.email == "bob@example.com"
        assert user.firstName == "Bob"
        assert user.lastName == "Frank"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass", "bob@example.com", "Bob", "Frank") #added more attributes to this test
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, 
                                         "username":"bob", 
                                         "email":"bob@example.com", 
                                         "firstName":"Bob", 
                                         "lastName":"Frank"}) # added more features for json
    
    def test_hashed_password(self):
        password = "bobpass"
        #hashed = generate_password_hash(password, method='sha256') #not sure the use of this hash so commented out 
        user = User("bob", password,"bob@example.com", "Bob", "Frank") #added more attributes to this test
        assert user.password != password

    def test_check_password(self):
        password = "bobpass"
        user = User("bob", password, "bob@example.com", "Bob", "Frank") #added more attributes to this test
        assert user.check_password(password)

    def test_new_student(self): #added this test for student model
        student = Student("student1", "studentpass", "student@mail.com","Jane", "Doe", "Coding Design") 
        assert student.username == "student1"
        assert student.email == "student@mail.com"
        assert student.firstName == "Jane"
        assert student.lastName == "Doe"
        assert student.skills == "Coding Design"

    def test_new_staff(self):
        staff = Staff("trudy", "trudypass", "trudy@mail.com")
        assert staff.username == "trudy"
        assert staff.email == "trudy@mail.com"

    def test_new_employer(self): #added this test for employer model
        employer = Employer("warren","warrenpass","warren@mail.com","Microsoft")
        assert employer.username == "warren"
        assert employer.email == "warren@mail.com"
        assert employer.companyName == "Microsoft"




'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


class UsersIntegrationTests(unittest.TestCase):
    maxDiff = None

    def test_create_user(self):
        user = create_user("rick", "rickpass","rick@example.com", "Rick", "Sanchez")
        users = get_all_users()
        self.assertIn(user, users)

    def test_create_student(self):
        student = create_student("student", "studentpass","student@mail.com", "Jane", "Doe", "Coding Design")
        users = get_all_users()
        self.assertIn(student, users)

    def test_create_staff(self):
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        users = get_all_users()
        self.assertIn(staff, users)

    def test_create_employer(self):
        employer = create_employer("warren","warrenpass","warren@mail.com","Microsoft")
        users = get_all_users()
        self.assertIn(employer, users)

    def test_get_all_users_json(self):
        user = create_user("mimi", "mimipass","mimi@example.com", "Mimi", "Smith")
        users_json = get_all_users_json()
        self.assertIn({"id": 1, 
                       "username":"mimi", 
                       "email":"mimi@example.com", 
                       "firstName":"Mimi", 
                       "lastName":"Smith"}, users_json)

    # Tests data changes in the database
    def test_update_user(self):
        user = create_user("rick", "rickpass","rick@example.com", "Rick", "Sanchez")
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        
    def test_login(self):
        user = create_user("bob", "bobpass","bob@example.com", "Bob", "Frank")
        assert login("bob", "bobpass") != None

    def test_authenticate(self):
        student = create_student("student", "studentpass","student@mail.com","Jane", "Doe", "Coding Design")
        assert authenticate("student", "studentpass") == student

    def test_jwt_authenticate(self):
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        assert jwt_authenticate("trudy", "trudypass") != None

    def test_is_staff(self):
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        assert is_staff(staff.id) == True

    def test_is_employer(self):
        employer = create_employer("warren","warrenpass","warren@mail.com","Microsoft")    
        assert is_employer(employer.id) == True

    def test_is_student(self):
        student = create_student("student", "studentpass","student@mail.com","Jane", "Doe", "Coding Design")    
        assert is_student(student.id) == True

    def test_logout(self):
        user = create_user("bob", "bobpass","bob@example.com", "Bob", "Frank")
        response = login("bob", "bobpass")
        response = jsonify({"msg": "logout successful"})
        assert logout(response) != None

    def test_list_students(self):
        student = create_student("student", "studentpass","student@mail.com", "Jane", "Doe", "Coding Design")
        student = student.get_json()
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        students_list = list_students(staff.id)
        self.assertIn(student, students_list["students"])

    def test_create_internship(self):
        employer = create_employer("warren","warrenpass","warren@mail.com","Microsoft")
        internship = create_internship_position(employer.id, "Software Intern", "Work on cool projects", 12)
        assert internship != None

    def test_view_internship_positions(self):
        employer = create_employer("warren","warrenpass","warren@mail.com","Microsoft")
        internship = create_internship_position(employer.id, "Software Intern", "Work on cool projects", 12)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        positions = view_internship_positions(staff.id)
        self.assertDictEqual(positions, {"internships": [{"company_name": "Microsoft",
                                                          "description": "Work on cool projects",
                                                          "duration": 12,
                                                          "employer_id": 1,
                                                          "id": 1,
                                                          "title": "Software Intern"}], 
                                                          "total": 1})
        
    def test_create_shortlist(self):
        employer = create_employer("warren","warrenpass","warren@mail.com","Microsoft")
        internship = create_internship_position(employer.id, "Software Intern", "Work on cool projects", 12)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(staff.id, internship.id)
        assert shortlist != None

    def test_view_shortlists(self):
        employer = create_employer("warren","warrenpass","warren@mail.com","Microsoft")
        internship = create_internship_position(employer.id, "Software Intern", "Work on cool projects", 12)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(staff.id, internship.id)
        shortlists = view_shortlists(staff.id)
        self.assertDictEqual(shortlists, {"shortlists": [{"shortlist_id": 1, 
                                                          "staff_id": 2, 
                                                          "company_name": "Microsoft",
                                                        "internship_title": "Software Intern (1)", 
                                                        "student_id": "TBD", 
                                                        "student_name": "TBD",
                                                        "student_email": "TBD", 
                                                        "student_skills": "TBD", 
                                                        "student_skills": "TBD", 
                                                        "status": "TBD"}], 
                                                        "total": 1})
        
    def test_create_shortlist_entry(self):
        employer = create_employer("warren","warrenpass","warren@mail.com","Microsoft")
        internship = create_internship_position(employer.id, "Software Intern", "Work on cool projects", 12)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(staff.id, internship.id)
        student = create_student("student", "studentpass","student@mail.com", "Jane", "Doe", "Coding Design")
        shortlist_entry = add_student_to_shortlist(staff.id, shortlist.id, student.id)
        assert shortlist_entry != None

    def test_view_my_shortlists(self):
        employer = create_employer("warren","warrenpass","warren@mail.com","Microsoft")
        internship = create_internship_position(employer.id, "Software Intern", "Work on cool projects", 12)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(staff.id, internship.id)
        student = create_student("student", "studentpass","student@mail.com", "Jane", "Doe", "Coding Design")
        shortlist_entry = add_student_to_shortlist(staff.id, shortlist.id, student.id)
        my_shortlist = view_my_shortlists(student.id)
        self.assertDictEqual(my_shortlist, {"student_id": 3, "shortlists": [{"company_name": "Microsoft",
                                                            "internship_title": "Software Intern",
                                                            "internship_id": 1, 
                                                            "student_id": 3,
                                                            "student_name": "Jane Doe", 
                                                            "student_email": "student@mail.com",
                                                            "student_skills": "Coding Design", 
                                                            "status": "pending"}], 
                                                            "total": 1})
        
    def test_view_shortlist(self):
        employer = create_employer("warren","warrenpass","warren@mail.com","Microsoft")
        internship = create_internship_position(employer.id, "Software Intern", "Work on cool projects", 12)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(staff.id, internship.id)
        student = create_student("student", "studentpass","student@mail.com", "Jane", "Doe", "Coding Design")
        shortlist_entry = add_student_to_shortlist(staff.id, shortlist.id, student.id)
        my_shortlist = view_shortlist(employer.id)
        self.assertDictEqual(my_shortlist, {"employer": {"id": 1, 
                                                         "company_name": 
                                                         "Microsoft"},
                                             "shortlists": [{"shortlist_id": 1,
                                                             "internship_title": "Software Intern",
                                                            "internship_id": 1, 
                                                            "student_id": 3, 
                                                            "student_name": "Jane Doe", 
                                                            "student_email": "student@mail.com", 
                                                            "student_skills": "Coding Design", 
                                                            "status": "pending"}], 
                                                            "total": 1})
        
    def test_accept_student(self):
        employer = create_employer("warren","warrenpass","warren@mail.com","Microsoft")
        internship = create_internship_position(employer.id, "Software Intern", "Work on cool projects", 12)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(staff.id, internship.id)
        student = create_student("student", "studentpass","student@mail.com", "Jane", "Doe", "Coding Design")
        shortlist_entry = add_student_to_shortlist(staff.id, shortlist.id, student.id)
        assert accept_student(employer.id, internship.id, student.id) == f"Student ID {student.id} has been accepted by {internship.employer.username}."

    def test_reject_student(self):
        employer = create_employer("warren","warrenpass","warren@mail.com","Microsoft")
        internship = create_internship_position(employer.id, "Software Intern", "Work on cool projects", 12)
        staff = create_staff("trudy", "trudypass","trudy@mail.com")
        shortlist = create_shortlist(staff.id, internship.id)
        student = create_student("student", "studentpass","student@mail.com", "Jane", "Doe", "Coding Design")
        shortlist_entry = add_student_to_shortlist(staff.id, shortlist.id, student.id)
        assert reject_student(employer.id, internship.id, student.id) == f"Student ID {student.id} has been rejected by {internship.employer.username}."
