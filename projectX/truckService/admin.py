from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(DischargePiont)
admin.site.register(customerProfile)
admin.site.register(staffProfile)
admin.site.register(Location)
admin.site.register(Trucks)
admin.site.register(Role)
admin.site.register(truckFuel)
admin.site.register(tripData)

admin.site.register(staffExpense)
admin.site.register(truckExpense)
admin.site.register(officeExpense)
admin.site.register(otherExpense)
admin.site.register(Expenses)
admin.site.register(AllPayments)
admin.site.register(Attendance)
admin.site.register(Leaves)
admin.site.register(UserProfile)  
admin.site.register(nft_detail)  
admin.site.register(billExpense )  
admin.site.register(deduction )  
admin.site.register(remaining_deduction )  
