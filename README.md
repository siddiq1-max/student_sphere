# Student Sphere

Student Sphere is a full-stack role-based academic management system built using Django, Bootstrap, and SQLite. It provides distinct interfaces for Admin, Teacher, and Student roles to streamline course management, attendance tracking, results declaration, and study material distribution.

## Features
- **Role-Based Authentication**: Custom User models isolating properties for Admins, Teachers, and Students.
- **Subject Allocation**: Efficiently allocate subjects to teachers and enroll students.
- **Attendance Management**: Bulk attendance marking system with Present/Absent/Late statuses.
- **Marks Declarement & Results**: Declarative interface for marks distribution.
- **Study Materials Repository**: Secure upload and download workflows for assignments and notes.
- **Real-Time Notifications**: Integrated notification engine alerting students of new marks and materials.
- **Modern UI**: Polished Glassmorphism design system integrated with Bootstrap 5.

 ## Host link here 
 http://siddiq.pythonanywhere.com

## Installation & Local Setup
1. Clone the repository: 
   ```bash
   git clone https://github.com/siddiq1-max/student_sphere.git
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install django pillow
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Tech Stack
- Backend: **Python, Django, SQLite**
- Frontend: **HTML, CSS, Bootstrap 5, JavaScript**

## License
MIT License


