from contextvars import Context
from functools import partial
from django.db.models import indexes
from django.db.models.fields import DateField
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template import context
from rest_framework import serializers
from .forms import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import random
from .models import *
from .serializers import *
from django.core.paginator import Paginator
from django.db.models import Sum
from rest_framework import status
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from datetime import date
import random


from truckService.utils import render_to_pdf #created in step 4

def set_if_not_none(mapping, key, value):
    if value:
        mapping[key] = value
    return mapping



def index(request):
    u=request.user
    if(u.is_authenticated):
        return render(request,'index.html')
    return render(request,'login.html',{'user':u})

def login(request):
    
    if request.method=='POST':
        check=False
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('/index/')
        else:
            check=True
        # form = AuthenticationForm(data=request.POST)
        # print(form.is_valid())
        
        # if form.is_valid():
        #     return render(request,'index.html')
        # else:
        #     check=True
    else:
        # form=AuthenticationForm()
        check=False
    return render(request,'login.html',{'check':check})

def logout(request):
        auth_logout(request)
        return render(request,'login.html')


    # Trip Data Crud
def tripdata(request):
    form=tripForm()
    return render(request,'addTripData.html',{'form': form})


@api_view(['GET'])
def customerlocationfetch(request):
    val=request.GET.get("value")
    custLocation=customerProfile.objects.get(id=val)
    serCustomer=customerSerializer(custLocation)

    return Response({"customerLocation":serCustomer.data})

@api_view(['POST'])
def addTripdata(request):
    confirm=False
    if request.method == 'POST':
        Trip_Form = tripForm(request.POST)
        
        if Trip_Form.is_valid():
            Trip_Form.save()

            confirm = True
        else:
            print("hhhhhh",Trip_Form.errors)

    return Response({'confirm':confirm}) 

def manageTripdata(request):

    return render(request,'manageTripData.html')

@api_view(['GET','POST'])
def tripslistshow(request):

    if request.method == 'POST':
        trips= tripData.objects.get(id=request.POST.get('id'))
        
        serializer1=tripdataSerializer(trips)
        
        custom=customerProfile.objects.all()
        custom_serializer=customerSerializer(custom,many=True)

        tripTrucks=Trucks.objects.all()
        tripTrucks_serializer=trucksSerializer(tripTrucks,many=True)
       
        tripDriver=staffProfile.objects.all()
        tripDriver_serializer=staffSerializer(tripDriver,many=True)
        # print("rrrrrrrrrrrrrrrrrrrrrrrrr",serializer1.data)
        return Response({'tripdata': serializer1.data,'tripcustomer':custom_serializer.data ,'tripdirver':tripDriver_serializer.data,'triptruck':tripTrucks_serializer.data})
    
    
    
    # customerUserDetail=User.objects.all().exclude(username=request.user.username)
    points=tripData.objects.all()
    # serializedUser=UserSerializer(customerUserDetail,many=True)
    # locations=Location.objects.all()
    # location_serializer=locationSerializer(locations,many=True)
    serializedDischarge=fetchtripdataSerializer(points,many=True)
    
    return Response({'tripdata':serializedDischarge.data})



 


@api_view(['POST'])
def updateTripdata(request,pk):
    # new_obj =  User.objects.filter(id=pk).first()
    new_obj2 =  tripData.objects.get(id=pk)
    print("cccccccccccccccccccccccccccccccccccccc",)
    print("dddddddddddddddddddddddddddddddddddddd",)
    updatecheck = False
    customer_id=request.POST['customer']
    cutomer_obj=customerProfile.objects.get(id=customer_id)
    oldnft=new_obj2.nft
    newnft=int(request.POST['nft'])
   
    if oldnft>newnft:
        gnft=oldnft-newnft
        cutomer_obj.noOfTrips -=gnft
        cutomer_obj.save()
    elif oldnft<newnft:
        lnft=newnft-oldnft
        cutomer_obj.noOfTrips +=lnft
        cutomer_obj.save()
    if request.method == 'POST':
         
        trip_Data = tripdataSerializer(new_obj2, data=request.POST, partial=True)
        
        if trip_Data.is_valid():
            
            trip_Data.save()
            updatecheck=True
    return Response({'updatecheck':updatecheck})

@api_view(['GET'])
def deleteTripdata(request):
   user_id = request.GET.get('id')
   tripData.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})





#   Customer CRUD APIS

def customerView(request):
    
    confirm=False
    # if request.method == 'POST':
        
    #     user_form = userForm(request.POST)
    #     customer_form = customer(request.POST)
    #     if user_form.is_valid() and customer_form.is_valid():
    #         obj2 = user_form.save(commit=False)
    #         obj=customer_form.save(commit=False)
            
    #         uname=obj2.first_name+obj2.last_name+str(random.randint(0,1000))
    #         obj2.username=uname
    #         obj2.save()
    #         obj.user=obj2
    #         obj.type_id=1
    #         obj.save()

    #         confirm = True
    form1=userForm()
    cform=customer()
    return render(request,'customer.html',{'cform':cform,'form1':form1,'confirm':confirm})




