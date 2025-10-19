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
    
def list_students(staff_id: int) -> dict:
    """Return students data in JSON format for API endpoints"""
    try:
        # Verify staff exists and is authorized
        staff = db.session.get(Staff, staff_id)
        if not staff:
            return {"error": f"Staff with ID {staff_id} does not exist"}
        
        students = db.session.execute(db.select(Student)).scalars().all()
        students_data = []
        
        for student in students:
            students_data.append(student.get_json())
        
        return {
            "students": students_data,
            "total": len(students_data)
        }
    except SQLAlchemyError as e:
        return {"error": f"Database error: {str(e)}"}

def view_shortlists(staff_id: int) -> dict:
    """View all shortlists and return as JSON"""
    try:
        shortlists = db.session.execute(
            db.select(Shortlist)
        ).scalars().all()

        shortlists_data = []
        for shortlist in shortlists:
            internship = db.session.get(Internship, shortlist.internship_id)
            company_name = internship.employer.companyName if internship and internship.employer else "N/A"
            internship_title = f"{internship.title} ({internship.id})" if internship else "N/A"
            entries = db.session.execute(
                db.select(ShortlistEntry).filter_by(shortlist_id=shortlist.id)
            ).scalars().all()
            
            if entries:
                for entry in entries:
                    student = db.session.get(Student, entry.student_id)
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
            else:
                shortlists_data.append({
                    "shortlist_id": shortlist.id,
                    "staff_id": shortlist.staff_id,
                    "company_name": company_name,
                    "internship_title": internship_title,
                    "student_id": "TBD",
                    "student_name": "TBD",
                    "student_email": "TBD",
                    "student_skills": "TBD",
                    "status": "TBD"
                })
        
        return {
            "shortlists": shortlists_data,
            "total": len(shortlists_data)
        }
    except SQLAlchemyError as e:
        return {"error": f"Database error: {str(e)}"}

#view all internship positions
def view_internship_positions(staff_id: int) -> dict:
    """View all internship positions and return as JSON"""
    try:
        # Verify staff exists and is authorized
        staff = db.session.get(Staff, staff_id)
        if not staff:
            return {"error": f"Staff with ID {staff_id} does not exist"}
        
        internships = db.session.execute(db.select(Internship)).scalars().all()
        internships_data = []
        
        for internship in internships:
            internship_json = internship.get_json()
            internship_json["company_name"] = internship.employer.companyName if internship.employer else "N/A"
            internships_data.append(internship_json)
        
        return {
            "internships": internships_data,
            "total": len(internships_data)
        }
    except SQLAlchemyError as e:
        return {"error": f"Database error: {str(e)}"}

# #search students by skill keyword if list is too long
# def search_students_by_skill(skill_keyword: str) -> dict:
#     """Search students by skill keyword and return as JSON"""
#     try:
#         students = db.session.execute(
#             db.select(Student).filter(Student.skills.ilike(f"%{skill_keyword}%"))
#         ).scalars().all()

#         students_data = []
#         for student in students:
#             students_data.append({
#                 "id": student.id,
#                 "firstName": student.firstName,
#                 "lastName": student.lastName,
#                 "email": student.email if student.email else "N/A",
#                 "skills": student.skills if student.skills else "N/A"
#             })
        
#         return {
#             "students": students_data,
#             "total": len(students_data),
#             "search_keyword": skill_keyword
#         }
#     except SQLAlchemyError as e:
#         return {"error": f"Database error: {str(e)}"}