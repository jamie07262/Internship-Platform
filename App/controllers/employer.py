from App.database import db
from App.models import Employer, Internship, ShortlistEntry, Shortlist, Student
from rich.table import Table
from sqlalchemy.exc import SQLAlchemyError

def create_employer(username: str, password: str, email: str, companyName: str) -> str:
    try:
        employer = Employer(username, password, email, companyName)
        db.session.add(employer)
        db.session.commit()
        return employer
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error creating employer: {e}"


def view_shortlist(employer_id: int) -> Table:
    employer = db.session.get(Employer, employer_id)
    if not employer:
        table = Table(title="Employer Not Found")
        return table
    
    # Get all shortlists for all internships created by this employer
    shortlists = db.session.execute(
        db.select(Shortlist)
        .join(Internship, Shortlist.internship_id == Internship.id)
        .filter(Internship.employer_id == employer_id)
    ).scalars().all()

    table = Table(title=f"{employer.companyName} - All Shortlists")    
    table.add_column("Shortlist ID", style="magenta")
    table.add_column("Internship ID", style="cyan")
    table.add_column("Internship Title", style="green")
    table.add_column("Student ID", style="cyan")
    table.add_column("Student Name", style="yellow")
    table.add_column("Student Email", style="blue")
    table.add_column("Student Skills", style="magenta")
    table.add_column("Status", style="red")

    for shortlist in shortlists:
        internship = db.session.get(Internship, shortlist.internship_id)
        entries = db.session.execute(
            db.select(ShortlistEntry).filter_by(shortlist_id=shortlist.id)
        ).scalars().all()
        
        if entries:
            for entry in entries:
                student = db.session.get(Student, entry.student_id)
                table.add_row(
                    str(shortlist.id),
                    str(shortlist.internship_id),
                    internship.title if internship else "N/A",
                    str(student.id) if student else "N/A",
                    f"{student.firstName} {student.lastName}" if student else "N/A",
                    student.email if student else "N/A",
                    student.skills if student else "N/A",
                    entry.status
                )
        else:
            table.add_row(
                str(shortlist.id),
                str(shortlist.internship_id),
                internship.title if internship else "N/A",
                "No students",
                "N/A",
                "N/A", 
                "N/A",
                "N/A"
            )
    return table

def accept_student(employer_id: int, internship_id: int, student_id: int) -> str:
    try:
        # Checking if the internship belongs to the employer
        internship = db.session.get(Internship, internship_id)
        if not internship:
            return f"Internship not found for ID {internship_id}."
        if internship.employer_id != employer_id:
            return f"Employer ID {employer_id} is not authorized to manage internship ID {internship_id}."
        
        shortlist = db.session.execute(
            db.select(Shortlist).filter_by(internship_id=internship_id)
        ).scalar_one_or_none()

        if not shortlist:
            return f"No shortlist found for internship ID {internship_id}."
        
        entry = db.session.execute(
            db.select(ShortlistEntry).filter_by(shortlist_id=shortlist.id, student_id=student_id)
        ).scalar_one_or_none()

        if not entry:
            return f"No shortlist entry for student ID {student_id} in internship ID {internship_id}."
        
        # Update the status to "accepted"
        entry.status = "accepted"
        db.session.commit()
        return f"Student ID {student_id} has been accepted by {internship.employer.username}."
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error accepting student: {e}"

def reject_student(employer_id: int, internship_id: int, student_id: int) -> str:
    try:
        # Checking if the internship belongs to the employer
        internship = db.session.get(Internship, internship_id)
        if not internship:
            return f"Internship not found for ID {internship_id}."
        if internship.employer_id != employer_id:
            return f"Employer ID {employer_id} is not authorized to manage internship ID {internship_id}."
        
        shortlist = db.session.execute(
            db.select(Shortlist).filter_by(internship_id=internship_id)
        ).scalar_one_or_none()

        if not shortlist:
            return f"No shortlist found for internship ID {internship_id}."
        
        entry = db.session.execute(
            db.select(ShortlistEntry).filter_by(shortlist_id=shortlist.id, student_id=student_id)
        ).scalar_one_or_none()

        if not entry:
            return f"No shortlist entry for student ID {student_id} in internship ID {internship_id}."
        
        # Update the status to "rejected"
        entry.status = "rejected"
        db.session.commit()
        return f"Student ID {student_id} has been rejected by {internship.employer.username}."
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error rejecting student: {e}"