def createCustomer(request):
    confirm=False
    if request.method == 'POST':
        user_form = userForm(request.POST)
        customer_form = customer(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            obj2 = user_form.save(commit=False)
            obj=customer_form.save(commit=False) 
            
            uname=obj2.first_name+obj2.last_name+str(random.randint(0,1000))
            obj2.username=uname
            obj2.save()
            obj.user=obj2
            obj.type=Role.objects.get(id=1)
            obj.save()
            confirm = True
    return JsonResponse({'confirm':confirm})    


def customerList(request):

    return render(request,'customerslist.html')


# def customerList(request):
#     customers=User.objects.all().exclude(username=request.user.username)
    
#     if request.method == 'POST':
#         customerUser = User.objects.get(id=request.POST.get('id'))
#         profile=userProfile.objects.get(user=customerUser)
#         serializer=UserSerializer(customerUser)
#         serializer1=profileSerializer(profile)
#         return JsonResponse({'specificCustomer': serializer.data,'customerdata': serializer1.data})
#     return render(request,'customerslist.html',{'customers':customers})

@api_view(['GET', 'POST'])
def customerListShow(request):

    if request.method == 'POST':
        customerUser = User.objects.get(id=request.POST.get('id'))
        # print("*********************",request.POST.get('id'))
        profile=customerProfile.objects.get(user=customerUser)
        # serializer=UserSerializer(customerUser)
        serializer1=customerSerializer(profile)
        

        # print("rrrrrrrrrrrrrrrrrrrrrrrrr",serializer1.data)
        return Response({'customerdata': serializer1.data})
    
    
    # customerUserDetail=User.objects.all().exclude(username=request.user.username)
    customerProfiles=customerProfile.objects.filter(type=1).exclude(user=request.user)
    # serializedUser=UserSerializer(customerUserDetail,many=True)
    # locations=Location.objects.all()
    # location_serializer=locationSerializer(locations,many=True)
    serializedProfile=fetchCustomerprofileSerializer(customerProfiles,many=True)
    
    return Response({'customerProfile':serializedProfile.data})


def updateCustomer(request,pk):
    new_obj =  User.objects.filter(id=pk).first()
    new_obj2 =  customerProfile.objects.get(user=new_obj)
    updatecheck = False
    if request.method == 'POST':
        
        serializerUser = UserSerializer(new_obj, data=request.POST, partial=True)
        updated_customer = customerSerializer(new_obj2, data=request.POST, partial=True)
        # print("sssssssssssssssssssssssssssssssssssssss",dischargePoints.data)
        if serializerUser.is_valid() and updated_customer.is_valid():
            # print("sssssssssssssssssssssssssssssssssssssss",dischargePoints.validated_data)
            serializerUser.save()
            instance=updated_customer.save()
            
            vat=instance.Vat
            tripcharges=instance.tripCharges
            totalnft=instance.noOfTrips
            totalcharges=tripcharges*totalnft
            vat_amount=  totalcharges*vat  
            vat_amount=vat_amount/100  
            instance.vatAmount=vat_amount
            instance.ReceivableAmount=totalcharges+vat_amount
            instance.save()


            updatecheck=True
    return JsonResponse({'updatecheck':updatecheck})
  

def deleteCustomer(request):
   user_id = request.GET.get('id')
   User.objects.get(id=user_id).delete()
   
  
   return HttpResponse({'confirm':True})



#    DischargePiont CRUD APIS


def dischargeListShow(request):

    if request.method == 'POST':
        editPoint= DischargePiont.objects.get(id=request.POST.get('id'))
        # print("*********************",request.POST.get('id'))
        # profile=userProfile.objects.get(user=customerUser)
        # serializer=UserSerializer(customerUser)
        serializer1=dischargeSerializer(editPoint)
        
        locations=Location.objects.all()
        location_serializer=locationSerializer(locations,many=True)
        # print("rrrrrrrrrrrrrrrrrrrrrrrrr",serializer1.data)
        return JsonResponse({'dischargePoints': serializer1.data,'locations':location_serializer.data})
    
    
    # customerUserDetail=User.objects.all().exclude(username=request.user.username)
    points=DischargePiont.objects.all()
    # serializedUser=UserSerializer(customerUserDetail,many=True)
    # locations=Location.objects.all()
    # location_serializer=locationSerializer(locations,many=True)
    serializedDischarge=fetchdischargeSerializer(points,many=True)
    print(">>>>>>>>>>>",serializedDischarge.data)
    return JsonResponse({'dischargePoints':serializedDischarge.data})

def createDischarge(request):
    
    dischargeForm1=dischargeForm()
    return render(request,'addDischargepoint.html',{'dform':dischargeForm})

def addDischarge(request):
    confirm=False
    if request.method == 'POST':
        user_form = dischargeForm(request.POST)
        
        if user_form.is_valid():
            user_form.save()
            confirm = True

    return JsonResponse({'confirm':confirm})  

def dischargepointList(request):

    return render(request,'manageDischargepoint.html')

def updatedischargepoint(request,pk):
    # new_obj =  User.objects.filter(id=pk).first()
    new_obj2 =  DischargePiont.objects.get(id=pk)
    print(">><<<<<<<<<<<<<<<<<<<",new_obj2)
    updatecheck = False
    if request.method == 'POST':
        
        dischargePoints = dischargeSerializer(new_obj2, data=request.POST, partial=True)
        # print("sssssssssssssssssssssssssssssssssssssss",dischargePoints.data)
        if dischargePoints.is_valid():
            print("sssssssssssssssssssssssssssssssssssssss",dischargePoints.validated_data)
            
            dischargePoints.save()
            updatecheck=True
    return JsonResponse({'updatecheck':updatecheck})

@api_view(['GET'])
def deleteDischargepoint(request):
   user_id = request.GET.get('id')
   DischargePiont.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})


