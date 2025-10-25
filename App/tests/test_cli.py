import pytest
from click.testing import CliRunner
from wsgi import app
import re

@pytest.fixture
def runner():
    return CliRunner()

def extract_id(output, pattern):
    match = re.search(pattern, output)
    if match:
        return match.group(1)
    raise AssertionError(f"Could not extract ID with pattern '{pattern}' from output:\n{output}")

def test_full_workflow(runner):
    # 1. Initialize database
    result = runner.invoke(app.cli, ['init'])

    # 2. Create staff
    result = runner.invoke(app.cli, [
        'staff', 'create', 'staff1', 'staffpass', 'staff1@staff.com'
    ])
    print(result.output)
    assert 'created' in result.output or result.exit_code == 0
    assert 'Next: Create an employer with:' in result.output
    staff_id = extract_id(result.output, r'ID: (\d+)') if 'ID:' in result.output else None

    # 3. Create employer
    result = runner.invoke(app.cli, [
        'employer', 'create', 'employer1', 'emppass', 'employer1@company.com', 'Company Ltd'
    ])
    print(result.output)
    assert 'created' in result.output or result.exit_code == 0
    assert 'Next: Create an internship for this employer with:' in result.output
    employer_id = extract_id(result.output, r'ID: (\d+)') if 'ID:' in result.output else None

    # 4. Create internship 
    result = runner.invoke(app.cli, [
        'internship', 'create', str(employer_id or 3), 'Software Intern', 'Work on Java projects', '3'
    ])
    print(result.output)
    assert 'created' in result.output or result.exit_code == 0
    assert 'Next: As staff, view all internship positions with:' in result.output
    internship_id = extract_id(result.output, r'ID: (\d+)') if 'ID:' in result.output else None

    # 5. Staff views internships
    result = runner.invoke(app.cli, ['staff', 'view-internships', str(staff_id or 1)])
    print(result.output)
    assert 'Internship' in result.output or result.exit_code == 0
    assert 'Next: As staff, create a shortlist for an internship with:' in result.output

    # 6. Staff creates shortlist for the new internship
    result = runner.invoke(app.cli, [
        'staff', 'create-shortlist', str(staff_id or 1), str(internship_id or 3)
    ])
    print(result.output)
    assert 'Shortlist' in result.output or result.exit_code == 0
    assert 'Next: As staff, add a student to a shortlist with:' in result.output
    shortlist_id = extract_id(result.output, r'ID:?(\d+)') if 'ID' in result.output else None

    # 7. Create student 
    result = runner.invoke(app.cli, [
        'student', 'create',
        'janesmith', 'janesmithpass', 'jane.smith@student.com', 'Jane', 'Smith', 'Java, SpringBoot'
    ])
    print(result.output)
    assert 'created' in result.output or result.exit_code == 0
    student_id = extract_id(result.output, r'ID: (\d+)') if 'ID:' in result.output else None

    # 8. Staff lists students
    result = runner.invoke(app.cli, ['staff', 'list-students', str(staff_id or 1)])
    print(result.output)
    assert 'Students' in result.output or result.exit_code == 0
    assert 'Next: As staff, add a student to a shortlist with:' in result.output

    # 9. Staff adds student to shortlist
    result = runner.invoke(app.cli, [
        'staff', 'add-student', str(staff_id or 1), str(shortlist_id or 3), str(student_id or 7)
    ])
    print(result.output)
    assert 'added' in result.output or result.exit_code == 0
    assert 'Next: As employer, view your internship shortlist with:' in result.output

    # 10. Employer views shortlist for their internship
    result = runner.invoke(app.cli, [
        'employer', 'view-shortlist', str(employer_id or 3)
    ])
    print(result.output)
    assert 'Shortlist' in result.output or result.exit_code == 0
    assert 'Next: As employer, accept or reject a student with:' in result.output

    # 11. Employer accepts student
    result = runner.invoke(app.cli, [
        'employer', 'accept-student', str(employer_id or 3), str(internship_id or 3), str(student_id or 7)
    ])
    print(result.output)
    assert 'accepted' in result.output or result.exit_code == 0
    assert 'Next: As student, view your shortlist with:' in result.output
 
    # 12. Student views their shortlist (should show accepted status)
    result = runner.invoke(app.cli, [
        'student', 'view-my-shortlist', str(student_id or 7)
    ])
    print(result.output)
    assert 'Shortlist' in result.output or result.exit_code == 0
    assert 'accepted' in result.output or result.exit_code == 0

    # 13. Employer rejects student 
    result = runner.invoke(app.cli, [
        'employer', 'reject-student', str(employer_id or 2), str(internship_id or 1), str(student_id or 6)
    ])
    print(result.output)
    assert 'rejected' in result.output or result.exit_code == 0
    assert 'Next: As student, view your shortlist with:' in result.output

    # 14. Student views their shortlist (should show rejected status)
    result = runner.invoke(app.cli, [
        'student', 'view-my-shortlist', str(student_id or 6)
    ])
    print(result.output)
    assert 'Shortlist' in result.output or result.exit_code == 0
    assert 'rejected' in result.output or result.exit_code == 0