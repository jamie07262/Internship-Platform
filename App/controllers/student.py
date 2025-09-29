# from flask import Blueprint, render_template, request, redirect, url_for, flash
from App.models import Student, Shortlist, ShortlistEntry
from App import db
from rich.table import Table

#student applying for internship
def create_student(username, password, email, firstName, lastName, skills):
    student = Student(username, password, email, firstName, lastName, skills)
    db.session.add(student)
    db.session.commit()
    return student

def view_my_shortlists(student_id: int) -> Table:
    from App.models import Internship, Employer

    entries = db.session.execute(
        db.select(ShortlistEntry).filter_by(student_id=student_id)
    ).scalars().all()

    table = Table(title=f"My Shortlists")
    table.add_column("Company Name", style="magenta")
    table.add_column("Internship (ID)", style="green")
    table.add_column("Student ID", style="cyan")
    table.add_column("Student Name", style="yellow")
    table.add_column("Student Email", style="blue")
    table.add_column("Student Skills", style="magenta")
    table.add_column("Status", style="red")

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
        table.add_row(
            company_name if employer else "N/A",
            f"{internship_title} ({internship_id})" if internship else "N/A",
            str(student.id) if student else "N/A",
            f"{student.firstName} {student.lastName}" if student else "N/A",
            student.email if student else "N/A",
            student.skills if student else "N/A",
            entry.status
        )
    return table