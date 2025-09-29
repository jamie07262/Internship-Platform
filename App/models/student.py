from App.models.user import User
from App.database import db

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    skills = db.Column(db.String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username, password, email, firstName, lastName, skills):
        super().__init__(username=username, password=password, email=email, firstName=firstName, lastName=lastName)
        self.skills = skills

    def __repr__(self):
        return f"<Student with ID {self.id} and username {self.username} ({self.firstName} {self.lastName}), skills={self.skills}>"