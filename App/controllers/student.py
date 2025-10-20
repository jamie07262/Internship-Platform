from App.models import Student, Shortlist, ShortlistEntry
from App import db
from sqlalchemy.exc import SQLAlchemyError

#student being created and is considered an applicant for internships
def create_student(username, password, email, firstName, lastName, skills): #removed None defaults for firstName and lastName
    try:
        student = Student(username, password, email, firstName, lastName, skills)
        db.session.add(student)
        db.session.commit()
        return student
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error creating student: {e}"

# student views their shortlisted internships
def view_my_shortlists(student_id: int) -> dict:
    try:
        from App.models import Internship, Employer

        entries = db.session.execute(
            db.select(ShortlistEntry).filter_by(student_id=student_id)
        ).scalars().all()

        shortlists_data = []
        for entry in entries:
            shortlist = db.session.get(Shortlist, entry.shortlist_id)
            internship = None
            employer = None
            internship_title = "N/A"
            internship_id = "N/A"
            company_name = "N/A"
            if shortlist:
                internship = db.session.get(Internship, shortlist.internship_id)
                if internship:
                    internship_title = internship.title
                    internship_id = internship.id
                    employer = db.session.get(Employer, internship.employer_id)
                    if employer:
                        company_name = employer.companyName
            student = db.session.get(Student, entry.student_id)
            
            shortlists_data.append({
                "company_name": company_name if employer else "N/A",
                "internship_title": internship_title,
                "internship_id": internship_id,
                "student_id": student.id if student else None,
                "student_name": f"{student.firstName} {student.lastName}" if student else "N/A",
                "student_email": student.email if student else "N/A",
                "student_skills": student.skills if student else "N/A",
                "status": entry.status
            })
        
        return {
            "student_id": student_id,
            "shortlists": shortlists_data,
            "total": len(shortlists_data)
        }
    except SQLAlchemyError as e:
        return {"error": f"Database error: {str(e)}"}