# Trucks CRUD

def createTrucks(request):
    
    tform=truckForm()
    return render(request,'addTrucks.html',{'tform':tform})

@api_view(['GET', 'POST'])
def addTrucks(request):
    confirm=False
    if request.method == 'POST':
       
        truck_form = truckForm(request.POST)
        
        if truck_form.is_valid():
            truck_form.save()
            confirm = True

    return Response({'confirm':confirm}) 

    # Manage Truck View 
def managetrucks(request):

    return render(request,'managetrucks.html')

@api_view(['GET', 'POST'])
def trucklistshow(request):
    print("ooooooooooooooooooooooooooooooooooooooooooookkk")
    if request.method == 'POST':
        editTruck= Trucks.objects.get(truckNumber=request.POST.get('id'))
        # print("*********************",request.POST.get('id'))
        # profile=userProfile.objects.get(user=customerUser)
        # serializer=UserSerializer(customerUser)
        serializer1=trucksSerializer(editTruck)
        
        # locations=Location.objects.all()
        # location_serializer=locationSerializer(locations,many=True)
        # print("rrrrrrrrrrrrrrrrrrrrrrrrr",serializer1.data)
        return JsonResponse({'trucks': serializer1.data})
    
    # customerUserDetail=User.objects.all().exclude(username=request.user.username)
    trucks=Trucks.objects.all()
    
    # serializedUser=UserSerializer(customerUserDetail,many=True)
    # locations=Location.objects.all()
    # location_serializer=locationSerializer(locations,many=True)
    serializedTrucks=trucksSerializer(trucks,many=True)
    # print("$$$$$$$$$$$$$$$$$$$$$$",serializedTrucks.data)
    return Response({'trucks':serializedTrucks.data})


@api_view(['GET', 'POST'])
def updateTruck(request,truckno):
    print("-------------------",truckno)
    # new_obj =  User.objects.filter(id=pk).first()
    new_obj2 = Trucks.objects.get(truckNumber=truckno)
    print(">><<<<<<<<<<<<<<<<<<<",new_obj2)
    updatecheck = False
    if request.method == 'POST':
        print("sssssssssssssssssssssssssssssssssssssss",request.POST)
        trucksSer = trucksSerializer(new_obj2, data=request.POST, partial=True)
        
        if trucksSer.is_valid():
            print("sssssssssssssssssssssssssssssssssssssss",trucksSer.validated_data)
            
            trucksSer.save()
            updatecheck=True
    return Response({'updatecheck':updatecheck})

@api_view(['GET', 'POST'])    
def deleteTruck(request):
   user_id = request.GET.get('id')
   print("-----s------------",user_id)
   Trucks.objects.get(truckNumber=user_id).delete()
   
  
   return Response({'confirm':True})



def manageFuelData(request):

    return render(request,'fuelData.html')

   

@api_view(['GET'])
def FuelDataShow(request):
#   This code will wakeup when i will update
    #     editTruck= Trucks.objects.get(truckNumber=request.POST.get('id'))
    #     serializer1=trucksSerializer(editTruck)
    #     return JsonResponse({'trucks': serializer1.data})
    
    fuel=truckFuel.objects.all()
    print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY",fuel)
    serializedFuel=truckFuelSerializer(fuel,many=True)
    print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYX")
    return Response({'fuel':serializedFuel.data})






