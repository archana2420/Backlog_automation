from django.db import models
from django.http import request


exam_choices = (

    ("backlog", "Backlog Exam"),
    ("improvement", "Improvement Exam"),
    ("year_back", "Year back Exam"),
)


code_cse = (("16CS302", "16CS302"), ("16CS303", "16CS303"),("16CS204","16CS204"),("17CS300","17CS300"))


# class Student_Details(models.Model):
#     NAME = models.CharField(max_length=50)
#     USN = models.CharField(max_length=11)
#     MOBILE = models.CharField(max_length=12)
#     EMAIL = models.EmailField(max_length=32, default="")

#     class Meta:
#         db_table = 'Student_Details'

#     def __str__(self):
#         return "%s %s %s %s" % (self.NAME, self.EMAIL, self.USN, self.MOBILE)


# class Subject(models.Model):
#     dept = models.CharField(max_length=5)
#     sem = models.CharField(max_length=200)
#     exam_type = models.CharField(max_length=200)
#     subject = models.CharField(max_length=200)
#     subject_code = models.CharField(max_length=200)
# USN = models.ManyToManyField(Student_Details)

# class Meta:
#     db_table = 'Subject'

# def __str__(self):
#     return "%s %s %s %s %s %s" % (self.dept, self.sem, self.exam_type, self.subject, self.subject_code, self.USN)


class final(models.Model):
    student_name = models.CharField(max_length=50)
    student_usn = models.CharField(max_length=11)
    student_mobile = models.CharField(max_length=12)
    student_email = models.EmailField(max_length=100, default="")

    student_dept = models.CharField(max_length=5)
    student_sem = models.CharField(max_length=200)
    student_exam_type = models.CharField(max_length=200)
    student_subject = models.CharField(max_length=200)
    student_subject_code = models.CharField(max_length=200)

    class Meta:
        db_table = 'final'


class subject_code_table(models.Model):
    sub_name=models.CharField(max_length=50)
    sub_code=models.CharField(max_length=10)

    def __str__(self):
        return self.sub_name


class Departments(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Semesters(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subjects(models.Model):
    name = models.CharField(max_length=100)
    semester = models.ForeignKey(Semesters, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    department = models.ForeignKey(
        Departments, on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(
        Semesters, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.SET_NULL, null=True)
    exam_type = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=200)

    # exam_type = forms.ChoiceField(
    #         choices=exam_choices, label='Examination_type:')
    #     subject_code = forms.ChoiceField(
    #         choices=code_cse, label='Subject Code:')
    exam_type = models.CharField(max_length=100,
                                 choices=exam_choices)
    subject_code = models.CharField(max_length=100,
                                    choices=code_cse)

    def __str__(self):
        return self.name


class orders(models.Model):
    ref_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(max_length=100,default=0)
    name = models.CharField(max_length=90)
    email = models.EmailField(max_length=111)
    phone = models.CharField(max_length=12, default="")

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    ref_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
