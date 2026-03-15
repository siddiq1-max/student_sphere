import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_sphere.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
    user.is_admin = True
    user.save()
    print("Superuser 'admin' created with password 'admin123'")
else:
    print("Superuser 'admin' already exists")
