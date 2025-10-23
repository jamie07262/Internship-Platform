from App.models import Student, ShortlistEntry, Shortlist, Internship
from App import db
from sqlalchemy.exc import SQLAlchemyError

def create_student(username: str, password: str, email: str, firstName: str, lastName: str, skills: str):
    try:
        student = Student(username, password, email, firstName, lastName, skills)
        db.session.add(student)
        db.session.commit()
        return student
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error creating student: {e}"

def view_my_shortlists(student_id: int):
    try:
        # Check if student exists
        student = Student.query.get(student_id)
        if not student:
            return None
        # Get all shortlist entries for the student
        entries = ShortlistEntry.query.filter_by(student_id=student_id).all()
        shortlists_data = []
        
        for entry in entries:
            shortlist = Shortlist.query.get(entry.shortlist_id)
            if shortlist:
                internship = Internship.query.get(shortlist.internship_id)
                employer = internship.employer if internship else None
                
                shortlists_data.append({
                    "company_name": employer.companyName if employer else "Unknown", 
                    "internship_title": internship.title if internship else "Unknown",
                    "description": internship.description if internship else "N/A",
                    "status": entry.status,
                    "student_id": student_id, 
                    "student_name": f"{student.firstName} {student.lastName}",
                    "student_email": student.email,
                    "student_skills": student.skills
                })
        return  shortlists_data
    except SQLAlchemyError as e:
        return f"Error viewing my shortlists: {e}"