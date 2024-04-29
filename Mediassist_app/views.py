from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect


# # Create your views here.
# def Test(request):
#     return render(request,"test.html")
from django.views import View

from Mediassist_app.forms import LoginRegister, DonorRegister, UsersRegister


# def landing_page(request):
    # return render(request,"index.html")


def login_page(request):

    return render(request,"login_page.html")

def admin_base(request):
    return render(request,"base.html")

def donator_home(request):
    return render(request,'donator_base.html')

def user_home(request):
    return render(request,'user_base.html')




def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_base')
            elif user.is_users:
                # Get the related users object for the logged-in user
                user_profile = user.users.get()
                if user_profile.verified ==1 :
                    return redirect('user_home')
                else:
                    messages.info(request, 'Waiting for admin approval')
                    # Redirect to a page indicating that the account is not verified
                    # return redirect('account_not_verified')
            elif user.is_donor:
                return redirect('donator_home')
        else:
            messages.info(request, 'Invalid Credentials')
    return render(request, 'login_page.html')
# def login_page(request):
#     if request.method == 'POST':
#         username = request.POST.get('uname')
#
#         password = request.POST.get('pass')
#
#         user = authenticate(request, username=username, password=password)
#         print(user)
#         if user is not None:
#             login(request,user)
#             if user.is_staff:
#
#                 return redirect('admin_base')
#             elif user.is_users:
#                 print(user.users.verified)
#                 return redirect('user_home')
#
#             elif user.is_donor:
#
#                 return redirect('donator_home')
#
#
#         else:
#             messages.info(request, 'Invalid Credentials')
#     return render(request,'login_page.html')



class RegistrationView(View):

    def get(self, request):
        user = LoginRegister()
        donor_form = DonorRegister()
        user_form = UsersRegister()

        return render(request, 'index.html', {"user": user, "donor_form": donor_form,'user_form':user_form})

    def post(self, request):
        user = LoginRegister(request.POST)
        user_form = UsersRegister(request.POST, request.FILES)
        donor_form = DonorRegister(request.POST)




        if user.is_valid() and user_form.is_valid():


                 a = user.save(commit=False)
                 print(a)

                 a.is_users = True
                 a.save()
                 user1 = user_form.save(commit=False)

                 user1.user = a
                 user1.save()
                 return redirect('login_page')




        return render(request,'index.html', {"user": user, "donor_form": donor_form, "user_form": user_form})



def logout_view(request):
    logout(request)
    return redirect('login_page')