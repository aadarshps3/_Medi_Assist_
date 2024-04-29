from django.urls import path

from Mediassist_app import views, user_views, admin_views, company_views
from Mediassist_app.admin_views import CompanyRegistrationView
from Mediassist_app.views import RegistrationView

urlpatterns = [
   # path("",views.Test,name='test'),
   # path("",views.landing_page,name="landing"),
   path('', RegistrationView.as_view(), name='registration'),
   path("login_page",views.login_page,name="login_page"),
   path("admin_base",views.admin_base,name="admin_base"),
   path("donator_home",views.donator_home,name="donator_home"),
   path("user_home",views.user_home,name="user_home"),

   path("logout_view/",views.logout_view,name='logout_view'),

   #user

   path("med_add",user_views.med_add,name="med_add"),
   path("med_view", user_views.med_view, name="med_view"),
   path("med_view1", user_views.med_view1, name="med_view1"),
   path("cash_add",user_views.cash_add,name='cash_add'),
   path("cash_view",user_views.cash_view,name="cash_view"),
   path("feedback", user_views.feedback, name="feedback"),
   path("feedback_view", user_views.feedback_view, name="feedback_view"),
   path("pay_status", user_views.pay_status, name="pay_status"),


   #admin

   path('CompanyRegistrationView', CompanyRegistrationView.as_view(), name='CompanyRegistrationView'),
   path('cmp_list',admin_views.cmp_list,name="cmp_list"),
   path('user_list',admin_views.user_list,name='user_list'),
   path("admin_approval",admin_views.admin_approval,name='admin_approval'),
   path('approve_donation/<int:id>/',admin_views.approve_donation, name='approve_donation'),
   path('reject_donation/<int:id>/',admin_views.reject_donation, name='reject_donation'),
   # path("admin_approval",admin_views.admin_approval,name='admin_approval'),
   path('requests',admin_views.requests,name='requests'),
   path('export-medicine',admin_views.export_medicines,name='export-medicine'),



   path('cash_requests',admin_views.cash_requests,name='cash_requests'),

   path("admin_cash_approval", admin_views.admin_cash_approval, name='admin_cash_approval'),
   path('approve_cash_donation/<int:id>/', admin_views.approve_cash_donation, name='approve_cash_donation'),
   path('reject_cash_donation/<int:id>/', admin_views.reject_cash_donation, name='reject_cash_donation'),
   path("users_approval/<int:id>/",admin_views.users_approval,name='users_approval'),
   path("users_reject/<int:id>/",admin_views.users_reject,name='users_reject'),
   path("generate_report",admin_views.generate_report,name='generate_report'),
   path("generate_cash_report",admin_views.generate_cash_report,name='generate_cash_report'),


   path('feedbacks',admin_views.feedbacks, name='feedbacks'),
   path('reply_feedback/<int:id>/',admin_views.reply_feedback, name='reply_feedback'),

   #company
   path("med_view_cmp", company_views.med_view_cmp, name="med_view_cmp"),
   path('donate/<int:id>/', company_views.donate, name='donate'),
   path("cash_view_cmp", company_views.cash_view_cmp, name="cash_view_cmp"),
   path('donate_cash/<int:id>/', company_views.donate_cash, name='donate_cash'),
   path("med_donation",company_views.MyDonations,name='med_donations'),
   path('CashDonation',company_views.CashDonation,name='CashDonation'),
   path('payment/<int:id>/',company_views.payment,name='payment'),

]