from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Teacher: {self.user.username}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    enrollment_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    grade = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Student: {self.user.username}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')

    def __str__(self):
        return f"{self.name} ({self.code})"

class StudentSubjectAllocation(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='allocations')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='allocations')

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name}"
        
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')

    class Meta:
        unique_together = ['subject', 'student', 'date']

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name} - {self.date}"

class StudentResult(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    declared_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name} - {self.marks_obtained}/{self.max_marks}"

class StudyMaterial(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='study_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username}: {self.message[:20]}"
