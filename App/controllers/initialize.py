from App.database import db
from App.controllers.staff import create_staff
from App.controllers.employer import create_employer, accept_student, reject_student
from App.controllers.student import create_student
from App.controllers.internship import create_internship_position
from App.controllers.shortlist import create_shortlist
from App.controllers.shortlistEntry import add_student_to_shortlist


def initialize():
    db.drop_all()
    db.create_all()

    # Creating sample data
    staff = create_staff("sally", "sallypass", "sally@staff.com")
    staff2 = create_staff("pam", "pampass", "pam@staff.com")

    employer = create_employer("Unit Trust", "password", "unit.trust@unit.com", "Unit Trust Ltd")
    employer2 = create_employer("evee", "eveepass", "evee@evee.com", "Evee Systems")

    student = create_student("johndoe", "johndoepass", "john.doe@student.com", "John", "Doe", "Java, Python, React")
    student2 = create_student("acelaw", "acepass", "ace.law@student.com", "Ace", "Law", "Python, R, SQL")

    internship = create_internship_position(
        int(employer.id), "Frontend Developer", "Work on React projects", 3
    )

    internship2 = create_internship_position(
        int(employer2.id), "Data Analytics", "Analyze data and build dashboards", 6
    )
    shortlist_result1 = create_shortlist(int(staff.id), int(internship.id))
    shortlist_result2 = create_shortlist(int(staff2.id), int(internship2.id))

    john_to_frontend = add_student_to_shortlist(int(staff.id), 1, int(student.id))
    john_to_data = add_student_to_shortlist(int(staff2.id), 2, int(student.id))
    
    ace_to_data = add_student_to_shortlist(int(staff2.id), 2, int(student2.id))
    
    # Update shortlist entry statuses using employer accept/reject functions
    accept_student(int(employer.id), 1, int(student.id))  # Unit Trust accepts John Doe for Frontend Developer
    reject_student(int(employer2.id), 2, int(student.id))  # Evee Systems rejects John Doe for Data Analytics
    accept_student(int(employer2.id), 2, int(student2.id))  # Evee Systems accepts Ace Law for Data Analytics
