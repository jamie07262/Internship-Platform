from App.models import ShortlistEntry, Shortlist, Student, Staff, Internship
from App import db
from sqlalchemy.exc import SQLAlchemyError

def add_student_to_shortlist(staff_id: int, shortlist_id: int, student_id: int) -> str:
    try:
        # Check if the shortlist student and staff exist
        shortlist = db.session.get(Shortlist, shortlist_id)
        student = db.session.get(Student, student_id)
        staff = db.session.get(Staff, staff_id)

        if not shortlist:
            return f"Shortlist with ID {shortlist_id} does not exists"
        if not student:
            return f"Student with ID {student_id} does not exist"
        if not staff:
            return f"Staff with ID {staff_id} does not exist"
        
        internship = db.session.get(Internship, shortlist.internship_id)
        if not internship:
            return f"Internship with ID {shortlist.internship_id} does not exist"

        # Add the student to the shortlist
        shortlist_entry = ShortlistEntry(shortlist_id=shortlist_id, student_id=student_id, staff_id=staff_id)
        db.session.add(shortlist_entry)
        db.session.commit()
        return (
            f"Student {student.firstName} {student.lastName} added to"
            f" Internship: {internship.title} (ID: {internship.id}), shortlisted by Staff ID {staff_id}"
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error adding student to shortlist: {e}"


