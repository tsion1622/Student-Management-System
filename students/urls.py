from django.urls import path
from . import views
from .views import login_view
from .views import CurrentUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:id>/', views.view_student, name='view_student'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('students/admin/', views.admin_student_list, name='admin_student_list'),
    path('add-course/', views.add_course, name='add_course'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('student/<int:student_id>/add-enrollment/', views.add_enrollment, name='add_enrollment'),
    path('enrollment/<int:enrollment_id>/delete/', views.delete_enrollment, name='delete_enrollment'),
    path('courses/', views.course_list, name='course_list'),
    path('student/<int:student_id>/report_card/', views.report_card, name='report_card'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/list/', views.attendance_list, name='attendance_list'),
    path('attendance/student/<int:student_id>/', views.student_attendance_detail, name='student_attendance_detail'),
    #path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('login/', login_view, name='login'),
]
