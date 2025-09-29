import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from rich.table import Table
from rich.console import Console

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers.user import list_users
from App.controllers.student import create_student, view_my_shortlists
from App.controllers.employer import (
    create_employer,
    view_shortlist as employer_view_shortlist,
    accept_student,
    reject_student
)
from App.controllers.internship import create_internship_position
from App.controllers.staff import (
    create_staff,
    list_students,
    search_students_by_skill,
    view_shortlists as staff_view_shortlists,
    view_internship_positions
)
from App.controllers.shortlist import create_shortlist
from App.controllers.shortlistEntry import add_student_to_shortlist
from App.controllers.initialize import ( initialize )

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')

# This command lists all users in the system
@app.cli.command("list-users", help="List all users in the system")
def list_users_command():
    table = list_users()
    console = Console()
    print("---------------------------------------------------------------------------")
    console.print(table)
    print("---------------------------------------------------------------------------")

@app.cli.command("help", help="Show CLI help for all commands")
def show_help():
    table = Table(title="Flask CLI Command Reference", show_lines=True)
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")

    table.add_row("flask init", "Initialize the database")
    table.add_row("flask list-users", "List all users in the system")
    
    # Staff commands
    table.add_row("flask staff create <username> <password> <email>", "Create a new staff member")
    table.add_row("flask staff list-students", "List all students")
    table.add_row("flask staff search-students <skill_keyword>", "Search students by skill")
    table.add_row("flask staff create-shortlist <staff_id> <internship_id>", "Create a shortlist for an internship")
    table.add_row("flask staff add-student <staff_id> <shortlist_id> <student_id>", "Add a student to a shortlist")
    table.add_row("flask staff view-shortlists <staff_id>", "View all shortlists for a staff member")
    table.add_row("flask staff view-internships", "View all internship positions")

    # Employer commands
    table.add_row("flask employer create <username> <password> <email> <companyname>", "Create a new employer")
    table.add_row("flask employer view-shortlist <employer_id>", "View all shortlists for an employer")
    table.add_row("flask employer accept-student <employer_id> <internship_id> <student_id>", "Accept a student into an internship")
    table.add_row("flask employer reject-student <employer_id> <internship_id> <student_id>", "Reject a student from an internship")

    # Internship commands
    table.add_row("flask internship create <employer_id> <title> <description> <duration>", "Create an internship position")

    # Student commands
    table.add_row("flask student create <username> <password> <firstname> <lastname> <email> <skills>", "Create a new student")
    table.add_row("flask student view-my-shortlist <student_id>", "View your shortlist(s)")

    console = Console()
    console.print(table)

#### STAFF COMMANDS ####
staff_cli = AppGroup('staff', help='Staff object commands')
@staff_cli.command("create", help="Creates a staff member")
@click.argument("username", default="bob")
@click.argument("password", default="bobpass`")
@click.argument("email", default="bob@staff.com")
def create_staff_command(username, password, email):
    result = create_staff(username, password, email)
    print("---------------------------------------------------------------------------")
    print(result)
    print("\nNext: Create an employer with:")
    print("  flask employer create <username> <password> <email> <companyname>")
    print("---------------------------------------------------------------------------")
   

@staff_cli.command("view-internships", help="View all internship positions")
def view_internships_command():
    table = view_internship_positions()
    console = Console()
    print("---------------------------------------------------------------------------")
    console.print(table)
    print("\nNext: As staff, create a shortlist for an internship with:")
    print("  flask staff create-shortlist <staff_id> <internship_id>")
    print("---------------------------------------------------------------------------")

@staff_cli.command("create-shortlist", help="Create a shortlist for an internship")
@click.argument("staff_id", type=int)
@click.argument("internship_id", type=int)
def create_shortlist_command(staff_id, internship_id):
    result = create_shortlist(staff_id, internship_id)
    print("---------------------------------------------------------------------------")
    print(result)
    print("\nNext: As staff, search for students by skill with:")
    print("  flask staff search-students <skill_keyword>")
    print("Or view all students with:")
    print("  flask staff list-students")
    print("---------------------------------------------------------------------------")

@staff_cli.command("list-students", help="List all students")
def list_students_command():
    table = list_students()
    console = Console()
    print("---------------------------------------------------------------------------")
    console.print(table)
    print("\nNext: As staff, add a student to a shortlist with:")
    print("  flask staff add-student <staff_id> <shortlist_id> <student_id>")
    print("---------------------------------------------------------------------------")


@staff_cli.command("search-students", help="Search students by skill")
@click.argument("skill_keyword", default="Python")  
def search_students_command(skill_keyword):
    table = search_students_by_skill(skill_keyword)
    console = Console()
    print("---------------------------------------------------------------------------")
    console.print(table)
    print("\nNext: As staff, add a student to a shortlist with:")
    print("  flask staff add-student <staff_id> <shortlist_id> <student_id>")
    print("---------------------------------------------------------------------------")