#   Staff CRUD APIS

def createStaff(request):
    
    confirm=False

    form1=userForm()
    sform=staff()
    return render(request,'createstaff.html',{'sform':sform,'form1':form1,'confirm':confirm})



@api_view(['POST'])
def addstaff(request):
    confirm=False
    if request.method == 'POST':
        user_form = userForm(request.POST)
        staff_form = staff(request.POST)
        print(">>>>>>>>>>>>>>>>>>>>>>>>",staff_form)
        if user_form.is_valid() and staff_form.is_valid():
            obj2 = user_form.save(commit=False)
            obj=staff_form.save(commit=False)
            
            uname=obj2.first_name+obj2.last_name+str(random.randint(0,1000))
            obj2.username=uname
            obj2.save()
            obj.user=obj2
            obj.type=Role.objects.get(id=2)
            obj.save()
            confirm = True
    return Response({'confirm':confirm})    


def staffList(request):

    return render(request,'managestaff.html')

@api_view(['GET', 'POST'])
def staffListShow(request):

    if request.method == 'POST':
        staffUser = User.objects.get(id=request.POST.get('id'))
        profile=staffProfile.objects.get(user=staffUser)
        serializer1=staffSerializer(profile)
       
        return Response({'staffdata': serializer1.data})

    staffProfiles=staffProfile.objects.filter(type=2).exclude(user=request.user)
    serializedProfile=fetchStaffprofileSerializer(staffProfiles,many=True)
    
    return Response({'staffProfile':serializedProfile.data})

@api_view(['POST'])
def updateStaff(request,pk):
    new_obj =  User.objects.filter(id=pk).first()
    new_obj2 =  staffProfile.objects.get(user=new_obj)
    print(">><<<<<<<<<<<<<<<<<<<",new_obj2)
    updatecheck = False
    if request.method == 'POST':
        
        serializerUser = UserSerializer(new_obj, data=request.POST, partial=True)
        staff = staffSerializer(new_obj2, data=request.POST, partial=True)
        # print("sssssssssssssssssssssssssssssssssssssss",dischargePoints.data)
        if serializerUser.is_valid() and staff.is_valid():
            # print("sssssssssssssssssssssssssssssssssssssss",dischargePoints.validated_data)
            serializerUser.save()
            staff.save()
            updatecheck=True
    return Response({'updatecheck':updatecheck})
  

def deleteStaff(request):
   user_id = request.GET.get('id')
   User.objects.get(id=user_id).delete()
   
  
   return HttpResponse({'confirm':True})


    # Expnses Cruds
    # create view
def Expenses(request):
    
    sform=staffexForm()
    tform=truckexForm()
    oform=officeexForm()
    otherform=otherexForm()
    return render(request,'Expenses.html',{'sform':sform,'tform':tform,'oform':oform,'otherform':otherform})
    

@api_view(['GET', 'POST'])
def addExpenses(request):
    confirm=False
    bill_no=100000000


    no = ''.join(str(random.randint(0,10)) for x in range(5))
    bill_number=bill_no+int(no)
    if request.method == 'POST':
       
        staffForm = staffexForm(request.POST)
        truckForm = truckexForm(request.POST)
        officeForm = officeexForm(request.POST)
        otherForm = otherexForm(request.POST)
        if staffForm.is_valid():
            obj=staffForm.save()
            
            obj.totalAmount=obj.salary+obj.visaFee+obj.eidFee+obj.medicalIns+obj.overTime+obj.others
            obj.save()
            payments=InvoicePaymentSerializer(data={"date":date.today(),"user":1,"vendor":"-----","payment_no":bill_number,"payment_type":2,"payment_type":2,"expense_type":"Staff Expense","payment_amount":obj.totalAmount,"payment_status":False},partial=True)
            if payments.is_valid():
                payments.save()
            confirm = True
            
        elif truckForm.is_valid():
            obj1=truckForm.save()
            obj1.totalAmount=obj1.renewalFee+obj1.fuel+obj1.maintenance+obj1.repair_replace+obj1.parking+obj1.others
            obj1.save()
            payments=InvoicePaymentSerializer(data={"date":date.today(),"user":1,"vendor":"-----","payment_no":bill_number,"payment_type":2,"payment_type":2,"expense_type":"Truck Expense","payment_amount":obj1.totalAmount,"payment_status":False},partial=True)
            if payments.is_valid():
                payments.save()
            confirm = True
        elif officeForm.is_valid():
            obj2=officeForm.save()
            obj2.totalAmount=obj2.officeRent+obj2.utilityBills+obj2.stationary+obj2.kitchen+obj2.others
            obj2.save()
            payments=InvoicePaymentSerializer(data={"date":date.today(),"user":1,"vendor":obj2.vendor,"payment_no":bill_number,"payment_type":2,"expense_type":"office Expense","payment_amount":obj2.totalAmount,"payment_status":False},partial=True)
            if payments.is_valid():
                payments.save()
            confirm = True
        elif otherForm.is_valid():
            obj3=otherForm.save()
            obj3.totalAmount=obj3.expenseAmount 
            obj3.save()
            payments=InvoicePaymentSerializer(data={"date":date.today(),"user":1,"vendor":obj3.vendor,"payment_no":bill_number,"payment_type":2,"expense_type":obj3.expenseName+" Expense","payment_amount":obj3.totalAmount,"payment_status":False},partial=True)
            if payments.is_valid():
                payments.save()
            confirm = True
            
        
        


        




    return Response({'confirm':confirm}) 

    # Manage Staff Expenses View 
