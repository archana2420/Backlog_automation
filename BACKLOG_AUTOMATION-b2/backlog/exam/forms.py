from django import forms
from django.forms import fields, formset_factory
from .models import *

# dept_choices = (
#     ("dummy", "Select Department"),
#     ("1st year", "1st year"),
#     ("CSE", "CSE"),
#     ("ECE", "ECE"),
#     ("AS", "AS"),
#     ("MECH", "MECH"),
#     ("BCA", "BCA"),
# )
# exam_choices = (
#     ("dummy", "Select Exam"),
#     ("backlog", "Backlog Exam"),
#     ("improvement", "Improvement Exam"),
#     ("year_back", "Year back Exam"),
# )
# sem_choices = (
#     ("dummy", "Select Sem"),
#     ("1", "1"),
#     ("2", "2"),
#     ("3", "3"),
#     ("4", "4"),
#     ("5", "5"),
#     ("6", "6"),
#     ("7", "7"),
#     ("8", "8"),
# )

# sub_cse = (
#     ("dummy", "Select Subject"),
#     ("DBMS", "Database Management System"),
#     ("OS", "Operating System"),
# )
# code_cse = (("16CS302", "16CS302"), ("16CS303", "16CS303"))


# class s_form(forms.Form):
#     # dept = forms.CharField()
#     dept = forms.ChoiceField(choices=dept_choices, label='Department:')
#     sem = forms.ChoiceField(choices=sem_choices, label='Semester:')
#     exam_type = forms.ChoiceField(
#         choices=exam_choices, label='Examination_type:')
#     subject = forms.ChoiceField(choices=sub_cse, label='Subject:')
#     subject_code = forms.ChoiceField(choices=code_cse, label='Subject Code:')


# SUBJECTFORMSET = formset_factory(s_form, extra=1)

class index_form(forms.Form):
    name = forms.CharField(max_length=30, label="Name:")
    usn = forms.CharField(max_length=11, label="USN:")
    phno = forms.IntegerField(label="Mobile no:")
    email = forms.EmailField(max_length=32, label="Gmail")


class student_form(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('department', 'semester', 'subject',
                  'exam_type', )
        # exam_type = forms.ChoiceField(
        #     choices=exam_choices, label='Examination_type:')
        # subject_code = forms.ChoiceField(
        #     choices=code_cse, label='Subject Code:')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['semester'].queryset = Semesters.objects.none()

            if 'department' in self.data:
                try:
                    dept_id = int(self.data.get('department'))
                    self.fields['semester'].queryset = Semesters.objects.filter(
                        dept_id=dept_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['semester'].queryset = self.instance.department.semester_set.order_by(
                    'name')

            self.fields['subject'].queryset = Semesters.objects.none()

            if 'semester' in self.data:
                try:
                    sem_id = int(self.data.get('semester'))
                    self.fields['subject'].queryset = Subjects.objects.filter(
                        sem_id=sem_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['subject'].queryset = self.instance.department.semester.subject_set.order_by(
                    'name')


SUBJECTFORMSET = formset_factory(student_form, extra=1)
