from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Student, Course, Enrollment
from .forms import StudentForm, EnrollmentForm
from .forms import CourseForm
from .forms import GradeEntryForm
from .forms import AttendanceForm
from .models import Attendance, Student
from rest_framework.decorators import api_view
from rest_framework import status
#from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import CustomUser
from django.contrib.auth import authenticate



@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        role = user.role  # directly from CustomUser.role
        return Response({
            'message': 'Login successful',
            'username': user.username,
            'role': role,
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
def index(request):
    return render(request, 'students/index.html', {
        'students': Student.objects.all()
    })

def view_student(request, id):
    return HttpResponseRedirect(reverse('index'))

def add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'students/add.html', {
                'form': StudentForm(),
                'success': True
            })
    else:
        form = StudentForm()
    return render(request, 'students/add.html', {
        'form': form
    })

def edit(request, id):
    student = get_object_or_404(Student, pk=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return render(request, 'students/edit.html', {
                'form': form,
                'success': True
            })
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/edit.html', {
        'form': form
    })

def delete(request, id):
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=id)
        student.delete()
    return HttpResponseRedirect(reverse('index'))

def admin_student_list(request):
    students = Student.objects.all()
    return render(request, 'students/admin_student_list.html', {
        'students': students
    })
def course_list(request):
    return render(request, 'students/course_list.html', {
        'courses': Course.objects.all()
    })

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # You can redirect anywhere
    else:
        form = CourseForm()
    return render(request, 'students/add_course.html', {'form': form})
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    enrollments = Enrollment.objects.filter(student=student).select_related('course')
    form = EnrollmentForm()
    return render(request, 'students/student_detail.html', {
        'student': student,
        'enrollments': enrollments,
        'form': form,
    })

def add_enrollment(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = student
            enrollment.save()
            return redirect('student_detail', student_id=student.id)
    else:
        form = EnrollmentForm()
    return render(request, 'students/add_enrollment.html', {
        'form': form,
        'student': student
    })
def delete_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    enrollment.delete()
    return redirect('enrollment_list')  # Replace with the name of your enrollment list view
    
def add_or_edit_grade(request):
    if request.method == 'POST':
        form = GradeEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    else:
        form = GradeEntryForm()
    return render(request, 'add_grade.html', {'form': form})

def grade_list(request):
    enrollments = Enrollment.objects.select_related('student', 'course')
    return render(request, 'grade_list.html', {'enrollments': enrollments})

def report_card(request, student_id):
    student = Student.objects.get(id=student_id)
    enrollments = student.enrollments.select_related('course')
    return render(request, 'students/report_card.html', {
        'student': student,
        'enrollments': enrollments
    })


def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'students/mark_attendance.html', {'form': form})

# View to list all attendance

def attendance_list(request):
    attendance_records = Attendance.objects.order_by('-date')
    return render(request, 'students/attendance_list.html', {'attendance_records': attendance_records})

# View attendance for a specific student

def student_attendance_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    records = Attendance.objects.filter(student=student).order_by('-date')
    return render(request, 'students/student_attendance_detail.html', {
        'student': student,
        'records': records
    })
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

