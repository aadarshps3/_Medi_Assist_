import csv
from datetime import datetime

from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from io import BytesIO
from Mediassist_app.forms import LoginRegister, DonorRegister
from Mediassist_app.models import donor, users, Medicine_approval, Medicine_request, Cash_approval, Cash_request, \
    Feedback
import xlsxwriter

class CompanyRegistrationView(View):

    def get(self, request):
        user = LoginRegister()
        company_form = DonorRegister()


        return render(request, 'admin/register_cmp.html', {"user": user, "company_form": company_form})

    def post(self, request):
        user = LoginRegister(request.POST)

        company_form = DonorRegister(request.POST)

        if user.is_valid() and company_form.is_valid():

            a = user.save(commit=False)
            print(a)
            a.is_donor = True
            a.save()
            user1 = company_form.save(commit=False)
            print(user1)
            user1.user = a
            user1.save()
            return redirect('admin_base')
        return render(request,'admin/register_cmp.html', {"user": user, "company_form": company_form})



def cmp_list(request):
    cmp=donor.objects.all()
    return render(request,'admin/cmp_list.html',{'cmp':cmp})


def user_list(request):
    user=users.objects.all()
    return render(request,'admin/user_list.html',{'user':user})


def requests(request):
    data = Medicine_approval.objects.all()
    return render(request, 'admin/approval.html', {'data': data})

def export_medicines(request):
    data = Medicine_approval.objects.filter(approval__status_1=2)

    # Create an in-memory Excel file
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Write headers
    headers = ['Company', 'User', 'Medicine', 'Quantity', 'Note']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Write data rows
    for row, task in enumerate(data, start=1):
        worksheet.write(row, 0, task.user.name)
        worksheet.write(row, 1, task.approval.user.username)
        # worksheet.write(row, 2, task.approval.end_date)
        worksheet.write(row, 3, task.approval.medicine_name)
        worksheet.write(row, 4, task.approval.quantity)
        worksheet.write(row, 5, task.note)

    workbook.close()

    # Set response headers for Excel file download
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Medicine_report.xlsx'
    return response



def admin_approval(request):
    data=Medicine_approval.objects.filter(approval__status_1 = 3 )
    return render(request,'admin/approval.html',{'data':data})




def approve_donation(request, id):
    n = Medicine_request.objects.get(id=id)
    print(n)
    n.status_1 = 2

    print(n.status_1)
    n.save()

    messages.info(request, 'Donation Confirmed')
    return redirect('requests')

def reject_donation(request, id):
    n = Medicine_request.objects.get(id=id)
    n.status_1 = 3
    n.save()
    messages.info(request, 'Rejected')
    return redirect('requests')



def cash_requests(request):
    data = Cash_approval.objects.all()
    return render(request, 'admin/cash_approval.html', {'data': data})

def admin_cash_approval(request):
    data=Cash_approval.objects.filter(approval__status_12 = 3)
    return render(request,'admin/cash_approval.html',{'data':data})




def approve_cash_donation(request,id):
    n = Cash_request.objects.get(id=id)
    print(n)
    n.status_12 = 2

    n.save()
    messages.info(request, 'Donation Confirmed')
    return redirect('cash_requests')

def reject_cash_donation(request, id):
    n = Cash_request.objects.get(id=id)
    n.status_12 = 3
    n.save()
    messages.info(request, 'Rejected')
    return redirect('cash_requests')


#approve users

def users_approval(request,id):
    data = users.objects.get(id=id)
    data.verified = 1
    data.save()
    return redirect('user_list')

def users_reject(request,id):
    data = users.objects.get(id=id)
    data.verified = 2
    data.save()
    return redirect('user_list')


def generate_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        report = Medicine_approval.objects.filter(date__gte=start_date, date__lte=end_date,approval__status_1=2).values(
            'date', 'user__name', 'approval__medicine_name', 'approval__quantity', 'note'
        ).order_by('date')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="donation_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Donor Name', 'Medicine Name', 'Quantity', 'Note'])

        for donation in report:
            writer.writerow([
                donation['date'].strftime('%Y-%m-%d'),
                donation['user__name'],
                donation['approval__medicine_name'],
                donation['approval__quantity'],
                donation['note']
            ])

        return response

    return render(request, 'admin/generate_report.html')

def generate_cash_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        cash_report = Cash_approval.objects.filter(date__gte=start_date, date__lte=end_date, approval__status_12=2).values(
            'date', 'user__name', 'approval__description', 'approval__amount', 'paystat'
        ).order_by('date')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cash_donation_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Donor Name', 'Description', 'Amount', 'Payment Status'])

        for cash_donation in cash_report:
            payment_status = "Payment Successful" if cash_donation['paystat'] == 1 else "Payment Pending"
            writer.writerow([
                cash_donation['date'].strftime('%Y-%m-%d'),
                cash_donation['user__name'],
                cash_donation['approval__description'],
                cash_donation['approval__amount'],
                payment_status
            ])

        return response

    return render(request, 'admin/generate_cash_report.html')

def feedbacks(request):
    n = Feedback.objects.all()
    return render(request,'admin/feedbacks.html',{'feedbacks':n})


def reply_feedback(request,id):
    feedback = Feedback.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        feedback.reply = r
        feedback.save()
        messages.info(request, 'Reply send for complaint')
        return redirect('feedbacks')
    return render(request, 'admin/admin_feedback.html', {'feedback': feedback})