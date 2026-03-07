"""
Students Infrastructure — Repository.

Implements data access for the Student aggregate using Django ORM.
"""

from django.utils import timezone


class StudentRepository:
    """Repository for Student aggregate — wraps Django ORM."""

    def _get_model(self):
        from students.models import Student
        return Student

    def create(self, data: dict):
        Student = self._get_model()
        return Student.objects.create(**data)

    def get_by_id(self, student_id: int):
        Student = self._get_model()
        return Student.objects.get(pk=student_id)

    def list_by_company(self, company_id: int = None):
        Student = self._get_model()
        qs = Student.objects.all()
        if company_id:
            qs = qs.filter(company_id=company_id)
        return qs

    def update(self, student_id: int, data: dict):
        Student = self._get_model()
        data["updated_at"] = timezone.now()
        Student.objects.filter(pk=student_id).update(**data)
        return self.get_by_id(student_id)


class EnrollmentRepository:
    """Repository for Enrollment — manages student/modality associations."""

    def _get_model(self):
        from students.models import Enrollment
        return Enrollment

    def enroll(self, student_id: int, modality_id: int):
        Enrollment = self._get_model()
        enrollment, _ = Enrollment.objects.get_or_create(
            student_id=student_id,
            modality_id=modality_id,
            defaults={"active": True},
        )
        if not enrollment.active:
            enrollment.active = True
            enrollment.save(update_fields=["active"])
        return enrollment

    def unenroll(self, student_id: int, modality_id: int):
        Enrollment = self._get_model()
        Enrollment.objects.filter(student_id=student_id, modality_id=modality_id).update(active=False)

    def list_by_student(self, student_id: int):
        Enrollment = self._get_model()
        return Enrollment.objects.filter(student_id=student_id, active=True)
