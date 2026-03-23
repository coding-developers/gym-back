from rest_framework import viewsets
from core.renderers import DestroyMixin
from .models import Student, Enrollment
from .serializers import StudentSerializer, EnrollmentSerializer


class StudentViewSet(DestroyMixin, viewsets.ModelViewSet):
    """
    ViewSet for the Alunos (Students) domain.
    Provides CRUD operations for gym member management.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class EnrollmentViewSet(DestroyMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing student enrollments in modalities.
    """
    queryset = Enrollment.objects.filter(active=True)
    serializer_class = EnrollmentSerializer
