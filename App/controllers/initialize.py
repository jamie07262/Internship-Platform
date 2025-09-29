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
    # Create staff (ID=1)
    staff = create_staff("sally", "sallypass", "sally@staff.com")
    # print(f"Created staff with ID: {staff.id } Name: {staff.username}")
    # Create staff (ID=2)
    staff2 = create_staff("pam", "pampass", "pam@staff.com")
    # print(f"Created staff with ID: {staff2.id } Name: {staff2.username}")
    # Create employer (ID=3)
    employer = create_employer("Unit Trust", "password", "unit.trust@unit.com", "Unit Trust Ltd")
    # print(f"Created employer with ID: {employer.id} Name: {employer.companyName}")
    # Create employer (ID=4)
    employer2 = create_employer("evee", "eveepass", "evee@evee.com", "Evee Systems")
    # print(f"Created employer with ID: {employer2.id} Name: {employer2.companyName}")
    # Create student (ID=5)
    student = create_student("johndoe", "johndoepass", "john.doe@student.com", "John", "Doe", "Java, Python, React")
    # print(f"Created student with ID: {student.id} Name: {student.firstName} {student.lastName}")
    # Create student (ID=6)
    student2 = create_student("acelaw", "acepass", "ace.law@student.com", "Ace", "Law", "Python, R, SQL")
    # print(f"Created student with ID: {student2.id} Name: {student2.firstName} {student2.lastName}")
    # Create internship for Unit Trust (ID=1)
    internship = create_internship_position(
        int(employer.id), "Frontend Developer", "Work on React projects", 3
    )
    # print(f"Created internship with ID: {internship.id} Title: {internship.title} for Employer: {employer.companyName}")
    
    # Create internship for Evee Systems (ID=2)
    internship2 = create_internship_position(
        int(employer2.id), "Data Analytics", "Analyze data and build dashboards", 6
    )
    # print(f"Created internship with ID: {internship2.id} Title: {internship2.title} for Employer: {employer2.companyName}")
    
    # Create shortlist for Frontend Developer internship (by staff sally - ID=1)
    shortlist_result1 = create_shortlist(int(staff.id), int(internship.id))
    # print(f"Shortlist creation result: {shortlist_result1}")
    
    # Create shortlist for Data Analytics internship (by staff pam - ID=2)
    shortlist_result2 = create_shortlist(int(staff2.id), int(internship2.id))
    # print(f"Shortlist creation result: {shortlist_result2}")
    
    # Add John Doe (ID=5) to both shortlists
    # Add to Frontend Developer shortlist (shortlist ID=1) - ACCEPTED
    john_to_frontend = add_student_to_shortlist(int(staff.id), 1, int(student.id))
    # print(f"Adding John Doe to Frontend Developer shortlist: {john_to_frontend}")
    
    # Add to Data Analytics shortlist (shortlist ID=2) - REJECTED
    john_to_data = add_student_to_shortlist(int(staff2.id), 2, int(student.id))
    # print(f"Adding John Doe to Data Analytics shortlist: {john_to_data}")
    
    # Add Ace Law (ID=6) only to Data Analytics shortlist (shortlist ID=2) - ACCEPTED
    ace_to_data = add_student_to_shortlist(int(staff2.id), 2, int(student2.id))
    # print(f"Adding Ace Law to Data Analytics shortlist: {ace_to_data}")
    
    # Update shortlist entry statuses using employer accept/reject functions
    accept_student(int(employer.id), 1, int(student.id))  # Unit Trust accepts John Doe for Frontend Developer
    reject_student(int(employer2.id), 2, int(student.id))  # Evee Systems rejects John Doe for Data Analytics
    accept_student(int(employer2.id), 2, int(student2.id))  # Evee Systems accepts Ace Law for Data Analytics
