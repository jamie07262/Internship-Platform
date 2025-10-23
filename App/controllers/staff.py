from App.models import Staff, Shortlist, ShortlistEntry, Student, Internship
from App import db
from sqlalchemy.exc import SQLAlchemyError

def create_staff(username: str, password: str, email: str):
    try:
        staff = Staff(username, password, email)
        db.session.add(staff)
        db.session.commit()
        return staff
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error creating staff: {e}"
    
def list_students(staff_id: int):
    try:
        staff = Staff.query.get(staff_id)
        if not staff:
            return None
        
        students = Student.query.all()
        students_data = []
        
        for student in students:
            students_data.append(student.get_json())
        return students_data
    except SQLAlchemyError as e:
        return f"Error listing students: {e}"

def view_shortlists(staff_id: int):
    try:
        # Check if staff exists
        staff = Staff.query.get(staff_id)
        if not staff:
            return None
        
        shortlists = Shortlist.query.all()

        shortlists_data = []
        for shortlist in shortlists:
            # Get associated internship and entries
            internship = Internship.query.get(shortlist.internship_id)
            entries = ShortlistEntry.query.filter_by(shortlist_id=shortlist.id).all()
            # Get company name and internship title
            company_name = internship.employer.companyName if internship and internship.employer else "N/A"
            internship_title = f"{internship.title} ({internship.id})" if internship else "N/A"

            if entries:
                for entry in entries:
                    student = Student.query.get(entry.student_id)
                    shortlists_data.append({
                        "shortlist_id": shortlist.id,
                        "staff_id": shortlist.staff_id,
                        "company_name": company_name,
                        "internship_title": internship_title,
                        "student_id": student.id if student else None,
                        "student_name": f"{student.firstName} {student.lastName}" if student else "N/A",
                        "student_email": student.email if student else "N/A",
                        "student_skills": student.skills if student else "N/A",
                        "status": entry.status
                    })
        return shortlists_data
    except SQLAlchemyError as e:
        return f"Error viewing shortlists: {e}"

#view all internship positions
def view_internship_positions(staff_id: int):
    try:
        # Check if staff exists
        staff = Staff.query.get(staff_id)
        if not staff:
            return None
        
        internships = Internship.query.all()
        internships_data = []
        
        for internship in internships:
            internship_json = internship.get_json()
            internship_json["company_name"] = internship.employer.companyName if internship.employer else "N/A"
            internships_data.append(internship_json)
        return internships_data
    except SQLAlchemyError as e:
        return f"Error viewing internships: {e}"