from django import forms
from .models import Student
import pandas as pd

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_number', 'first_name', 'last_name', 'email', 'field_of_study', 'gpa']
        labels = {
            'student_number': 'Student Number',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'field_of_study': 'Field of Study',
            'gpa': 'GPA'
        }
        widgets = {
            'student_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BulkStudentUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File', required=True)

    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('File is not CSV type')
        
        # Optionally: Read the CSV and validate contents
        try:
            df = pd.read_csv(csv_file)
            # Ensure the required columns are in the CSV
            for field in ['student_number', 'first_name', 'last_name', 'email', 'field_of_study', 'gpa']:
                if field not in df.columns:
                    raise forms.ValidationError(f'Missing column: {field}')
        except Exception as e:
            raise forms.ValidationError('Error processing file: ' + str(e))
        
        return csv_file

# New feature added: A separate form for updating student profiles
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']  # Allows updating only these fields
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class