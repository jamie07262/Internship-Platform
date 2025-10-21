from App.database import db
from App.models import Employer, Internship
from rich.table import Table
from sqlalchemy.exc import SQLAlchemyError

# create internship position
def create_internship_position(employer_id: int, title:str, description: str, duration:int):
    employer: Employer | None = db.session.get(Employer, employer_id)
    if employer is None:
        return f"Employer with ID {employer_id} does not exist"
    
    # Check if employer already has an internship with the same title, description, and duration
    existing_internship = db.session.execute(
        db.select(Internship).filter_by(
            employer_id=employer_id, 
            title=title, 
            description=description, 
            duration=duration
        )
    ).scalar_one_or_none()
    
    if existing_internship:
        return f"duplicate internship"


    try:
        internship = Internship(employer.id, title, description, duration)
        db.session.add(internship)
        db.session.commit()
        return internship
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error creating internship position: {e}"


