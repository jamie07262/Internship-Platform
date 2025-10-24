# Internship Platform

An app for staff to shortlist students to internship opportunities created by employers who can accept or reject student.

## Demonstration

https://github.com/user-attachments/assets/f3705681-911b-46ef-af02-45a7a14afd42

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