def manageStaffExpense(request):

    return render(request,'manageStaffExpense.html')

@api_view(['GET', 'POST'])
def staffExpenseListshow(request):
    if request.method == 'POST':
        staffex= staffExpense.objects.get(id=request.POST.get('id'))
        
        serializer1=staffexSerializer(staffex)
        
        tripDriver=staffProfile.objects.all()
        tripDriver_serializer=staffSerializer(tripDriver,many=True)
        # print("rrrrrrrrrrrrrrrrrrrrrrrrr",serializer1.data)
        return Response({'staffexpenses': serializer1.data,'staffNames':tripDriver_serializer.data})
    
    staffexpenses=staffExpense.objects.all()
    serializedDischarge=fetchstaffexSerializer(staffexpenses,many=True)
    
    return Response({'staffexpenses':serializedDischarge.data})


@api_view(['GET', 'POST'])
def updateStaffExpense(request,pk):
    
    # new_obj =  User.objects.filter(id=pk).first()
    new_obj2 = staffExpense.objects.get(id=pk)
    
    updatecheck = False
    if request.method == 'POST':
        
        staffexserials = staffexSerializer(new_obj2, data=request.POST, partial=True)
        
        if staffexserials.is_valid():
            
            staffobj=staffexserials.save()
            staffobj.totalAmount=staffobj.totalAmount=staffobj.salary+staffobj.visaFee+staffobj.eidFee+staffobj.medicalIns+staffobj.overTime+staffobj.others
            staffobj.save()
            updatecheck=True
    return Response({'updatecheck':updatecheck})

@api_view(['GET', 'POST'])    
def deleteStaffExpense(request):
   user_id = request.GET.get('id')
   print("-----s------------",user_id)
   staffExpense.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})


# Manage Staff Expenses View 
def manageTruckExpense(request):

    return render(request,'manageTruckExpense.html')


@api_view(['GET', 'POST'])
def truckExpenseListshow(request):
    if request.method == 'POST':
        print("TTTTTTTTTTTTTTTTTTTTTTT",request.POST.get('id'))
        staffex= truckExpense.objects.get(id=request.POST.get('id'))
        
        serializer1=truckexSerializer(staffex)
    
        truckex=Trucks.objects.all()
        truckex_serializer=trucksSerializer(truckex,many=True)
        
        return Response({'trucksexpense': serializer1.data,'truckNumbers':truckex_serializer.data})
   
    truckexpenses=truckExpense.objects.all()
    
    serializedtruckex=fetchtruckexSerializer(truckexpenses,many=True)
    
    return Response({'trucksexpense':serializedtruckex.data})


@api_view(['GET', 'POST'])
def updateTruckExpense(request,pk):
    print("ddddddddddddddddddddddddddddd",pk)
    # new_obj =  User.objects.filter(id=pk).first()
    new_obj2 = truckExpense.objects.get(id=pk)
    
    updatecheck = False
    if request.method == 'POST':
        
        officeexserials = truckexSerializer(new_obj2, data=request.POST, partial=True)
        
        if officeexserials.is_valid():
            
            truckobj=officeexserials.save()
            truckobj.totalAmount=truckobj.renewalFee+truckobj.fuel+truckobj.maintenance+truckobj.repair_replace+truckobj.parking+truckobj.others
            truckobj.save()
            updatecheck=True
    return Response({'updatecheck':updatecheck})

@api_view(['GET', 'POST'])    
def deleteTruckExpense(request):
   user_id = request.GET.get('id')
   print("-----s------------",user_id)
   truckExpense.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})



# Manage Staff Expenses View 
def manageOfficeExpense(request):

    return render(request,'manageOfficeExpense.html')

