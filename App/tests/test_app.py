import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Staff, Employer
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
)


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
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "email":"bob@example.com", "firstName":"Bob", "lastName":"Frank"}) # added more features for json
    
    def test_hashed_password(self):
        password = "mypass"
        #hashed = generate_password_hash(password, method='sha256') #not sure the use of this hash so commented out 
        user = User("bob", password,"bob@example.com", "Bob", "Frank") #added more attributes to this test
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
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
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass","bob@example.com", "Bob", "Frank")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass","bob@example.com", "Bob", "Frank")
        get_all_users_json()
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        

