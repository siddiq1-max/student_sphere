from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import TeacherProfile, StudentProfile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create corresponding profile
            if user.is_teacher:
                TeacherProfile.objects.create(user=user)
            elif user.is_student:
                StudentProfile.objects.create(user=user)
            
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard_view(request):
    if request.user.is_admin or request.user.is_superuser:
        return render(request, 'dashboard/admin_dashboard.html')
    elif request.user.is_teacher:
        return render(request, 'dashboard/teacher_dashboard.html')
    elif request.user.is_student:
        return render(request, 'dashboard/student_dashboard.html')
    else:
        # Fallback
        return render(request, 'base.html')

from .models import Subject, StudentSubjectAllocation, Attendance, StudentResult, StudyMaterial, Notification
from django.contrib import messages
import datetime

# --- TEACHER VIEWS ---
@login_required
def teacher_subjects(request):
    if not request.user.is_teacher:
        return redirect('dashboard')
    subjects = request.user.teacher_profile.subjects.all()
    return render(request, 'teacher/subjects.html', {'subjects': subjects})

@login_required
def mark_attendance(request, subject_id):
    if not request.user.is_teacher:
        return redirect('dashboard')
    subject = Subject.objects.get(id=subject_id)
    allocations = subject.allocations.all()
    
    if request.method == 'POST':
        date_str = request.POST.get('date', datetime.date.today().strftime('%Y-%m-%d'))
        for alloc in allocations:
            status = request.POST.get(f'status_{alloc.student.id}', 'present')
            Attendance.objects.update_or_create(
                subject=subject,
                student=alloc.student,
                date=date_str,
                defaults={'status': status}
            )
        messages.success(request, 'Attendance marked successfully.')
        return redirect('teacher_subjects')
        
    return render(request, 'teacher/mark_attendance.html', {'subject': subject, 'allocations': allocations})

@login_required
def declare_results(request, subject_id):
    if not request.user.is_teacher:
        return redirect('dashboard')
    subject = Subject.objects.get(id=subject_id)
    allocations = subject.allocations.all()
    
    if request.method == 'POST':
        for alloc in allocations:
            marks = request.POST.get(f'marks_{alloc.student.id}')
            if marks:
                StudentResult.objects.update_or_create(
                    subject=subject,
                    student=alloc.student,
                    defaults={'marks_obtained': marks, 'max_marks': 100}
                )
                Notification.objects.create(
                    user=alloc.student.user,
                    message=f"Marks declared for {subject.name}: {marks}/100"
                )
        messages.success(request, 'Results declared successfully.')
        return redirect('teacher_subjects')
        
    return render(request, 'teacher/declare_results.html', {'subject': subject, 'allocations': allocations})

@login_required
def upload_material(request, subject_id):
    if not request.user.is_teacher:
        return redirect('dashboard')
    subject = Subject.objects.get(id=subject_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        if title and file:
            StudyMaterial.objects.create(
                subject=subject,
                title=title,
                file=file,
                uploaded_by=request.user.teacher_profile
            )
            # Notify students
            for alloc in subject.allocations.all():
                Notification.objects.create(
                    user=alloc.student.user,
                    message=f"New study material uploaded for {subject.name}: {title}"
                )
            messages.success(request, 'Material uploaded successfully.')
            return redirect('teacher_subjects')
            
    materials = StudyMaterial.objects.filter(subject=subject)        
    return render(request, 'teacher/upload_material.html', {'subject': subject, 'materials': materials})

# --- STUDENT VIEWS ---
@login_required
def student_attendance(request):
    if not request.user.is_student:
        return redirect('dashboard')
    attendance_records = Attendance.objects.filter(student=request.user.student_profile).order_by('-date')
    return render(request, 'student/attendance.html', {'attendance_records': attendance_records})

@login_required
def student_results(request):
    if not request.user.is_student:
        return redirect('dashboard')
    results = StudentResult.objects.filter(student=request.user.student_profile)
    return render(request, 'student/results.html', {'results': results})

@login_required
def student_materials(request):
    if not request.user.is_student:
        return redirect('dashboard')
    allocations = request.user.student_profile.allocations.all()
    subjects = [a.subject for a in allocations]
    materials = StudyMaterial.objects.filter(subject__in=subjects).order_by('-uploaded_at')
    return render(request, 'student/materials.html', {'materials': materials})

@login_required
def notifications_view(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    # Mark as read
    unread = request.user.notifications.filter(is_read=False)
    unread.update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifications})

