from App.models.user import User
from App.database import db

class Employer(User):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    companyName = db.Column(db.String(120), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'employer',
    }

    def __init__(self, username, password, email, companyName):
        super().__init__(username, password, email)
        self.companyName = companyName

    def __repr__(self):
        return f"<Employer with ID {self.id} and username {self.username} ({self.companyName})>"