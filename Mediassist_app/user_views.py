from django.contrib import messages
from django.shortcuts import redirect, render

from Mediassist_app.forms import MedicineForm, CashRequestForm, FeedbackForm
from Mediassist_app.models import Medicine_request, donor, users, Cash_request, Feedback, Medicine_approval, \
    Cash_approval


def med_add(request):
    form = MedicineForm()
    u = request.user
    print(u)
    # n = users.objects.get(user=u)
    # print(n)
    if request.method == 'POST':
        form = MedicineForm(request.POST,request.FILES)
        if form.is_valid():
            new_med = form.save(commit=False)
            new_med.user = u
            new_med.save()
            messages.info(request, 'Added Successfully')
            return redirect('med_view')
    else:
        form = MedicineForm()
    return render(request, 'users/med_add.html', {'form':form})


def med_view(request):
    u = request.user
    n = Medicine_request.objects.filter(user=u)

    return render(request, 'users/med_request_view.html',{'medicine':n})


def med_view1(request):
    u = request.user
    # t = donor.objects.get(approval = u)
    # print(t)

    n = Medicine_approval.objects.filter(approval__user=u, approval__status_1=2)



    return render(request, 'users/med_request_status.html',{'medicine':n})



def cash_add(request):
    form = CashRequestForm()
    u = request.user
    print(u)
    # n = users.objects.get(user=u)
    # print(n)
    if request.method == 'POST':
        form = CashRequestForm(request.POST)
        if form.is_valid():
            new_med = form.save(commit=False)
            new_med.user = u
            new_med.save()
            messages.info(request, 'Added Successfully')
            return redirect('cash_view')
    else:
        form = CashRequestForm()
    return render(request,'users/cash_add.html', {'form':form})



def cash_view(request):
    u = request.user
    n = Cash_request.objects.filter(user=u)

    return render(request, 'users/cash_request_view.html',{'cash':n})




def feedback(request):
    form=FeedbackForm
    u= request.user

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request,"thank you for your feedback...!!!")
            return redirect('feedback_view')
    else:
        form = FeedbackForm()
    return render(request,'users/feedback_add.html',{'form':form})



def feedback_view(request):

    u = Feedback.objects.filter(user=request.user)
    return render(request,"users/feedback_view.html",{'feedback':u})

def pay_status(request):
    u=request.user
    data=Cash_approval.objects.filter(approval__user=u)
    return render(request,'users/pay_status.html',{'data':data})