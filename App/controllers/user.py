from App.models import User
from App.database import db
from rich.table import Table

def create_user(username, password, email, firstName=None, lastName=None):
    newuser = User(username=username, password=password, email=email, firstName=firstName, lastName=lastName)
    db.session.add(newuser)
    db.session.commit()
    return newuser

# def get_user_by_username(username):
#     result = db.session.execute(db.select(User).filter_by(username=username))
#     return result.scalar_one_or_none()

# def get_user(id):
#     return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

# def update_user(id, username):
#     user = get_user(id)
#     if user:
#         user.username = username
#         # user is already in the session; no need to re-add
#         db.session.commit()
#         return True
#     return None

# def list_users():
#     users = get_all_users()
#     table = Table(title="All Users")
#     table.add_column("ID", style="cyan")
#     table.add_column("Username", style="magenta")
#     table.add_column("Email", style="green")
#     table.add_column("Type", style="blue")
#     for user in users:
#         table.add_row(
#             str(user.id),
#             user.username,
#             user.email,
#             getattr(user, "type", "N/A")
#         )
#     return table
