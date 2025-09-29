![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Internship Platform

An app for staff to shortlist students to internship opportunities created by employers who can accept or reject student.

## Core Functionality

1. **(Employer)** Create internship positions
2. **(Staff)** Add students to internship position shortlists
3. **(Employer)** Accept/reject students from shortlists
4. **(Student)** View shortlisted positions and employer responses

# CLI Commands Reference

## General Commands

| Command            | Description                    |
| ------------------ | ------------------------------ |
| `flask init`       | Initialize the database        |
| `flask list-users` | List all users in the system   |
| `flask help`       | Show CLI help for all commands |

## Staff Commands

Staff members can manage students and create shortlists for internship positions.

| Command                                                          | Description                                   | Example                                        |
| ---------------------------------------------------------------- | --------------------------------------------- | ---------------------------------------------- |
| `flask staff create <username> <password> <email>`               | Create a new staff member                     | `flask staff create bob bobpass bob@staff.com` |
| `flask staff list-students`                                      | List all students in the system               | `flask staff list-students`                    |
| `flask staff search-students <skill_keyword>`                    | Search students by skill keyword              | `flask staff search-students Python`           |
| `flask staff view-internships`                                   | View all available internship positions       | `flask staff view-internships`                 |
| `flask staff create-shortlist <staff_id> <internship_id>`        | Create a shortlist for an internship          | `flask staff create-shortlist 1 1`             |
| `flask staff add-student <staff_id> <shortlist_id> <student_id>` | Add a student to a shortlist                  | `flask staff add-student 1 1 1`                |
| `flask staff view-shortlists <staff_id>`                         | View all shortlists created by a staff member | `flask staff view-shortlists 1`                |

## Employer Commands

Employers can manage their company's internship positions and review/respond to student applications.

| Command                                                                    | Description                                    | Example                                                         |
| -------------------------------------------------------------------------- | ---------------------------------------------- | --------------------------------------------------------------- |
| `flask employer create <username> <password> <email> <companyname>`        | Create a new employer account                  | `flask employer create TechQ techqpass techq@q.com "TechQ Ltd"` |
| `flask employer view-shortlist <employer_id>`                              | View all shortlists for employer's internships | `flask employer view-shortlist 1`                               |
| `flask employer accept-student <employer_id> <internship_id> <student_id>` | Accept a student into an internship            | `flask employer accept-student 1 1 1`                           |
| `flask employer reject-student <employer_id> <internship_id> <student_id>` | Reject a student from an internship            | `flask employer reject-student 1 1 1`                           |

## Internship Commands

Manage internship positions and opportunities.

| Command                                                                  | Description                      | Example                                                                 |
| ------------------------------------------------------------------------ | -------------------------------- | ----------------------------------------------------------------------- |
| `flask internship create <employer_id> <title> <description> <duration>` | Create a new internship position | `flask internship create 1 "Software Intern" "Work on Java projects" 3` |

## Student Commands

Students can create profiles and view their shortlist status.

| Command                                                                              | Description                                 | Example                                                                                        |
| ------------------------------------------------------------------------------------ | ------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `flask student create <username> <password> <firstname> <lastname> <email> <skills>` | Create a new student profile                | `flask student create janedoe janedoepass Jane Doe jane.doe@student.com "Angular, TypeScript"` |
| `flask student view-my-shortlist <student_id>`                                       | View your shortlist status and applications | `flask student view-my-shortlist 1`                                                            |

## Typical Workflow

### 1. Initial Setup

```bash
# Initialize the database
flask init

# Create a staff member
flask staff create bob bobpass bob@staff.com

# Create an employer
flask employer create TechQ techqpass techq@q.com "TechQ Ltd"

# Create a student
flask student create janedoe janedoepass Jane Doe jane.doe@student.com "Python, JavaScript"
```

### 2. Create Internship Opportunities

```bash
# Employer creates internship positions
flask internship create 1 "Software Developer Intern" "Full-stack development position" 6

# Staff views available internships
flask staff view-internships
```

### 3. Manage Shortlists

```bash
# Staff creates shortlists for internships
flask staff create-shortlist 1 1

# Staff searches for suitable students
flask staff search-students Python

# Staff adds students to shortlists
flask staff add-student 1 1 1
```

### 4. Employer Review Process

```bash
# Employer views shortlisted students
flask employer view-shortlist 1

# Employer accepts or rejects students
flask employer accept-student 1 1 1
# or
flask employer reject-student 1 1 1
```

### 5. Student Status Check

```bash
# Student checks their application status
flask student view-my-shortlist 1
```

# Dependencies

- Python3/pip3
- Packages listed in requirements.txt

# Installing Dependencies

```bash
$ pip install -r requirements.txt
```

# Configuration Management

Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py

```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py

```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# Flask Commands

The application uses Flask CLI commands to interact with the system. All commands are defined in `wsgi.py` and use the Click library for command-line interface functionality.

## Creating Custom Commands

You can create custom management commands by adding them to `wsgi.py`:

```python
# inside wsgi.py

user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

app.cli.add_command(user_cli) # add the group to the cli
```

Then execute the command using Flask CLI:

```bash
$ flask user create bob bobpass
```

## Database Models

The system includes the following main entities:

- **User**: Base user model with authentication
- **Staff**: Staff members who manage shortlists
- **Employer**: Company representatives who post internships
- **Student**: Students applying for internships
- **Internship**: Available internship positions
- **Shortlist**: Collections of students for specific internships
- **ShortlistEntry**: Individual student entries in shortlists

# Running the Project

_For development run the serve command (what you execute):_

```bash
$ flask run
```

_For production using gunicorn (what the production server executes):_

```bash
$ gunicorn wsgi:app
```

# Deploying

You can deploy your version of this app to render by clicking on the "Deploy to Render" link above.

# Initializing the Database

When connecting the project to a fresh empty database, ensure the appropriate configuration is set then run the following command. This initializes all database tables and sets up the system for use.

```bash
$ flask init
```

This command must also be executed once when running the app on cloud platforms by accessing the console and running the command in the container.

# Database Migrations

If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration

Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

```python
@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
```

You can then execute all user tests as follows

```bash
$ flask test user
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```

## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
