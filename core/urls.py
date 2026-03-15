from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    
    # Teacher URLs
    path('teacher/subjects/', views.teacher_subjects, name='teacher_subjects'),
    path('teacher/attendance/<int:subject_id>/', views.mark_attendance, name='mark_attendance'),
    path('teacher/results/<int:subject_id>/', views.declare_results, name='declare_results'),
    path('teacher/materials/<int:subject_id>/', views.upload_material, name='upload_material'),
    
    # Student URLs
    path('student/attendance/', views.student_attendance, name='student_attendance'),
    path('student/results/', views.student_results, name='student_results'),
    path('student/materials/', views.student_materials, name='student_materials'),
    
    path('notifications/', views.notifications_view, name='notifications'),
]
