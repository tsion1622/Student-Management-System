from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('<int:id>/', views.view_student, name='view_student'),
    path('add/', views.add, name='add'),
    path('add/', views.add, name='add'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('student/<int:student_id>/add-enrollment/', views.add_enrollment, name='add_enrollment'),
    path('enrollment/<int:enrollment_id>/delete/', views.delete_enrollment, name='delete_enrollment'),

]