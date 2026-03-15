from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, TeacherProfile, StudentProfile,
    Subject, StudentSubjectAllocation, Attendance, StudentResult, StudyMaterial
)

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Role',
            {
                'fields': (
                    'is_admin',
                    'is_teacher',
                    'is_student',
                ),
            },
        ),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(Subject)
admin.site.register(StudentSubjectAllocation)
admin.site.register(Attendance)
admin.site.register(StudentResult)
admin.site.register(StudyMaterial)
