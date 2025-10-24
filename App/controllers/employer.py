from App.database import db
from App.models import Employer, Internship, ShortlistEntry, Shortlist, Student
from sqlalchemy.exc import SQLAlchemyError

def create_employer(username: str, password: str, email: str, companyName: str):
    try:
        employer = Employer(username, password, email, companyName)
        db.session.add(employer)
        db.session.commit()
        return employer
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error creating employer: {e}"


def view_shortlist(employer_id: int):
    try:
        # Get employer and their internships
        employer = Employer.query.get(employer_id)
        if not employer:
            return None
        
        internships = Internship.query.filter_by(employer_id=employer_id).all()
        shortlisted_data = []
        
        for internship in internships:
            shortlists = Shortlist.query.filter_by(internship_id=internship.id).all()

            for shortlist in shortlists:
                entries = ShortlistEntry.query.filter_by(shortlist_id=shortlist.id).all()
                
                for entry in entries:
                    student = Student.query.get(entry.student_id)
                    if student:
                        shortlisted_data.append({
                            "shortlist_id": shortlist.id, 
                            "internship_title": internship.title,
                            "internship_id": internship.id,
                            "student_id": student.id,
                            "student_name": f"{student.firstName} {student.lastName}",
                            "student_email": student.email,
                            "student_skills": student.skills,
                            "status": entry.status
                        })
        
        return shortlisted_data
    except SQLAlchemyError as e:
        return f"Error viewing shortlist: {e}"

def accept_student(employer_id: int, internship_id: int, student_id: int) -> bool:
    try:
        # Get the internship and verify employer 
        internship = Internship.query.get(internship_id)
        if not internship:
            return False
        if int(internship.employer_id) != int(employer_id):
            return False

        shortlist = Shortlist.query.filter_by(internship_id=internship_id).first()

        if not shortlist:
            return False

        entry = ShortlistEntry.query.filter_by(shortlist_id=shortlist.id, student_id=student_id).first()

        if not entry:
            return False

        entry.status = "accepted"
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        return False

def reject_student(employer_id: int, internship_id: int, student_id: int) -> bool:
    try:
        # Get the internship and verify employer
        internship = Internship.query.get(internship_id)
        if not internship:
            return False
        if int(internship.employer_id) != int(employer_id):
            return False
        
        shortlist = Shortlist.query.filter_by(internship_id=internship_id).first()
        if not shortlist:
            return False

        entry = ShortlistEntry.query.filter_by(shortlist_id=shortlist.id, student_id=student_id).first()
        if not entry:
            return False

        entry.status = "rejected"
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        return False
