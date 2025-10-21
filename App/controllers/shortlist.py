from App.models import Shortlist, Staff, Internship
from App import db
from sqlalchemy.exc import SQLAlchemyError

def create_shortlist(staff_id: int, internship_id: int):
    try:
        # Check if the staff and internship exist
        staff = db.session.get(Staff, staff_id)
        internship = db.session.get(Internship, internship_id)

        if not staff:
            return f"Staff with ID {staff_id} does not exist"
        if not internship:
            return f"Internship with ID {internship_id} does not exist"

        # Check if a shortlist already exists for this internship
        existing = db.session.execute(
            db.select(Shortlist).filter_by(internship_id=internship_id)
        ).scalar_one_or_none()
        if existing:
            return f"duplicate shortlist"

        shortlist = Shortlist(staff_id=staff_id, internship_id=internship_id)
        db.session.add(shortlist)
        db.session.commit()
        return shortlist
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error creating shortlist: {e}"

