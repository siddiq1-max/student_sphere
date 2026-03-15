from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, widget=forms.RadioSelect)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        if role == 'teacher':
            user.is_teacher = True
        elif role == 'student':
            user.is_student = True
            
        if commit:
            user.save()
        return user
