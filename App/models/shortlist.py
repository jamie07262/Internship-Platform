from App.database import db
from App.models.staff import Staff

class Shortlist(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id', ondelete='CASCADE'), nullable=False, unique=True)

    internship = db.relationship('Internship', back_populates='shortlist')
    staff = db.relationship('Staff', backref='shortlists', lazy=True) 
    entries = db.relationship("ShortlistEntry", backref="shortlist", cascade="all, delete-orphan")

    def __init__(self, staff_id, internship_id):
        self.staff_id = staff_id
        self.internship_id = internship_id

    def __repr__(self):
        return f'<Shortlist entries: {len(self.entries)}>'