@api_view(['GET', 'POST'])
def officeExpenseListshow(request):
     if request.method == 'POST':
        print("TTTTTTTTTTTTTTTTTTTTTTT",request.POST.get('id'))
        officeex= officeExpense.objects.get(id=request.POST.get('id'))
        serializer1=officeexSerializer(officeex)
        return Response({'officesexpense': serializer1.data})

     truckexpenses=officeExpense.objects.all()
     serializedofficeex=fetchofficeexSerializer(truckexpenses,many=True)
     return Response({'officesexpense':serializedofficeex.data})



@api_view(['GET', 'POST'])
def updateOfficeExpense(request,pk):
    
    new_obj2 = officeExpense.objects.get(id=pk)
    
    updatecheck = False
    if request.method == 'POST':
        
        officeexserials = officeexSerializer(new_obj2, data=request.POST, partial=True)
        
        if officeexserials.is_valid():
            
            officeobj=officeexserials.save()
            officeobj.totalAmount=officeobj.officeRent+officeobj.utilityBills+officeobj.stationary+officeobj.kitchen+officeobj.others
            officeobj.save()
            updatecheck=True
    return Response({'updatecheck':updatecheck})

@api_view(['GET', 'POST'])    
def deleteOfficeExpense(request):
   user_id = request.GET.get('id')

   officeExpense.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})


# Manage Staff Expenses View 
def manageOtherExpense(request):

    return render(request,'manageOtherExpense.html')

@api_view(['GET', 'POST'])
def otherExpenseListshow(request):
    if request.method == 'POST':
        
        officeex= otherExpense.objects.get(id=request.POST.get('id'))
        
        serializer1=otherexSerializer(officeex)
      
        return Response({'otherexpense': serializer1.data})
    otherexpenses=otherExpense.objects.all()
   
    serializedotherex=fetchotherexSerializer(otherexpenses,many=True)
    
    return Response({'otherexpense':serializedotherex.data})



@api_view(['GET', 'POST'])
def updateOtherExpense(request,pk):
   new_obj2 = otherExpense.objects.get(id=pk)
    
   updatecheck = False
   if request.method == 'POST':
        
        otherexserials = otherexSerializer(new_obj2, data=request.POST, partial=True)
        
        if otherexserials.is_valid():
            
            othereobj=otherexserials.save()
            othereobj.totalAmount=othereobj.expenseAmount   
            othereobj.save()
            updatecheck=True
   return Response({'updatecheck':updatecheck})


@api_view(['GET', 'POST'])    
def deleteOtherExpense(request):
   user_id = request.GET.get('id')
   print("-----s------------",user_id)
   otherExpense.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})



# Manage Staff Expenses View 
def manageTotalExpense(request):

    return render(request,'manageTotalExpense.html')

@api_view(['GET', 'POST'])
def totalExpenseListshow(request):
   
    totalStaffExpense=staffExpense.objects.aggregate(Sum('totalAmount'))
    totalOfficeExpense=officeExpense.objects.aggregate(Sum('totalAmount'))
    totalOtherExpense=otherExpense.objects.aggregate(Sum('totalAmount'))
    totalTruckExpense=truckExpense.objects.aggregate(Sum('totalAmount'))
    totalExpense=totalStaffExpense["totalAmount__sum"]+totalOfficeExpense["totalAmount__sum"]+totalOtherExpense["totalAmount__sum"]+totalTruckExpense["totalAmount__sum"]
    
    return Response({'staffexpense':totalStaffExpense,'officeexpense':totalOfficeExpense,'otherexpense':totalOtherExpense,'truckexpense':totalTruckExpense,'totalExpense':totalExpense,})


# @api_view(['GET', 'POST'])
# def updateTotalExpense(request,truckno):
#     print("-------------------",truckno)
#     # new_obj =  User.objects.filter(id=pk).first()
#     new_obj2 = Trucks.objects.get(truckNumber=truckno)
#     print(">><<<<<<<<<<<<<<<<<<<",new_obj2)
#     updatecheck = False
#     if request.method == 'POST':
#         print("sssssssssssssssssssssssssssssssssssssss",request.POST)
#         trucksSer = trucksSerializer(new_obj2, data=request.POST, partial=True)
        
#         if trucksSer.is_valid():
#             print("sssssssssssssssssssssssssssssssssssssss",trucksSer.validated_data)
            
#             trucksSer.save()
#             updatecheck=True
#     return Response({'updatecheck':updatecheck})

# @api_view(['GET', 'POST'])    
# def deleteTotalExpense(request):
#    user_id = request.GET.get('id')
#    print("-----s------------",user_id)
#    Trucks.objects.get(truckNumber=user_id).delete()
   
  
#    return Response({'confirm':True})



# Generate Invoice
def generateInvoice(request):
    form=customerField()
    return render(request,'generateInvoice.html',{'form':form})

   # Generate Invoice
