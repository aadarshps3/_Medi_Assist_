from django.contrib import admin

# Register your models here.
from Mediassist_app import models

admin.site.register(models.Login_view)
admin.site.register(models.users)
admin.site.register(models.donor)
admin.site.register(models.Medicine_request)
admin.site.register(models.Medicine_approval)
admin.site.register(models.Cash_approval)
admin.site.register(models.Cash_request)

