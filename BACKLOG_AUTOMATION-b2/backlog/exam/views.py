# from django.shortcuts import render
from django.shortcuts import render
from .Paytm import Checksum
# Create your views here.
from django.forms.models import model_to_dict
from django import forms
from django.forms import formsets
from django.forms.forms import Form
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import generic
import requests
# import json
from .forms import *
from .forms import SUBJECTFORMSET
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import razorpay

MERCHANT_KEY = 'Zr%PlovaG6P4wbLt'


def index(request):
    cont = {}
    i_form = index_form()
    cont['form'] = i_form

    if request.method == "POST":
        i_form = index_form(request.POST)
        if i_form.is_valid():

            name = i_form.cleaned_data['name']
            usn = i_form.cleaned_data['usn']
            email = i_form.cleaned_data['email']
            phno = i_form.cleaned_data['phno']

            student_data = {

                "Student_Name": name,
                "Student_USN": usn,
                "Student_email": email,
                "Student_mobile": phno
            }

            request.session['data1'] = student_data

        total_subjects = 1
        request.session['total_subjects'] = total_subjects
        return redirect('display')
    else:
        return render(request, "index2.html", cont)


def load_semesters(request):
    department = request.GET.get('department')

    semesters = Semesters.objects.filter(
        department=department).order_by('name')

    context = {'semesters': semesters}
    return render(request, 'load_semesters.html', context)


def load_subjects(request):
    semester_id = request.GET.get('semester')
    subjects = Subjects.objects.filter(
        semester_id=semester_id).order_by('name')
    context = {'subjects': subjects}
    return render(request, 'load_subjects.html', context)


def otp(request):
    # student_information(request)
    return render(request, 'otp.html')


def display_information(request):
    template_name = 'display_information.html'
    # if request.method == 'GET':
    #     formset = SUBJECTFORMSET(request.GET or None)
    if request.method == 'POST':
        SUBJECTFORMSET = formset_factory(student_form, extra=1, max_num=6)
        formset = SUBJECTFORMSET(request.POST)
        count=0
        if formset.is_valid():
            subject_data = {}
            y = {}
            for form in formset:
                try:
                    count+=1
                    # extract name from each form and save
                    old_department = form.cleaned_data['department']
                    department = model_to_dict(old_department)
                    department = department["name"]

                    exam = form.cleaned_data['exam_type']

                    old_sem = form.cleaned_data['semester']
                    sem = model_to_dict(old_sem)
                    sem = sem["name"]

                    old_subject = form.cleaned_data['subject']
                    subject = model_to_dict(old_subject)
                    subject = subject["name"]



                    subject_code=subject_code_table.objects.get(sub_name=subject)
                    s_code=subject_code.sub_code
                    y = {

                        "Department": department,
                        "Exam_type": exam,
                        "Semester": sem,
                        "Subject": subject,
                        "Subject_Code": s_code
                    }
                    # student_form.objects.get(id=id).delete()

                    subject_data.update({f"{s_code}": y})
                    # print(subject_data)
                except KeyError:
                    break
            request.session['data2'] = subject_data
            print(count)
            request.session['count'] = count

            return redirect('student_info')

        # return render(request, template_name, {'formset': formset })
    else:
        total_subjects = request.session.get('total_subjects')
        SUBJECTFORMSET = formset_factory(student_form, extra=total_subjects, max_num=6)
        formset = SUBJECTFORMSET()
    return render(request, template_name, {'formset': formset})


def load_semesters(request):
    department = request.GET.get('department')

    semesters = Semesters.objects.filter(
        department=department).order_by('name')

    context = {'semesters': semesters}
    return render(request, 'load_semesters.html', context)


def load_subjects(request):
    semester_id = request.GET.get('semester')
    subjects = Subjects.objects.filter(
        semester_id=semester_id).order_by('name')
    context = {'subjects': subjects}
    return render(request, 'load_subjects.html', context)

