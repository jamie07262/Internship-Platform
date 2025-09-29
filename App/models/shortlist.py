from App.database import db
from App.models.staff import Staff

class Shortlist(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), nullable=False)

    internship = db.relationship('Internship', backref=db.backref('shortlists', lazy=True))
    staff = db.relationship('Staff', lazy=True) 
    entries = db.relationship("ShortlistEntry", backref="shortlist", cascade="all, delete-orphan")

    def __init__(self, staff_id, internship_id):
        self.staff_id = staff_id
        self.internship_id = internship_id

    def __repr__(self):
        return f'<Shortlist entries: {len(self.entries)}>'