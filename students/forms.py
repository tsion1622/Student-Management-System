from django import forms
from .models import Student, Enrollment  # ✅ Added Enrollment here
from .models import Course
from .models import Enrollment
from .models import Attendance, Student


class StudentForm(forms.ModelForm):
    # Add related user fields manually
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = ['student_number', 'field_of_study', 'gpa']  # Removed first_name, last_name, email here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        student = super().save(commit=False)
        user = student.user

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            student.save()
        else:
            # Optionally handle delayed save
            pass
        return student

    def clean_gpa(self):
        gpa = self.cleaned_data.get('gpa')
        if gpa is not None and (gpa < 0.0 or gpa > 4.0):
            raise forms.ValidationError("GPA must be between 0.0 and 4.0")
        return gpa

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course', 'grade']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code']  # Add other fields if needed

class GradeEntryForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'grade']        

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']
