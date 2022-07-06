from pickle import TRUE
from celery import maybe_signature
from django.http import JsonResponse
from .models import staffProfile,Trucks
from datetime import date, timedelta
from .serializers import *
from rest_framework.response import Response
def expiry_alerts(request):
    current_date=date.today()
    print("Current date",current_date)
    current_date_15=current_date+timedelta(days=15)
    print("Date after 15 days",current_date_15)
    visa_expiry_alert1=staffProfile.objects.filter(visaExpiry__gt=current_date,visaExpiry__lte=current_date_15).values_list("user__first_name",flat=True)
    visa_expiry_alert2=staffProfile.objects.filter(visaExpiry__gt=current_date,visaExpiry__lte=current_date_15).values_list("user__last_name",flat=True)
    visa_expiry_alert1=list(visa_expiry_alert1)
    visa_expiry_alert2=list(visa_expiry_alert2)
    visa_expiry_alert=[x+" "+y for x,y in zip(visa_expiry_alert1,visa_expiry_alert2)]

    visa_expired1=staffProfile.objects.filter(visaExpiry__lte=current_date).values_list("user__first_name",flat=True)
    visa_expired2=staffProfile.objects.filter(visaExpiry__lte=current_date).values_list("user__last_name",flat=True)
    visa_expired1=list(visa_expired1)
    visa_expired2=list(visa_expired2)
    visa_expired=[x+" "+y for x,y in zip(visa_expired1,visa_expired2)]

    print("Expiry alert",visa_expiry_alert)
    print("Expired",visa_expired)

    passport_expiry_alert1=staffProfile.objects.filter(passportExpiry__gt=current_date,passportExpiry__lte=current_date_15).values_list("user__first_name",flat=True)
    passport_expiry_alert2=staffProfile.objects.filter(passportExpiry__gt=current_date,passportExpiry__lte=current_date_15).values_list("user__last_name",flat=True)
    passport_expiry_alert1=list(passport_expiry_alert1)
    passport_expiry_alert2=list(passport_expiry_alert2)
    passport_expiry_alert=[x+" "+y for x,y in zip(passport_expiry_alert1,passport_expiry_alert2)]

    passport_expired1=staffProfile.objects.filter(passportExpiry__lte=current_date).values_list("user__first_name",flat=True)
    passport_expired2=staffProfile.objects.filter(passportExpiry__lte=current_date).values_list("user__last_name",flat=True)
    passport_expired1=list(passport_expired1)
    passport_expired2=list(passport_expired2)
    passport_expired=[x+" "+y for x,y in zip(passport_expired1,passport_expired2)]
    print("Expiry alert",passport_expiry_alert)
    print("Expired",passport_expired)   

    truck_expiry_alert=Trucks.objects.filter(MulikaExpDate__gt=current_date,MulikaExpDate__lte=current_date_15).values_list("truckNumber",flat=True)
    truck_expiry_alert=list(truck_expiry_alert)
    print("ssssssss",truck_expiry_alert)

    
    truck_expired=Trucks.objects.filter(MulikaExpDate__lte=current_date).values_list("truckNumber",flat=True)
    truck_expired=list(truck_expired)
    print("Expiry alert",truck_expiry_alert)
    print("Expired",truck_expired)
    
    
    return  {'visa_expiry_alert':visa_expiry_alert,'visa_expired':visa_expired,'passport_expiry_alert':passport_expiry_alert,'passport_expired':passport_expired,'truck_expiry_alert':truck_expiry_alert,'truck_expired':truck_expired}