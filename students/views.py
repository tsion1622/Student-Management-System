from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Course, Enrollment
from .forms import EnrollmentForm
from .models import Student
from .forms import StudentForm

def index(request):
    return render(request, 'students/index.html', {
        'students': Student.objects.all()
    })

def view_student(request, id):
    student = Student.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))

def add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            new_student_number = form.cleaned_data['student_number']
            new_first_name = form.cleaned_data['first_name']
            new_last_name = form.cleaned_data['last_name']
            new_email = form.cleaned_data['email']
            new_field_of_study = form.cleaned_data['field_of_study']
            new_gpa = form.cleaned_data['gpa']

            new_student = Student(
                student_number=new_student_number,
                first_name=new_first_name,
                last_name=new_last_name,
                email=new_email,
                field_of_study=new_field_of_study,
                gpa=new_gpa
            )
            new_student.save()
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
    if request.method == 'POST':
        student = Student.objects.get(pk=id)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return render(request, 'students/edit.html', {
                'form': form,
                'success': True
            })
    else:
        student = Student.objects.get(pk=id)
        form = StudentForm(instance=student)
    return render(request, 'students/edit.html', {
        'form': form
    })

def delete(request, id):
    if request.method == 'POST':
        student = Student.objects.get(pk=id)
        student.delete()
    return HttpResponseRedirect(reverse('index'))

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    enrollments = student.enrollments.select_related('course')
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
    return render(request, 'students/add_enrollment.html', {'form': form, 'student': student})