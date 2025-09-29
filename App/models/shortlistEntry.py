from App.database import db

class ShortlistEntry(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    shortlist_id = db.Column(db.Integer, db.ForeignKey('shortlist.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')

def __init__(self, staff_id, student_id, shortlist_id):
    self.staff_id = staff_id
    self.shortlist_id = shortlist_id
    self.student_id = student_id


def __repr__(self):
    return f'<ShortlistEntry StaffID: {self.staff_id}, ShortlistID: {self.shortlist_id}, StudentID: {self.student_id}, Status: {self.status}>'