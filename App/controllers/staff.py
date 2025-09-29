from App.models import Staff, Shortlist, ShortlistEntry, Student, Internship
from App import db
from rich.table import Table
from sqlalchemy.exc import SQLAlchemyError

def create_staff(username: str, password: str, email: str) -> str:
    try:
        staff = Staff(username, password, email)
        db.session.add(staff)
        db.session.commit()
        return staff
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error creating staff: {e}"
    
def list_students() -> Table:
    students = db.session.execute(db.select(Student)).scalars().all()
    table = Table(title="Students")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("First Name", style="magenta")
    table.add_column("Last Name", style="green")
    table.add_column("Email", style="yellow")
    table.add_column("Skills", style="blue")

    for student in students:
        table.add_row(str(student.id), student.firstName, student.lastName, student.email if student.email else "N/A", student.skills if student.skills else "N/A")
    return table

def view_shortlists(staff_id: int) -> Table:
    shortlists = db.session.execute(
        db.select(Shortlist)
    ).scalars().all()

    table = Table(title=f"Shortlists")
    table.add_column("Shortlist ID", style="cyan")
    table.add_column("Staff ID", style="cyan")
    table.add_column("Company Name", style="magenta")
    table.add_column("Internship Title (Internship ID)", style="green")
    table.add_column("Student ID", style="cyan")
    table.add_column("Student Name", style="yellow")
    table.add_column("Student Email", style="blue")
    table.add_column("Student Skills", style="magenta")
    table.add_column("Status", style="red")

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
                table.add_row(
                    str(shortlist.id),
                    str(shortlist.staff_id),
                    company_name,
                    internship_title,
                    str(student.id),
                    f"{student.firstName} {student.lastName}",
                    student.email,
                    student.skills,
                    entry.status
                )
        else:
            # No students yet, show metadata and "TBD" for student columns
            table.add_row(
                str(shortlist.id),
                str(shortlist.staff_id),
                company_name,
                internship_title,
                "TBD",
                "TBD",
                "TBD",
                "TBD",
                "TBD"
            )
    return table

#view all internship positions
def view_internship_positions() -> Table:

    internships = db.session.execute(db.select(Internship)).scalars().all()
    table = Table(title="All Internship Positions")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Employer ID", style="magenta")
    table.add_column("Company Name", style="green")
    table.add_column("Title", style="green")
    table.add_column("Description", style="yellow")
    table.add_column("Duration (months)", justify="right", style="blue")

    for internship in internships:
        company_name = internship.employer.companyName if internship.employer else "N/A"
        table.add_row(
            str(internship.id),
            str(internship.employer_id),
            company_name,
            internship.title,
            internship.description if internship.description else "N/A",
            str(internship.duration)
        )
    return table

#search students by skill keyword if list is too long
def search_students_by_skill(skill_keyword: str) -> Table:

    students = db.session.execute(
        db.select(Student).filter(Student.skills.ilike(f"%{skill_keyword}%"))
    ).scalars().all()

    table = Table(title=f"Students with skill: {skill_keyword}")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("First Name", style="magenta")
    table.add_column("Last Name", style="green")
    table.add_column("Email", style="yellow")
    table.add_column("Skills", style="blue")

    for student in students:
        table.add_row(
            str(student.id),
            student.firstName,
            student.lastName,
            student.email,
            student.skills
        )
    return table