def student_information(request):

    student_dict = request.session.get('data1')
    # print(student_dict)
    sub_info_dict = request.session.get('data2')
    total_subjects = len(sub_info_dict)
    total_amount = (1000 * total_subjects)
    email = student_dict['Student_email']
    # print(email)
    request.session['total_subjects'] = total_subjects
    r_amt=total_amount*100
    client = razorpay.Client(auth=("rzp_test_uZs7UIhICwdoWx", "oamjRDd71nP3U4WsqmvltJdG"))

    DATA = {
            "amount": r_amt,
            "currency": "INR",
            "receipt": "receipt#1",

    }
    payment=client.order.create(data=DATA)
    print(payment)
    if request.method == "POST":
        return redirect('success')


    return render(request, 'student_info.html',
                      {'stud': student_dict, 'sub_info_dict': sub_info_dict, 'total_amount':total_amount,'payment':payment,'r_amt':r_amt})

    # return render(request, 'student_info.html', {'stud': student_dict, 'sub_info_dict': sub_info_dict, 'total_amount':total_amount,'r_amt':r_amt})


@csrf_exempt
def success(request):
    student_dict = request.session.get('data1')
    print(student_dict)
    student_sub_dict = request.session.get('data2')
    email = student_dict['Student_email']

    context={'student_data':student_dict,'subject_data':student_sub_dict,'email':email}
    count=request.session.get('count')
    for key,value in student_sub_dict.items():

        application_entry=final(student_name=student_dict['Student_Name'],student_usn=student_dict['Student_USN']
                            ,student_mobile=student_dict['Student_mobile'],student_email=student_dict['Student_email']
                                ,student_dept=value['Department'],student_sem=value['Semester'],
                                student_exam_type=value['Exam_type'],student_subject=value['Subject'],
                                student_subject_code=key)

        application_entry.save()

    return render(request,'paymentstatus_success.html',context)



@login_required
def dashboard1(request):
    return render(request, 'staff_dashboard.html')
    student_dict = {"Student_Name": student_data["name"],
                    "Student_USN": student_data["usn"],
                    "Student_email": student_data["email"],
                    "Student_mobile": student_data["phno"]}

    # return redirect('Checkout')

    # final(student_name=student_data["name"], student_usn=student_data["usn"], student_email=student_data["email"], student_mobile=student_data["phno"], student_dept=department,
    #       student_sem=sem, student_exam_type=exam, student_subject=subject, student_subject_code=subject_code).save()
    return render(request, 'Checkout.html', {'stud': student_dict, 'sub_info_dict': sub_info_dict})


@csrf_exempt
def handle_request(request):
    form = request.POST
    response_dict = {}
    student_dict = request.session.get('data1')
    print(student_dict)
    
    
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Payment Successful')
            return render(request, 'paymentstatus_success.html', {'response': response_dict})
        else:
            print('Payment was not successful because' +
                  response_dict['RESPMSG'])
            return render(request, 'Transaction_failed.html', {'response': response_dict})




# def checkout(request):
#     if request.method == "POST":
#         name = request.session.get(['data1']['name'])
#         email = request.session.get(['data1']['email'])
#         phone = request.session.get(['data1']['phno'])

#         print(name)
#         amount = request.POST.get('amount')
#         print(amount)
#         order = orders(name=name, email=email,
#                        phone=phone, amount=amount).save()
#         update = OrderUpdate(ref_id=order.ref_id,
#                              update_desc="The payment has been made")
#         update.save()
#         thank = True
#         id = order.ref_id
#         param_dict = {

#             'MID': 'WorldP64425807474247',
#             'ORDER_ID': str(order.ref_id),
#             'TXN_AMOUNT': str(amount),
#             'CUST_ID': email,
#             'INDUSTRY_TYPE_ID': 'Retail',
#             'WEBSITE': 'WEBSTAGING',
#             'CHANNEL_ID': 'WEB',
#             'CALLBACK_URL': 'http://127.0.0.1:8000/exam/handle_request/',

#         }
#         param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
#             param_dict, MERCHANT_KEY)

#         return render(request, 'paytm.html', {'param_dict': param_dict})
#     return render(request, 'student_info.html')




































# def send_email(request):
#     message = MIMEMultipart()

#     message["from"] = "Anupam Ahi"
#     message["to"] = "anupam.gollapalli@gmail.com"
#     message["subject"] = "TEST MAIL"
#     message.attach(MIMEText("Body"))
#     # Body is the pdf file of confirmation details
#     with smtplib.SMTP(host="smtp.gmail.com", port=587) as sm:
#         sm.ehlo()
#         sm.starttls()
#         sm.login("", "")
#         # https://www.google.com/settings/security/lesssecureapps
#         sm.send_message(message)
#         print("Sent...")
