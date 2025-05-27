from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home or student list page
    path('add/', views.add, name='add'),  # Add a new student
    path('<int:id>/', views.view_student, name='view_student'),  # View a student by ID
    path('edit/<int:id>/', views.edit, name='edit'),  # Edit student details
    path('delete/<int:id>/', views.delete, name='delete'),  # Delete a student
    path('students/admin/', views.admin_student_list, name='admin_student_list'),
    path('add-course/', views.add_course, name='add_course'),
    # Enrollment-related URLs
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),  # Detailed view of student
    path('student/<int:student_id>/add-enrollment/', views.add_enrollment, name='add_enrollment'),  # Add enrollment
    path('enrollment/<int:enrollment_id>/delete/', views.delete_enrollment, name='delete_enrollment'),  # Delete enrollment
    path('courses/', views.course_list, name='course_list'),
    path('student/<int:student_id>/report_card/', views.report_card, name='report_card'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/list/', views.attendance_list, name='attendance_list'),
    path('attendance/student/<int:student_id>/', views.student_attendance_detail, name='student_attendance_detail'),

]
