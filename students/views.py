from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Student, Course, Enrollment
from .forms import StudentForm, EnrollmentForm
from .forms import CourseForm

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