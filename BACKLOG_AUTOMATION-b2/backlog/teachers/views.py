from django.shortcuts import render,redirect
from exam.models import final
from .forms import search_form,staff_form,staff_loginForm
from .models import staff_details
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
# Create your views here.

def staff_login(request):
    if request.user.is_authenticated:
        return redirect('staff_dashboard')

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        print(username,password)
        user=User.objects.get(username=username)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('staff_dashboard')
        # print(user)
        # records=staff_details.objects.all()
        # print(records)
        # user=authenticate(email=email,password=password)
        # print(user)
        # if user is not None:
        #     login(request,user)
        #     return redirect('staff_dashboard')
            # user=authenticate(request,email=email,password=password)
            # if user is not None:
            #     login(request,user)
            #     return redirect('staff_dashboard')
    return render(request,'staff_login.html')




def staff_registeration(request):
    form=CustomUserCreationForm()
    context={'form':form}
    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=True)
            user.save()
            login(request,user)
            return redirect('staff_dashboard')


    return render(request,'staff_registration.html',context)




def staff_dashboard(request):
    form=search_form()
    all_enteries = final.objects.all()
    context = {'all_enteries': all_enteries,'form':form}
    if request.method=="POST":
        form = search_form(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            search_type = form.data['search_choice']
            print(search_type)
            if search_type=="subject_code":
                search=final.objects.filter(student_subject_code=content)
                print(search)
            elif search_type=="subject":
                search = final.objects.filter(student_subject=content)
                print(search)
            elif search_type=="exam_type":
                search = final.objects.filter(student_exam_type=content)
                print(search)
            elif search_type=="department":
                search = final.objects.filter(student_dept=content)
                print(search)
            elif search_type=="sem":
                search = final.objects.filter(student_sem=content)
                print(search)
            context = {'all_enteries': search, 'form': form}
            request.session['search_content']=content
            request.session['search_type']=search_type
            return render(request, 'teachers_dashboard.html', context)
    return render(request, 'teachers_dashboard.html',context)

def csv_download(request):
    search_content=request.session.get('search_content')
    search_type=request.session.get('search_type')
    if search_type == "subject_code":
        search = final.objects.filter(student_subject_code=search_content)

    elif search_type == "subject":
        search = final.objects.filter(student_subject=search_content)

    elif search_type == "exam_type":
        search = final.objects.filter(student_exam_type=search_content)

    elif search_type == "department":
        search = final.objects.filter(student_dept=search_content)

    elif search_type == "sem":
        search = final.objects.filter(student_sem=search_content)


    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=students_list.csv'
    writer = csv.writer(response)
    writer.writerow(
        ['USN', 'Name', 'Mobile No.', 'Email', 'Subject', 'Subject Code', 'Semester', 'Department', 'Exam Type'])
    students = search.values_list('student_usn', 'student_name', 'student_mobile', 'student_email', 'student_subject',
                              'student_subject_code', 'student_sem', 'student_dept', 'student_exam_type')
    for student in students:
        writer.writerow(student)
    return response

def logoutPage(request):
    logout(request)
    return redirect('staff_login')