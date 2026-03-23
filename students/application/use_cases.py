"""
Students Application Use Cases.

Orchestrates domain objects to fulfill application commands for the Alunos domain.
"""

from students.infrastructure.repositories import StudentRepository, EnrollmentRepository


class CreateStudentUseCase:
    """Use case: register a new student."""

    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def execute(self, data: dict):
        return self.repository.create(data)


class GetStudentUseCase:
    """Use case: retrieve a student by ID."""

    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def execute(self, student_id: int):
        return self.repository.get_by_id(student_id)


class ListStudentsUseCase:
    """Use case: list all students for a given company."""

    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def execute(self, company_id: int = None):
        return self.repository.list_by_company(company_id)


class EnrollStudentUseCase:
    """Use case: enroll a student in a modality."""

    def __init__(self, repository: EnrollmentRepository):
        self.repository = repository

    def execute(self, student_id: int, modality_id: int):
        return self.repository.enroll(student_id, modality_id)


class UnenrollStudentUseCase:
    """Use case: remove a student from a modality."""

    def __init__(self, repository: EnrollmentRepository):
        self.repository = repository

    def execute(self, student_id: int, modality_id: int):
        return self.repository.unenroll(student_id, modality_id)


class UpdateStudentUseCase:
    """Use case: update student profile."""

    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def execute(self, student_id: int, data: dict):
        return self.repository.update(student_id, data)
