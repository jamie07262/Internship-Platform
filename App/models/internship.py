from App.database import db
from App.models.employer import Employer

class Internship(db.Model): 
    id = db.Column(db.Integer, primary_key=True)    
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.Integer, nullable=False)

    employer = db.relationship('Employer', backref=db.backref('internships', lazy=True))

    def __init__(self, employer_id, title, description, duration):
        self.employer_id = employer_id
        self.title = title
        self.description = description
        self.duration = duration
    
    def __repr__(self):
        return f'<Internship Position (ID: {self.id}) \'{self.title}\' created by {self.employer.username} (ID: {self.employer.id})>'