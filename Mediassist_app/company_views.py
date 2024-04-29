from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from Mediassist_app.forms import PayForm
from Mediassist_app.models import Medicine_request, donor, Medicine_approval, Cash_request, Cash_approval


def med_view_cmp(request):
    n = Medicine_request.objects.all()

    return render(request, 'company/med_request_view.html',{'medicine':n})



#donate

def donate(request,id):
    note = request.POST.get('note')
    approval = Medicine_request.objects.get(id=id)
    u = donor.objects.get(user=request.user)
    appointment = Medicine_approval.objects.filter(user=u , approval=approval)
    if appointment.exists():
        messages.info(request, 'You Have Already Requested Donation..we will reach you soon')
        return redirect("med_view_cmp")
    else:
        if request.method == 'POST':
            obj = Medicine_approval()
            obj.user = u
            obj.approval = approval

            obj.note = note

            obj.save()

            approval.status_1 = 1
            approval.save()




            messages.info(request, 'Thanks for your support..we will reach you soon')
            return redirect('med_view_cmp')
    return render(request, 'company/donate.html', {'approval': approval})




def cash_view_cmp(request):

    n = Cash_request.objects.all()

    return render(request, 'company/cash_request_view.html',{'cash':n})




def donate_cash(request,id):
    approval = Cash_request.objects.get(id=id)
    u = donor.objects.get(user=request.user)
    appointment = Cash_approval.objects.filter(user=u , approval=approval)
    if appointment.exists():
        messages.info(request, 'You Have Already Requested Donation..we will reach you soon')
        return redirect("cash_view_cmp")
    else:
        if request.method == 'POST':
            obj = Cash_approval()
            obj.user = u
            obj.approval = approval

            obj.save()

            approval.status_12 = 1
            approval.save()


            messages.info(request, 'Thanks for your support..we will reach you soon')
            return redirect('cash_view_cmp')
    return render(request, 'company/donate_cash.html', {'approval': approval})


def MyDonations(request):
    u = request.user
    cmp = donor.objects.get(user = u)
    data = Medicine_approval.objects.filter(user = cmp)

    return render(request,'company/mydonations.html',{'data':data})


def CashDonation(request):
    u = request.user
    cmp = donor.objects.get(user = u)
    data = Cash_approval.objects.filter(user = cmp)
    return render(request,'company/cashdonation.html',{'data':data})


def payment(request,id):
    data = get_object_or_404(Cash_approval, id=id)
    form = PayForm()
    if request.method == 'POST':
        form = PayForm(request.POST)
        if form.is_valid():
            med = form.save(commit=False)
            med.user = data
            med.save()
            data.paystat = 1
            print(data.approval.status_12,"********")
            data.save()
            messages.success(request,'Paid Successfully')
            return redirect('CashDonation')

    return render(request,'company/payonline.html', {'form': form})
