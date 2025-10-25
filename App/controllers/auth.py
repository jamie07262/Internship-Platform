from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, unset_jwt_cookies, verify_jwt_in_request

from App.models import User
from App.database import db
from App.models import Staff, Employer, Student

def login(username, password):
  result = db.session.execute(db.select(User).filter_by(username=username))
  user = result.scalar_one_or_none()
  if user and user.check_password(password):
    # Store ONLY the user id as a string in JWT 'sub'
    return create_access_token(identity=str(user.id))
  return None

def authenticate(username, password):
  staff = Staff.query.filter_by(username=username).first()
  if staff and staff.check_password(password):
    return staff
  
  employer = Employer.query.filter_by(username=username).first()
  if employer and employer.check_password(password):
    return employer
  
  student = Student.query.filter_by(username=username).first()
  if student and student.check_password(password):
    return student

  return None

def jwt_authenticate(username, password):
  user = User.query.filter_by(username=username).one_or_none()
  if user and user.check_password(password):
    user_type = None

    if Staff.query.filter_by(id=user.id).first():
      user_type = 'staff'
    elif Employer.query.filter_by(id=user.id).first():
      user_type = 'employer'
    elif Student.query.filter_by(id=user.id).first():
      user_type = 'student'

    return create_access_token(identity=str(user.id), additional_claims={'user_type': user_type, 'username': username})
  return None

def is_staff(identity):
  user = User.query.filter_by(id=identity).first()
  if user and Staff.query.filter_by(id=user.id).first():
    return True
  return False

def is_employer(identity):
  user = User.query.filter_by(id=identity).first()
  if user and Employer.query.filter_by(id=user.id).first():
    return True
  return False

def is_student(identity):
  user = User.query.filter_by(id=identity).first()
  if user and Student.query.filter_by(id=user.id).first():
    return True
  return False  

def logout(response):
    unset_jwt_cookies(response)
    return response

def setup_jwt(app):
  jwt = JWTManager(app)

  # Always store a string user id in the JWT identity (sub),
  # whether a User object or a raw id is passed.
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    user_id = getattr(identity, "id", identity)
    return str(user_id) if user_id is not None else None

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    # Cast back to int primary key
    try:
      user_id = int(identity)
    except (TypeError, ValueError):
      return None
    return db.session.get(User, user_id)

  return jwt


# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          identity = get_jwt_identity()
          user_id = int(identity) if identity is not None else None
          current_user = db.session.get(User, user_id) if user_id is not None else None
          is_authenticated = current_user is not None
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)