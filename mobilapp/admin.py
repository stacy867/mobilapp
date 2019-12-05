from django.contrib import admin
from mobilapp.models import Account,Category,CompanyProfile,Services,Booking


# Register your models here.

admin.site.register(Account)
admin.site.register(Services)
admin.site.register(Booking)
admin.site.register(Category)
admin.site.register(CompanyProfile)

