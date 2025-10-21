# blue prints are imported 
# explicitly instead of using *
from .index import index_views
from .auth import auth_views
# from .admin import setup_admin
from .employer import employer_views
from .staff import staff_views
from .student import student_views
from .internship import internship_views
from .shortlist import shortlist_views
from .shortlistEntry import shortlistEntry_views


views = [index_views, auth_views, employer_views, staff_views, student_views, shortlist_views, shortlistEntry_views, internship_views] 
# blueprints must be added to this list