@staff_cli.command("add-student", help="Add a student to a shortlist")
@click.argument("staff_id", type=int)
@click.argument("shortlist_id", type=int)
@click.argument("student_id", type=int)
def add_student_command(staff_id, shortlist_id, student_id):
    result = add_student_to_shortlist(staff_id, shortlist_id, student_id)
    print("---------------------------------------------------------------------------")
    print(result)
    print("\nNext: As employer, view your internship shortlist with:")
    print("  flask employer view-shortlist <employer_id>")
    print("---------------------------------------------------------------------------")


@staff_cli.command("view-shortlists", help="View all shortlists")
@click.argument("staff_id", type=int)
def view_shortlist_command(staff_id):
    table = staff_view_shortlists(staff_id)
    console = Console()
    print("---------------------------------------------------------------------------")
    console.print(table)
    print("---------------------------------------------------------------------------")



#### EMPLOYER COMMANDS ####
employer_cli = AppGroup('employer', help='Employer object commands')
@employer_cli.command("create", help="Creates an employer")
@click.argument("username", default="TechQ")
@click.argument("password", default="techqpass")
@click.argument("email", default="techq@q.com")
@click.argument("companyname", default="TechQ Ltd")
def create_employer_command(username, password, email, companyname):
    result = create_employer(username, password, email, companyname)
    print("---------------------------------------------------------------------------")
    print("\nNext: Create a student with:")
    print("  flask student create <firstname> <lastname> <username> <password> <email> <skills>")
    print("---------------------------------------------------------------------------")
   

@employer_cli.command("view-shortlist", help="View all shortlists for an employer")
@click.argument("employer_id", type=int)
def view_shortlist_command(employer_id):
    table = employer_view_shortlist(employer_id)
    console = Console()
    print("---------------------------------------------------------------------------")
    console.print(table)
    print("\nNext: As employer, accept or reject a student with:")
    print("  flask employer accept-student <employer_id> <internship_id> <student_id>")
    print("  flask employer reject-student <employer_id> <internship_id> <student_id>")
    print("---------------------------------------------------------------------------")

@employer_cli.command("accept-student", help="Accept a student into an internship")
@click.argument("employer_id", type=int)
@click.argument("internship_id", type=int)
@click.argument("student_id", type=int)
def accept_student_command(employer_id, internship_id, student_id):
    result = accept_student(employer_id, internship_id, student_id)
    print("---------------------------------------------------------------------------")
    print(result)   
    print("\nNext: As student, view your shortlist with:")
    print("  flask student view-my-shortlist <student_id>")
    print("---------------------------------------------------------------------------")


@employer_cli.command("reject-student", help="Reject a student from an internship")     
@click.argument("employer_id", type=int)
@click.argument("internship_id", type=int)
@click.argument("student_id", type=int)
def reject_student_command(employer_id, internship_id, student_id):
    result = reject_student(employer_id, internship_id, student_id)
    print("---------------------------------------------------------------------------")
    print(result)
    print("\nNext: As student, view your shortlist with:")
    print("  flask student view-my-shortlist <student_id>")
    print("---------------------------------------------------------------------------")



#### INTERNSHIP COMMANDS ####
internship_cli = AppGroup('internship', help='Internship object commands')
@internship_cli.command("create", help="Creates an internship position")
@click.argument("employer_id", type=int)
@click.argument("title", default="Software Intern")
@click.argument("description", default="Work on Java projects")
@click.argument("duration", type=int, default=3)
def create_internship_command(employer_id, title, description, duration):
    result = create_internship_position(employer_id, title, description, duration)
    print("---------------------------------------------------------------------------")
    print(result)
    print("\nNext: As staff, view all internship positions with:")
    print("flask staff view-internships")
    print("---------------------------------------------------------------------------")
   

#### STUDENT COMMANDS ####
student_cli = AppGroup('student', help='Student object commands')
@student_cli.command("create", help="Creates a student")
@click.argument("firstname", default="Jane")
@click.argument("lastname", default="Doe")
@click.argument("username", default="janedoe")
@click.argument("password", default="janedoepass")
@click.argument("email", default="jane.doe@student.com")
@click.argument("skills", default="Angular, TypeScript")
def create_student_command(username, password, firstname, lastname, email, skills):
    result = create_student(username, password, email, firstname, lastname, skills)
    print("---------------------------------------------------------------------------")
    print(result)
    print("\nNext: Create an internship for this employer with:")
    print("  flask internship create <employer_id> <title> <description> <duration>")
    print("---------------------------------------------------------------------------")
   

@student_cli.command("view-my-shortlist", help="View my shortlists")
@click.argument("student_id", type=int)
def view_my_shortlist_command(student_id):
    table = view_my_shortlists(student_id)
    console = Console()
    print("---------------------------------------------------------------------------")
    console.print(table)
    print("---------------------------------------------------------------------------")

app.cli.add_command(staff_cli)
app.cli.add_command(employer_cli)
app.cli.add_command(internship_cli)
app.cli.add_command(student_cli)

