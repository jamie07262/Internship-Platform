from App.database import db
from App.models import Employer, Internship
from rich.table import Table
from sqlalchemy.exc import SQLAlchemyError

# create internship position
def create_internship_position(employer_id: int, title:str, description: str, duration:int) -> str:
    employer: Employer | None = db.session.get(Employer, employer_id)
    if employer is None:
        return f"Employer with ID {employer_id} does not exist"

    try:
        internship = Internship(employer.id, title, description, duration)
        db.session.add(internship)
        db.session.commit()
        return internship
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error creating internship position: {e}"