@api_view(['POST'])
def createInvoice(request):
    filtered_trips=''
    if request.method=="POST":
        list={}
       
        from_date = request.POST.get("fromDate")
        to_date = request.POST.get("toDate")
        customer = request.POST.get("customer")
        
        # if from_date and to_date:
        #     fromdate=datetime.strptime(from_date , '%Y-%m-%d')
        #     todate =datetime.strptime(to_date , '%Y-%m-%d')
        
        set_if_not_none(list,'date__gte',from_date)
        set_if_not_none(list,'date__lte',to_date)
        returned_list=set_if_not_none(list,'customer',customer) 
      
        filter_trips=tripData.objects.filter(**returned_list)
       
        # to_date =  "sss"
        # customer = "sss"
        # if from_date and to_date:
        #     fromdate=datetime.strptime(from_date , '%Y-%m-%d')
        #     todate =datetime.strptime(to_date , '%Y-%m-%d')
            
        #     filtered_trips=tripData.objects.filter(Q(date__gte=fromdate.date()) & Q(date__lte=todate.date()))
        # if customer:
        #     filtered_trips=tripData.objects.filter(Q(id__in=filtered_trips) & Q(customer=customer))
         
        filtered_serialized_trips=tripdataSerializer(filter_trips,many=True)
    

    return Response({'tripDetails':filtered_serialized_trips.data},status.HTTP_200_OK)
invoice_no=1000000000

def Invoice(request):
    no = ''.join(str(random.randint(0,10)) for x in range(5))
    invoice_number=invoice_no+int(no)
    
    if request.method=='POST':
        
        customer=customerProfile.objects.get(id=request.POST["customer"])
        from_date = request.POST["fromDate"]
        to_date = request.POST["toDate"]
        csrf = request.POST["csrfmiddlewaretoken"]

        context={
            'fromDate':request.POST["fromDate"],
            'toDate' : request.POST["toDate"],
             'customer' :  customer,
             'location' :  customer.location,
              'date'  :  date.today(),
              'csrf':csrf,
              'invoiceNo':invoice_number,
              'record_no':invoice_no-99990,
        }
        
        return render(request,'invoice.html',context)

def printInvoice(request):
    
    return render(request,'invoice_print.html')

@api_view(['POST'])
def saveinvoice(request):
    
    if request.method=="POST":
        customer=customerProfile.objects.get(id=request.POST["customer"])
        invoice_number=request.POST["payment_no"]
        payment_amount=int(request.POST["payment_amount"])
        # payment type '1' means Invoice
        payments=InvoicePaymentSerializer(data={"date":date.today(),"user":customer.user.id,"payment_no":invoice_number,"payment_type":1,"payment_amount":payment_amount,"payment_status":False},partial=True)
        if payments.is_valid():
            payments.save()
        return Response(status.HTTP_200_OK)
    return Response({status.HTTP_404_NOT_FOUND})


    

# Generating pdf


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
            #  'today': datetime.date.today(), 
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('invoice_print.html', data)
        return HttpResponse(pdf, content_type='application/pdf')



# class GeneratePDF(View):
#     def get(self, request, *args, **kwargs):
#         template = get_template('invoice_print.html')
#         context = {
#             "invoice_id": 123,
#             "customer_name": "John Cooper",
#             "amount": 1399.99,    
#             "today": "Today",
#         }
#         html = template.render(context)
#         pdf = render_to_pdf('invoice_print.html', context)
#         print("--------------")
#         if pdf:
#             response=HttpResponse(pdf, content_type='application/pdf')
            
#             filename = "Invoice_%s.pdf" %(context["customer_name"])
#             content = "inline; filename='%s'" %(filename)
#             # download = request.GET.get("download")
#             # if download:
            
#             content = "attachment; filename='%s'" %(filename)
#             response['Content-Disposition'] = content
#             print("--------------",response)
#             return HttpResponse(pdf, content_type='application/pdf')

#         return HttpResponse("Not found")

def Payments(request):
    
    
    return render(request,'payments.html',{'staff':staff})

def pendingInvoices(request):
    
    return render(request,'pendingInvoices.html')



# pending and received  invoices  module APIs
   
@api_view(['GET'])
def pendingInvoiceData(request):
       
    invoices=AllPayments.objects.filter(Q(payment_type=1) & Q(payment_status=False))

    serializedinvoices=fetchInvoicePaymentSerializer(invoices,many=True)
    
    return Response({'invoices':serializedinvoices.data})

