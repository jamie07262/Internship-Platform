from App.models import ShortlistEntry, Shortlist, Student, Staff, Internship
from App import db
from sqlalchemy.exc import SQLAlchemyError

def add_student_to_shortlist(staff_id: int, shortlist_id: int, student_id: int):
    try:
        # Check if the shortlist, student, staff and internship exist
        shortlist = Shortlist.query.get(shortlist_id)
        student = Student.query.get(student_id)
        staff = Staff.query.get(staff_id)
        internship = Internship.query.get(shortlist.internship_id) if shortlist else None

        if not shortlist or not student or not staff or not internship:
            return None

        # Check if student already in shortlist
        existing = ShortlistEntry.query.filter_by(shortlist_id=shortlist_id, student_id=student_id).first()
        if existing:
            return None

        # Add the student to the shortlist
        shortlist_entry = ShortlistEntry(shortlist_id=shortlist_id, student_id=student_id, staff_id=staff_id)
        db.session.add(shortlist_entry)
        db.session.commit()
        return shortlist_entry
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error adding student to shortlist: {e}"