@api_view(['GET'])  
def paymentsAutoData(request):
    
    invoiceNos=AllPayments.objects.filter(Q(payment_type=1) & Q(payment_status=False) ).values('payment_no','payment_amount')
    
    billNos=AllPayments.objects.filter(Q(payment_type=2) & Q(payment_status=False)).values('payment_no','payment_amount')
   
    staff=staffProfile.objects.all()
    serializedstaff=staffSerializer(staff,many=True)
    serializedinvoices=InvoicesAutoDataSerializer(invoiceNos,many=True)
    serializedbills=InvoicesAutoDataSerializer(billNos,many=True)
    print('invoice_nums',serializedbills.data)
    return Response({'invoice_nums':serializedinvoices.data,'bills':serializedbills.data,'staff':serializedstaff.data})
    # return Response({'invoice_nums':serializedinvoices.data,'staff':serializedstaff.data})

@api_view(['POST'])
def updatingReceivedStatus(request):
    received_paymentNo=request.data['paymentNo']
    receivedDate=request.data['date']
    received_by=request.data['staff']
    channel=request.data['channel']
    print("::::::::",channel)
    paid_obj=AllPayments.objects.filter(payment_no=received_paymentNo).update(date=receivedDate,payment_status=True,processed_by=received_by,channel=channel)
    
    return Response({"Payment Status Updated"})
def receivedInvoices(request):
    
    return render(request,'receivedInvoices.html')
@api_view(['GET'])
def receivedInvoiceData(request):
       
    invoice_obj=AllPayments.objects.filter(Q(payment_type=1) & Q(payment_status=True))
    bill_obj=AllPayments.objects.filter(Q(payment_type=2) & Q(payment_status=True))

    serialized_invoices=fetchInvoicePaymentSerializer(invoice_obj,many=True)
    serialized_bills=fetchInvoicePaymentSerializer(bill_obj,many=True)
    return Response ({'receivedInvoices':serialized_invoices.data,'paidbills':serialized_bills.data})

# pending and paid bills module APIs

def pendingBills(request):
    
    return render(request,'pendingbills.html')

   
@api_view(['GET'])
def pendingBillData(request):
       
    bills=AllPayments.objects.filter(Q(payment_type=2) & Q(payment_status=False))

    serializedbills=fetchInvoicePaymentSerializer(bills,many=True)
    
    return Response({'bills':serializedbills.data})



def paidBills(request):
    
    return render(request,'paidBills.html')

def allPayments(request):
    
    return render(request,'Allpayments.html')

@api_view(['GET'])
def allPaymentsData(request):
    
    pendingReceivable=AllPayments.objects.filter(Q(payment_type=1) & Q(payment_status=False)).aggregate(Sum('payment_amount'))
    totalreceived=AllPayments.objects.filter(Q(payment_type=1) & Q(payment_status=True)).aggregate(Sum('payment_amount'))
    pendingPayable=AllPayments.objects.filter(Q(payment_type=2) & Q(payment_status=False)).aggregate(Sum('payment_amount'))
    totalPaid=AllPayments.objects.filter(Q(payment_type=2) & Q(payment_status=True)).aggregate(Sum('payment_amount'))
    
    
    
    return Response({'totalReceived': totalreceived,'pendingReceivable': pendingReceivable,'pendingPayable': pendingPayable,'totalPaid': totalPaid})

    
    





def Income(request):
    
    return render(request,'Income.html')
# @api_view(['GET'])  
# def paymentsAutoData(request):
    
#     invoiceNos=AllPayments.objects.filter(Q(payment_type=1) & Q(payment_status=False) ).values('payment_no','payment_amount')
    
#     # billNos=AllPayments.objects.filter(payment_type=2).values('payment_no','payment_amount')
   
#     staff=staffProfile.objects.all()
#     serializedstaff=staffSerializer(staff,many=True)
#     serializedinvoices=InvoicesAutoDataSerializer(invoiceNos,many=True)
#     # serializedbills=InvoicesAutoDataSerializer(billNos,many=True)
#     print('invoice_nums',serializedinvoices.data)
#     # return Response({'invoice_nums':serializedinvoices.data,'bills':serializedbills,'staff':serializedstaff.data})
#     return Response({'invoice_nums':serializedinvoices.data,'staff':serializedstaff.data})
    
# @api_view(['POST'])
# def updatingReceivedStatus(request):
#     received_invoiceNo=request.data['invoice']
#     received_by=request.data['staff']
#     channel=request.data['channel']
#     print("::::::::",channel)
#     paid_obj=AllPayments.objects.filter(payment_no=received_invoiceNo).update(payment_status=True,processed_by=received_by,channel=channel)
    
#     return Response({"received payments are working"})
# def receivedInvoices(request):
    
#     return render(request,'receivedInvoices.html')
# @api_view(['GET'])
# def receivedInvoiceData(request):
       
#     obj=AllPayments.objects.filter(Q(payment_type=1) & Q(payment_status=True    ))
#     serialized_obj=fetchInvoicePaymentSerializer(obj,many=True)
#     return Response ({'receivedInvoices':serialized_obj.data})







