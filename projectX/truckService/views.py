from contextvars import Context
from email.policy import HTTP
from functools import partial
from heapq import merge
from http.client import HTTPResponse
from django.db.models import indexes
from django.db.models.fields import DateField
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template import context
from rest_framework import serializers
from .forms import *
from rest_framework.decorators import api_view,action
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
from projectX.settings import BASE_DIR
from .utils import role_check
from django.contrib.auth.decorators import login_required
from truckService.utils import render_to_pdf ,is_user_admin_Permission #created in step 4
import itertools

def set_if_not_none(mapping, key, value):
    if value:
        mapping[key] = value
    return mapping

@login_required
def createUser(request):
    return render(request,'createuser.html',role_check(request.user))


@login_required
def create_users(request):
    if request.method=="POST":
    
        email = request.POST['email']
        password = request.POST['password']
        
        if email and password:
        
            if User.objects.filter(Q(username=email)).exists():
                return JsonResponse({'message': False})
            else:
                
                user = User.objects.create_user(username=email,password=password)
                
                serializer=UserProfileSerializer(data={'user':user.id ,'role': request.POST['role']})
                if serializer.is_valid():
                    serializer.save()
                return JsonResponse({'message': True})
        else:
            return JsonResponse({'message': 'Please Enter the Email and Password.'}, status=status.HTTP_400_BAD_REQUEST)
    


def login_check(request):
    u=request.user
    if(u.is_authenticated):
        return render(request,'/index/',role_check(request.user))
    
    return render(request,'login.html',{'user':u})

def index(request):
    # print("UUUUU",role_check(request.user))
    u=request.user
    # allowed=False
    # dataEntry=True
    if(u.is_authenticated):
    #     role = UserProfile.objects.get(user=u).role
    #     print("------------",role)
    #     if role=="admin":
    #         allowed=True
    #     if role=="dataentry":
    #         dataEntry=False
    #     print("allowed:",allowed,dataEntry)
        return render(request,'index.html',role_check(request.user))
    
    return render(request,'login.html',{'user':u})

def login(request):
    check=False
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
    context={'check':check}
    # b=role_check(request.user)
    # print(">>>>",a)
    # print(">>>>",b)
    # context={**a, **b}
    return render(request,'login.html',context)
@login_required
def logout(request):
        auth_logout(request)
        return render(request,'login.html')


    # Trip Data Crud
@login_required
def tripdata(request):
        
        form1=tripForm()
        form2=NFTform()
        dischrge_points=DischargePiont.objects.all().values_list("locationName",flat=True)
        dischrge_points=list(dischrge_points)
        a={'form': form1,'nftForm': form2,'discharge_points':dischrge_points}
        b=role_check(request.user)
        context={**a, **b}
        return render(request,'addTripData.html',context)

@login_required
@api_view(['GET'])
def customerlocationfetch(request):
    
    val=request.GET.get("value")
    custLocation=customerProfile.objects.get(id=val)
    serCustomer=customerSerializer(custLocation)

    return Response({"customerLocation":serCustomer.data})
@login_required
@api_view(['POST'])
def addTripdata(request):
    confirm=False
    if request.method == 'POST':
    
        # d=dict(itertools.islice(d.items(),7,len(d)))
        # print("*****",d)
        # Trip_Form = tripForm(request.POST)
        # if Trip_Form.is_valid():
        #     Trip_Form.save()
        #     confirm = True
        # else:
        #     print("Errors",Trip_Form.errors)
        
        serialzer1=tripdataSerializer1(data=request.POST,partial=True)
        
        if serialzer1.is_valid():
            obj=serialzer1.save()
            print(">>>>>>>.....",obj)
            print(">>>>>>>.....",type(obj.pickupPoint))
            serilized_data=serialzer1.data
            confirm = True

        trip_obj=tripData.objects.get(id=serilized_data["id"])
        d=dict(request.data)
        
        length=(len(d)-6)//2
        discharge_cost=0
        discharge_vat=0
        for i in range(length):
            a=d["order_now"+str(i)]
            b=d["discharge_points"+str(i)]
            
            s=b[0][1]
            discharges=DischargePiont.objects.all()
            
            
            if s=='S':
                cost=discharges[0].Cost
                vat=discharges[0].Vat
              
                
                calculated_vat=(cost*vat)/100
                
                discharge_cost=discharge_cost+(cost+calculated_vat)
                
                discharge_vat=discharge_vat+calculated_vat
                
            elif s=='J':
                 cost=discharges[1].Cost
                 vat=discharges[1].Vat
                 calculated_vat=(cost*vat)/100
                 discharge_cost=discharge_cost+(cost+calculated_vat)
                 discharge_vat=discharge_vat+calculated_vat
                 
            elif s=='N':
                 cost=discharges[2].Cost
                 vat=discharges[2].Vat
                 calculated_vat=(cost*vat)/100
                 discharge_cost=discharge_cost+(cost+calculated_vat)
                 discharge_vat=discharge_vat+calculated_vat
                 
            elif s=='A':
                 cost=discharges[3].Cost
                 vat=discharges[3].Vat
                 calculated_vat=(cost*vat)/100
                 discharge_cost=discharge_cost+(cost+calculated_vat)
                 discharge_vat=discharge_vat+calculated_vat
                 
            elif s=='M':
                 
                 cost=discharges[4].Cost
                 vat=discharges[4].Vat
                 calculated_vat=(cost*vat)/100
                 discharge_cost=discharge_cost+(cost+calculated_vat)
                 discharge_vat=discharge_vat+calculated_vat
                 
            elif s=='O':
                 cost=discharges[5].Cost
                 vat=discharges[5].Vat
                 calculated_vat=(cost*vat)/100
                 discharge_cost=discharge_cost+(cost+calculated_vat)
                 discharge_vat=discharge_vat+calculated_vat
                 
            
            data={'order_no':a[0],'discharge_point':b[0]}
            data.update({'trip':trip_obj.id})
            serializer2=NFTSerializer(data=data,partial=True)
            if serializer2.is_valid():
                serializer2.save()
        
        trip_obj.discharge_vat=discharge_vat
        trip_obj.discharge_cost=discharge_cost
        trip_obj.total_discharge_cost=discharge_cost
        
        trip_obj.save()
        
    return Response({'confirm':confirm,'length':length}) 
@login_required
def manageTripdata(request):

    return render(request,'manageTripData.html',role_check(request.user))

@login_required
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



@login_required
@api_view(['GET','POST'])
def nftlistshow(request):
    if request.method == 'POST':
        
        trip= tripData.objects.get(id=request.POST.get('id'))
        # points=tripData.objects.all()
        print(trip,"/////////////////")
        serialzer=nftTripDataSerialzer(trip)
        print(">>>>>>>>>>>>s",serialzer.data)
        return Response({'tripdata':serialzer.data})
    
    

 

@login_required
@api_view(['POST'])
def updateTripdata(request,pk):
    # new_obj =  User.objects.filter(id=pk).first()
    new_obj2 =  tripData.objects.get(id=pk)
    
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

@login_required
@api_view(['GET'])
def deleteTripdata(request):
   user_id = request.GET.get('id')
   tripData.objects.get(id=user_id).delete()
   
   return Response({'confirm':True})





#   Customer CRUD APIS
@login_required
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
    a={'cform':cform,'form1':form1,'confirm':confirm}
    b=role_check(request.user)
    context={**a, **b}
    return render(request,'customer.html',context)



@login_required
@api_view(['GET', 'POST'])
def createCustomer(request):
    confirm=False
    email="----"
    contact_person="----"
    estate_name="----"
    if request.method=='POST':
        print(request.POST)
        user_form = userForm(request.POST)
        customer_form = customer(request.POST)
        post=request.POST
        if post['managing_by']=='Real_Estate':
            email=request.data.get('email')
            contact_person=request.data.get("contact_person")
            estate_name=request.data.get("estate_name")
        if user_form.is_valid() and customer_form.is_valid():
            obj2 = user_form.save(commit=False)
            obj=customer_form.save(commit=False) 
            
            uname=obj2.first_name+obj2.last_name+str(random.randint(0,1000))
            obj2.username=uname
            obj2.save()
            obj.user=obj2
            obj.type=Role.objects.get(id=1)
        
            obj.estate_name=estate_name
            obj.contact_person=contact_person
            obj.email=email
            obj.save()
            confirm = True

                
            
                
                
            
    return Response({'confirm':confirm})    

@login_required
def customerList(request):

    return render(request,'customerslist.html',role_check(request.user))


# def customerList(request):
#     customers=User.objects.all().exclude(username=request.user.username)
    
#     if request.method == 'POST':
#         customerUser = User.objects.get(id=request.POST.get('id'))
#         profile=userProfile.objects.get(user=customerUser)
#         serializer=UserSerializer(customerUser)
#         serializer1=profileSerializer(profile)
#         return JsonResponse({'specificCustomer': serializer.data,'customerdata': serializer1.data})
#     return render(request,'customerslist.html',{'customers':customers})

@login_required
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

@login_required
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
@api_view(['GET', 'POST'])
@login_required
def deleteCustomer(request):
   user_id = request.GET.get('id')
   User.objects.get(id=user_id).delete()
   return Response({'confirm':True})



#    DischargePiont CRUD APIS

@login_required
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

@login_required
def createDischarge(request):
    
    dischargeForm1=dischargeForm()
    a={'dform':dischargeForm}
    b=role_check(request.user)
    context={**a,**b}
    return render(request,'addDischargepoint.html',context)

@login_required
def addDischarge(request):
    confirm=False
    if request.method == 'POST':
        user_form = dischargeForm(request.POST)
        
        if user_form.is_valid():
            user_form.save()
            confirm = True

    return JsonResponse({'confirm':confirm})  


@login_required
def dischargepointList(request):

    return render(request,'manageDischargepoint.html',role_check(request.user))


@login_required
def updatedischargepoint(request,pk):
    # new_obj =  User.objects.filter(id=pk).first()
    new_obj2 =  DischargePiont.objects.get(id=pk)
    
    updatecheck = False
    if request.method == 'POST':
        
        dischargePoints = dischargeSerializer(new_obj2, data=request.POST, partial=True)
        # print("sssssssssssssssssssssssssssssssssssssss",dischargePoints.data)
        if dischargePoints.is_valid():
            print("sssssssssssssssssssssssssssssssssssssss",dischargePoints.validated_data)
            
            dischargePoints.save()
            updatecheck=True
    return JsonResponse({'updatecheck':updatecheck})

@login_required
@api_view(['GET'])
def deleteDischargepoint(request):
   user_id = request.GET.get('id')
   DischargePiont.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})


@login_required
def creatededuction(request):
    
    dischargeForm1=deductionForm()
    a={'dform':dischargeForm1}
    b=role_check(request.user)
    context={**a,**b}
    return render(request,'deduction.html',context)

@login_required
def addDeduction(request):
    confirm=False
    if request.method == 'POST':
        data=request.POST
        user_form = deductionForm(request.POST)
        
        if user_form.is_valid():
            model_instance = user_form.save()
            confirm = True
        staff_obj=staffProfile.objects.get(id=int(data['staff'])) 
        total_amount=deduction.objects.filter(staff=staff_obj).aggregate(Sum('amount'))
        
        model_instance.total_fine=total_amount['amount__sum']
        model_instance.save()
        # deduction.objects.filter(staff=staff_obj).update(total_fine=total_amount['amount__sum'])
        fine=int(data['amount'])
        
        obj=remaining_deduction.objects.filter(staff=staff_obj).first()
        if obj:
            remaining=obj.total_payable
            remaining=remaining+fine
            obj.total_payable=remaining
            obj.save()
        else:
            obj2=remaining_deduction.objects.create(staff=staff_obj,total_payable=fine)
            obj2.save()
    return JsonResponse({'confirm':confirm})  


@login_required
def managededuction(request):

    return render(request,'manageDeduction.html',role_check(request.user))

@login_required
def deductionlistshow(request):

    if request.method == 'POST':
        editPoint= deduction.objects.get(id=request.POST.get('id'))
        # print("*********************",request.POST.get('id'))
        # profile=userProfile.objects.get(user=customerUser)
        # serializer=UserSerializer(customerUser)
        serializer1=deductionSerializer(editPoint)
        tripDriver=staffProfile.objects.all()
        tripDriver_serializer=staffSerializer(tripDriver,many=True)
         
        
        # print("rrrrrrrrrrrrrrrrrrrrrrrrr",serializer1.data)
        return JsonResponse({'dischargePoints': serializer1.data,'tripdirver':tripDriver_serializer.data})
    
    
    # customerUserDetail=User.objects.all().exclude(username=request.user.username)
    points=deduction.objects.all().order_by('staff')
    remainings=remaining_deduction.objects.all().order_by('staff')
    # serializedUser=UserSerializer(customerUserDetail,many=True)
    # locations=Location.objects.all()
    # location_serializer=locationSerializer(locations,many=True)
    serializedDischarge=fetchdeductionSerializer(points,many=True)
    serializedremaining=fetchRemainingSerializer(remainings,many=True)
    return JsonResponse({'dischargePoints':serializedDischarge.data,'remainings':serializedremaining.data})

@login_required
def updateDeduction(request,pk):
    # new_obj =  User.objects.filter(id=pk).first()
    new_obj2 =  deduction.objects.get(id=pk)
    print(">><<<<<<<<<<<<<<<<<<<",new_obj2)
    updatecheck = False
    if request.method == 'POST':
        
        dischargePoints = deductionSerializer(new_obj2, data=request.POST, partial=True)
        # print("sssssssssssssssssssssssssssssssssssssss",dischargePoints.data)
        if dischargePoints.is_valid():            
            dischargePoints.save()
            updatecheck=True
    return JsonResponse({'updatecheck':updatecheck})

@login_required
@api_view(['GET'])
def deletededuction(request):
   user_id = request.GET.get('id')
   deduction.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})



# Trucks CRUD
@login_required
def createTrucks(request):
    
    tform=truckForm()
    a={'tform':tform}
    b=role_check(request.user)
    context={**a,**b}
    return render(request,'addTrucks.html',context)

@login_required
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
@login_required
def managetrucks(request):

    return render(request,'managetrucks.html',role_check(request.user))

@login_required
@api_view(['GET', 'POST'])
def trucklistshow(request):
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

@login_required
@api_view(['GET', 'POST'])
def updateTruck(request,truckno):
    
    # new_obj =  User.objects.filter(id=pk).first()
    new_obj2 = Trucks.objects.get(truckNumber=truckno)
    
    updatecheck = False
    if request.method == 'POST':
       
        trucksSer = trucksSerializer(new_obj2, data=request.POST, partial=True)
        
        if trucksSer.is_valid():
            
            trucksSer.save()
            updatecheck=True
    return Response({'updatecheck':updatecheck})

@login_required
@api_view(['GET', 'POST'])    
def deleteTruck(request):
   user_id = request.GET.get('id')
   Trucks.objects.get(truckNumber=user_id).delete()
   
  
   return Response({'confirm':True})


@login_required
def manageFuelData(request):

    return render(request,'fuelData.html',role_check(request.user))

   
@login_required
@api_view(['GET'])
def FuelDataShow(request):
#   This code will wakeup when i will update
    #     editTruck= Trucks.objects.get(truckNumber=request.POST.get('id'))
    #     serializer1=trucksSerializer(editTruck)
    #     return JsonResponse({'trucks': serializer1.data})
    
    fuel=truckFuel.objects.all()
    serializedFuel=truckFuelSerializer(fuel,many=True)
    return Response({'fuel':serializedFuel.data})






#   Staff CRUD APIS
@login_required
def createStaff(request):
    
    confirm=False

    form1=userForm()
    sform=staff()
    a={'sform':sform,'form1':form1,'confirm':confirm}
    b=role_check(request.user)
    context={**a,**b}
    return render(request,'createstaff.html',context)


@login_required
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

@login_required
def staffList(request):

    return render(request,'managestaff.html',role_check(request.user))

@login_required
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

@login_required
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
  

@login_required
def deleteStaff(request):
   user_id = request.GET.get('id')
   User.objects.get(id=user_id).delete()
   
  
   return HttpResponse({'confirm':True})


    # Expnses Cruds
    # create view
@login_required
def Expenses(request):
    
    sform=staffexForm()
    tform=truckexForm()
    oform=officeexForm()
    otherform=otherexForm()
    billxForm=billForm()
    a={'sform':sform,'tform':tform,'oform':oform,'otherform':otherform,'billxForm':billxForm}
    b=role_check(request.user)
    context={**a,**b}
    return render(request,'Expenses.html',context)
    

@login_required
@api_view(['GET', 'POST'])
def addExpenses(request):
    confirm=False
    deduct_status=False
    bill_no=100000000
    print("ssssss")

    no = ''.join(str(random.randint(0,10)) for x in range(5))
    bill_number=bill_no+int(no)
    if request.method == 'POST':
        exchange="----"
        by_hand="----"
        data=request.POST
        value_at_index=False
        
        length=list(data.values())
        length=len(length)
        if length>14:
            value_at_index = list(data.values())[14]
            if  value_at_index=="Both":
                exchange=request.POST.get("exchange")
                by_hand=request.POST.get("by_hand")
        staffForm = staffexForm(request.POST)
        truckForm = truckexForm(request.POST)
        officeForm = officeexForm(request.POST)
        otherForm = otherexForm(request.POST)
        truckfuellForm=truckfuelForm(request.POST)
        # billxForm = billForm(request.POST)
        if staffForm.is_valid():
            obj=staffForm.save()
            deduct=obj.deduction

            staff_obj=obj.staff 
            objx=remaining_deduction.objects.filter(staff=staff_obj).first()
            if objx:
                remaining=objx.total_payable
                remaining=remaining-deduct
                objx.total_payable=remaining
                objx.deduct=objx.deduct+deduct
                objx.save()
            else:
                deduct_status=True


            obj.totalAmount=obj.remaining_salary+obj.visaFee+obj.eidFee+obj.medicalIns+obj.overTime+obj.others+obj.vat
            obj.save()
            obj.exchange=exchange
            obj.by_hand=by_hand
            obj.save()
            # payments=InvoicePaymentSerializer(data={"date":date.today(),"user":1,"vendor":"-----","payment_no":bill_number,payment_type,"payment_type":2,"expense_type":"Staff Expense","payment_amount":obj.totalAmount,"payment_status":False},partial=True)
            # if payments.is_valid():
            #     payments.save()
            payments=incomeExpenseSerializer(data={"date":date.today(),"payment_no":bill_number,"payment_type":2,"payment_amount":obj.totalAmount,"payment_status":True,"user":1},partial=True)
            if payments.is_valid():
                payments.save()
            confirm = True
            
        elif truckfuellForm.is_valid():
            obj5=truckfuellForm.save()
            obj5.save()
            if truckForm.is_valid():
                obj1=truckForm.save()
                obj1.totalAmount=obj1.renewalFee+obj1.fuel+obj1.maintenance+obj1.repair_replace+obj1.parking+obj1.others+obj1.vat
                obj1.save()
                payments=incomeExpenseSerializer(data={"date":date.today(),"payment_no":bill_number,"payment_type":2,"payment_amount":obj1.totalAmount,"payment_status":True,"user":1},partial=True)
                if payments.is_valid():
                    payments.save()
                confirm = True
        elif officeForm.is_valid():
            obj2=officeForm.save()
            obj2.totalAmount=obj2.officeRent+obj2.utilityBills+obj2.stationary+obj2.kitchen+obj2.others+obj2.vat
            obj2.save()
            payments=incomeExpenseSerializer(data={"date":date.today(),"payment_no":bill_number,"payment_type":2,"payment_amount":obj2.totalAmount,"payment_status":True,"user":1},partial=True)
            if payments.is_valid():
                payments.save()
            confirm = True
        elif otherForm.is_valid():
            obj3=otherForm.save()
            obj3.totalAmount=obj3.expenseAmount+obj3.vat
            obj3.save()
            payments=incomeExpenseSerializer(data={"date":date.today(),"payment_no":bill_number,"payment_type":2,"payment_amount":obj3.totalAmount,"payment_status":True,"user":1},partial=True)
            if payments.is_valid():
                payments.save()
            confirm = True
        # elif billxForm.is_valid():
        #     obj4=billxForm.save()
        #     obj4.totalAmount=obj4.amount+obj4.vat
        #     obj4.save()
            # payments=InvoicePaymentSerializer(data={"date":date.today(),"user":1,"vendor":obj4.vendor,"payment_no":bill_number,"payment_type":2,"expense_type":obj3.expenseName+" Expense","payment_amount":obj3.totalAmount,"payment_status":False},partial=True)
            # if payments.is_valid():
                # payments.save()
            # confirm = True
       
    return Response({'confirm':confirm,"deduction_check":deduct_status}) 

    # Manage Staff Expenses View 
@login_required
def manageStaffExpense(request):

    return render(request,'manageStaffExpense.html',role_check(request.user))

@login_required
@api_view(['GET', 'POST'])
def staffExpenseListshow(request):
    if request.method == 'POST':
        staffex= staffExpense.objects.get(id=request.POST.get('id'))
        serializer1=fetchstaffexSerializer(staffex)
        
        tripDriver=staffProfile.objects.all()
        tripDriver_serializer=staffSerializer(tripDriver,many=True)
        # print("rrrrrrrrrrrrrrrrrrrrrrrrr",serializer1.data)
        return Response({'staffexpenses': serializer1.data,'staffNames':tripDriver_serializer.data})
    
    staffexpenses=staffExpense.objects.all()
    
    # code to deduct will go here

    serializedDischarge=fetchstaffexSerializer(staffexpenses,many=True)
    
    return Response({'staffexpenses':serializedDischarge.data})


@login_required
@api_view(['GET', 'POST'])
def updateStaffExpense(request,pk):
    
    # new_obj =  User.objects.filter(id=pk).first()
    new_obj2 = staffExpense.objects.get(id=pk)
    
    updatecheck = False
    if request.method == 'POST':
       
        staffexserials = staffexSerializer(new_obj2, data=request.POST, partial=True)
   
        if staffexserials.is_valid():

            staffobj=staffexserials.save()
            staffobj.totalAmount=staffobj.totalAmount=staffobj.remaining_salary+staffobj.visaFee+staffobj.eidFee+staffobj.medicalIns+staffobj.overTime+staffobj.others+staffobj.vat
            staffobj.save()
            updatecheck=True
        else:
            print("Error : ",staffexserials.errors)
            
    return Response({'updatecheck':updatecheck})

@login_required
@api_view(['GET', 'POST'])    
def deleteStaffExpense(request):
   user_id = request.GET.get('id')
   print("-----s------------",user_id)
   staffExpense.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})


# Manage Staff Expenses View 
def manageTruckExpense(request):

    return render(request,'manageTruckExpense.html',role_check(request.user))


@login_required
@api_view(['GET', 'POST'])
def truckExpenseListshow(request):
    if request.method == 'POST':

        tripDriver=staffProfile.objects.all()
        tripDriver_serializer=staffSerializer(tripDriver,many=True)

        staffex= truckExpense.objects.get(id=request.POST.get('id'))
        serializer1=fetchtruckexSerializer(staffex)
    
        truckex=Trucks.objects.all()
        truckex_serializer=trucksSerializer(truckex,many=True)
        
        return Response({'staffNames':tripDriver_serializer.data,'trucksexpense': serializer1.data,'truckNumbers':truckex_serializer.data})
   
    truckexpenses=truckExpense.objects.all()
    
    serializedtruckex=fetchtruckexSerializer(truckexpenses,many=True)
    
    return Response({'trucksexpense':serializedtruckex.data})

@login_required
@api_view(['GET', 'POST'])
def updateTruckExpense(request,pk):
    
    # new_obj =  User.objects.filter(id=pk).first()
    new_obj2 = truckExpense.objects.get(id=pk)
    
    updatecheck = False
    if request.method == 'POST':
        
        officeexserials = truckexSerializer(new_obj2, data=request.POST, partial=True)
        
        if officeexserials.is_valid():
            
            truckobj=officeexserials.save()
            truckobj.totalAmount=truckobj.renewalFee+truckobj.fuel+truckobj.maintenance+truckobj.repair_replace+truckobj.parking+truckobj.others+truckobj.vat
            truckobj.save()
            updatecheck=True
    return Response({'updatecheck':updatecheck})

@login_required
@api_view(['GET', 'POST'])    
def deleteTruckExpense(request):
   user_id = request.GET.get('id')
   print("-----s------------",user_id)
   truckExpense.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})



# Manage Staff Expenses View 
@login_required
def manageOfficeExpense(request):

    return render(request,'manageOfficeExpense.html',role_check(request.user))

@login_required
@api_view(['GET', 'POST'])
def officeExpenseListshow(request):
     if request.method == 'POST':
        tripDriver=staffProfile.objects.all()
        tripDriver_serializer=staffSerializer(tripDriver,many=True)

        officeex= officeExpense.objects.get(id=request.POST.get('id'))
        serializer1=fetchofficeexSerializer(officeex)
        return Response({'staffNames':tripDriver_serializer.data,'officesexpense': serializer1.data})

     truckexpenses=officeExpense.objects.all()
     serializedofficeex=fetchofficeexSerializer(truckexpenses,many=True)
     return Response({'officesexpense':serializedofficeex.data})


@login_required
@api_view(['GET', 'POST'])
def updateOfficeExpense(request,pk):
    
    new_obj2 = officeExpense.objects.get(id=pk)
    
    updatecheck = False
    if request.method == 'POST':
        
        officeexserials = officeexSerializer(new_obj2, data=request.POST, partial=True)
        
        if officeexserials.is_valid():
            
            officeobj=officeexserials.save()
            officeobj.totalAmount=officeobj.officeRent+officeobj.utilityBills+officeobj.stationary+officeobj.kitchen+officeobj.others+officeobj.vat
            officeobj.save()
            updatecheck=True
    return Response({'updatecheck':updatecheck})


@login_required
@api_view(['GET', 'POST'])    
def deleteOfficeExpense(request):
   user_id = request.GET.get('id')

   officeExpense.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})


# Manage Staff Expenses View
@login_required 
def manageOtherExpense(request):

    return render(request,'manageOtherExpense.html',role_check(request.user))

@login_required
@api_view(['GET', 'POST'])
def otherExpenseListshow(request):
    if request.method == 'POST':
        tripDriver=staffProfile.objects.all()
        tripDriver_serializer=staffSerializer(tripDriver,many=True)

        officeex= otherExpense.objects.get(id=request.POST.get('id'))
        
        serializer1=fetchotherexSerializer(officeex)
      
        return Response({'staffNames':tripDriver_serializer.data,'otherexpense': serializer1.data})
    otherexpenses=otherExpense.objects.all()
   
    serializedotherex=fetchotherexSerializer(otherexpenses,many=True)
    
    return Response({'otherexpense':serializedotherex.data})


@login_required
@api_view(['GET', 'POST'])
def updateOtherExpense(request,pk):
   new_obj2 = otherExpense.objects.get(id=pk)
    
   updatecheck = False
   if request.method == 'POST':
        
        otherexserials = otherexSerializer(new_obj2, data=request.POST, partial=True)
        
        if otherexserials.is_valid():
            
            othereobj=otherexserials.save()
            othereobj.totalAmount=othereobj.expenseAmount+othereobj.vat  
            othereobj.save()
            updatecheck=True
   return Response({'updatecheck':updatecheck})


@login_required
@api_view(['GET', 'POST'])    
def deleteOtherExpense(request):
   user_id = request.GET.get('id')
   print("-----s------------",user_id)
   otherExpense.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})



# Manage Staff Expenses View
@login_required 
def manageTotalExpense(request):

    return render(request,'manageTotalExpense.html',role_check(request.user))

@login_required
@api_view(['GET', 'POST'])
def totalExpenseListshow(request):
   
    totalStaffExpense=staffExpense.objects.aggregate(Sum('totalAmount'))
    totalOfficeExpense=officeExpense.objects.aggregate(Sum('totalAmount'))
    totalOtherExpense=otherExpense.objects.aggregate(Sum('totalAmount'))
    totalTruckExpense=truckExpense.objects.aggregate(Sum('totalAmount'))
    # totalBillExpense=billExpense.objects.aggregate(Sum('totalAmount'))
    totaldischargeExpense=tripData.objects.aggregate(Sum('total_discharge_cost'))
    totalExpense=totalStaffExpense["totalAmount__sum"]+totalOfficeExpense["totalAmount__sum"]+totalOtherExpense["totalAmount__sum"]+totalTruckExpense["totalAmount__sum"]+totaldischargeExpense["total_discharge_cost__sum"]
    
    return Response({'staffexpense':totalStaffExpense,'officeexpense':totalOfficeExpense,'otherexpense':totalOtherExpense,'truckexpense':totalTruckExpense,'dischargeexpense':totaldischargeExpense,'totalExpense':totalExpense})


# Manage Bill Expenses View
@login_required 
def manageBillExpense(request):

    return render(request,'billExpense.html',role_check(request.user))

@login_required
@api_view(['GET', 'POST'])
def billExpenseListshow(request):
    if request.method == 'POST':
        
        officeex= billExpense.objects.get(id=request.POST.get('id'))
        
        serializer1=billSerializer(officeex)
        print("ffff",serializer1.data)
        return Response({'billexpense': serializer1.data})
    otherexpenses=billExpense.objects.all()
   
    serializedotherex=billSerializer(otherexpenses,many=True)
    print("ffff",serializedotherex.data)
    return Response({'billexpense':serializedotherex.data})


@login_required
@api_view(['GET', 'POST'])
def updateBillExpense(request,pk):
   new_obj2 = billExpense.objects.get(id=pk)
    
   updatecheck = False
   if request.method == 'POST':
        
        otherexserials = billSerializer(new_obj2, data=request.POST, partial=True)
        
        if otherexserials.is_valid():
            
            othereobj=otherexserials.save()
            othereobj.totalAmount=othereobj.amount+othereobj.vat  
            othereobj.save()
            updatecheck=True
   return Response({'updatecheck':updatecheck})


@login_required
@api_view(['GET', 'POST'])    
def deleteBillExpense(request):
   user_id = request.GET.get('id')
   print("-----s------------",user_id)
   billExpense.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})





# Generate Invoice
@login_required
def generateInvoice(request):
    form=customerField()
    a={'form':form}
    b=role_check(request.user)
    context={**a,**b}
    return render(request,'generateInvoice.html',context)

   # Generate Invoice
@login_required
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
        a={**returned_list}
        print(":::",a)
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
invoice_no=0000


@login_required
def Invoice(request):
    global invoice_no
    invoice_no=invoice_no+1
    
    if request.method=='POST':
        
        customer=customerProfile.objects.get(id=request.POST["customer"])
        from_date = request.POST["fromDate"]
        to_date = request.POST["toDate"]
        csrf = request.POST["csrfmiddlewaretoken"]

        a={
            'fromDate':request.POST["fromDate"],
            'toDate' : request.POST["toDate"],
             'customer' :  customer,
             'contactNo' :  customer.contact,
             'location' :  customer.location,
              'date'  :  date.today(),
              'csrf':csrf,
              'invoiceNo':invoice_no,
              'record_no':customer.record_number,
              'rate':customer.tripCharges,
        }
        
        b=role_check(request.user)
        context={**a,**b}
        
        return render(request,'invoice.html',context)

@login_required
def printInvoice(request):
    
    return render(request,'invoice_print.html',role_check(request.user))

@login_required
@api_view(['POST'])
def saveinvoice(request):
    
    if request.method=="POST":
        customer=customerProfile.objects.get(id=request.POST["customer"])
        invoice_number=request.POST["payment_no"]
        tripsAmount=request.POST["tripsAmount"]
        payment_amount=int(request.POST["payment_amount"])
        tax=int(request.POST["tax"])
        # payment type '1' means Invoice
        payments=InvoicePaymentSerializer(data={"date":date.today(),"user":customer.user.id,"payment_no":invoice_number,"payment_type":1,"payment_amount":payment_amount,"payment_status":False,"tax":tax,"tripsAmount":tripsAmount},partial=True)
        if payments.is_valid():
            payments.save()
        return Response(status.HTTP_200_OK)
    return Response({status.HTTP_404_NOT_FOUND})


    

# Generating pdf

# 
class GeneratePdf(View):
    @login_required
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

@login_required
def Payments(request):
    
    a={'staff':staff}
    b=role_check(request.user)
    context={**a,**b}
    return render(request,'payments.html',context)

@login_required
def pendingInvoices(request):
    
    return render(request,'pendingInvoices.html',role_check(request.user))



# pending and received  invoices  module APIs
   
@login_required
@api_view(['GET'])
def pendingInvoiceData(request):
       
    invoices=AllPayments.objects.filter(Q(payment_type=1) & Q(payment_status=False))

    serializedinvoices=fetchInvoicePaymentSerializer(invoices,many=True)
    
    return Response({'invoices':serializedinvoices.data})

@login_required
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


@login_required
@api_view(['POST'])
def updatingReceivedStatus(request):
    received_paymentNo=request.data['paymentNo']
    receivedDate=request.data['date']
    received_by=request.data['staff']
    channel=request.data['channel']
    
    paid_obj=AllPayments.objects.filter(payment_no=received_paymentNo).update(date=receivedDate,payment_status=True,processed_by=received_by,channel=channel)
    
    return Response({"Payment Status Updated"})

@login_required
def receivedInvoices(request):
    
    return render(request,'receivedInvoices.html',role_check(request.user))

@login_required
@api_view(['GET'])
def receivedInvoiceData(request):
       
    invoice_obj=AllPayments.objects.filter(Q(payment_type=1) & Q(payment_status=True))
    bill_obj=AllPayments.objects.filter(Q(payment_type=2) & Q(payment_status=True))

    serialized_invoices=fetchInvoicePaymentSerializer(invoice_obj,many=True)
    serialized_bills=fetchInvoicePaymentSerializer(bill_obj,many=True)
    return Response ({'receivedInvoices':serialized_invoices.data,'paidbills':serialized_bills.data})

# pending and paid bills module APIs

@login_required
def pendingBills(request):
    
    return render(request,'pendingbills.html',role_check(request.user))


@login_required
@api_view(['GET'])
def pendingBillData(request):
       
    bills=AllPayments.objects.filter(Q(payment_type=2) & Q(payment_status=False))

    serializedbills=fetchInvoicePaymentSerializer(bills,many=True)
    
    return Response({'bills':serializedbills.data})


@login_required
def paidBills(request):
    
    return render(request,'paidBills.html',role_check(request.user))


@login_required
def allPayments(request):
    
    return render(request,'Allpayments.html',role_check(request.user))


@login_required
@api_view(['GET'])
def allPaymentsData(request):
    
    pendingReceivable=AllPayments.objects.filter(Q(payment_type=1) & Q(payment_status=False)).aggregate(Sum('payment_amount'))
    totalreceived=AllPayments.objects.filter(Q(payment_type=1) & Q(payment_status=True)).aggregate(Sum('payment_amount'))
    pendingPayable=AllPayments.objects.filter(Q(payment_type=2) & Q(payment_status=False)).aggregate(Sum('payment_amount'))
    totalPaid=AllPayments.objects.filter(Q(payment_type=2) & Q(payment_status=True)).aggregate(Sum('payment_amount'))
    totaldischargeExpense=tripData.objects.aggregate(Sum('total_discharge_cost'))
    
    totalPaid=totalPaid["payment_amount__sum"]+totaldischargeExpense['total_discharge_cost__sum']
    return Response({'totalReceived': totalreceived,'pendingReceivable': pendingReceivable,'pendingPayable': pendingPayable,'totalPaid': totalPaid})

@login_required
def Income(request):
    return render(request,'Income.html',role_check(request.user))



# Trip Data Crud
@login_required
def attendance(request):
    form=attendanceForm()
    a={'form': form}
    b=role_check(request.user)
    context={**a,**b}
    return render(request,'attendance.html',context)

@login_required
@api_view(['POST'])
def addAttendance(request):
    confirm=False
    if request.method == 'POST':
        attendance_Form = attendanceForm(request.POST)
        if attendance_Form.is_valid():
            attendance_Form.save()
            confirm = True
        else:
            print("hhhhhh",attendance_Form.errors)
    return Response({'confirm':confirm}) 

@login_required
def manageAttendance(request):
    return render(request,'manageAttendance.html',role_check(request.user))

@login_required
@api_view(['GET','POST'])
def attendanceListshow(request):

    if request.method == 'POST':
        attendance= Attendance.objects.get(id=request.POST.get('id'))
        serializer1=fetchAttendanceSerializer(attendance)
        staff=staffProfile.objects.all()
        staff_serializer=staffSerializer(staff,many=True)
        return Response({'attendance': serializer1.data,'staff':staff_serializer.data })
    attendances=Attendance.objects.all()
    serialized=fetchAttendanceSerializer(attendances,many=True)
    print(">>>>>>>",serialized.data)
    return Response({'attendance':serialized.data})


@login_required
@api_view(['POST'])
def updateAttendace(request,pk):
    new_obj2 =  Attendance.objects.get(id=pk)
    updatecheck = False
    employee_id=request.POST['employee']
    cutomer_obj=staffProfile.objects.get(id=employee_id)
    if request.method == 'POST':
        attendance_Data = AttendanceSerializer(new_obj2, data=request.POST, partial=True)
        if attendance_Data.is_valid():
            attendance_Data.save()
            updatecheck=True
    return Response({'updatecheck':updatecheck})


@login_required
@api_view(['GET'])
def deleteAttendance(request):
   user_id = request.GET.get('id')
   Attendance.objects.get(id=user_id).delete()
   
  
   return Response({'confirm':True})



# Trip Data Crud
@login_required
def leaves(request):
    form=leavesForm()
    a={'form': form}
    b=role_check(request.user)
    context={**a,**b}
    return render(request,'leaves.html',context)

@login_required
@api_view(['GET'])
def joiningDatefetch(request):
    val=request.GET.get("value")
    joiningDate=list(staffProfile.objects.filter(id=val).values('joiningDate'))
    # serCustomer=customerSerializer(custLocation)
    joiningDate=joiningDate[0]["joiningDate"]
    return Response({"joiningDate":joiningDate}) 


@login_required
@api_view(['POST'])
def addLeaves(request):
    confirm=False
    if request.method == 'POST':
        leaves_Form = leavesForm(request.POST)
        if leaves_Form.is_valid():
            leaves_Form.save()
            confirm = True
        else:
            print("hhhhhh",leaves_Form.errors)
    return Response({'confirm':True}) 


@login_required
def manageLeaves(request):
    return render(request,'manageLeaves.html',role_check(request.user))


@login_required
@api_view(['GET','POST'])
def leavesListshow(request):

    if request.method == 'POST':
        leaves= Leaves.objects.get(id=request.POST.get('id'))
        serializer1=fetchLeavesSerializer(leaves)
        staff=staffProfile.objects.all()
        staff_serializer=staffSerializer(staff,many=True)
        return Response({'leaves': serializer1.data,'staff':staff_serializer.data })
    leaves=Leaves.objects.all()
    serialized=fetchLeavesSerializer(leaves,many=True)
    
    return Response({'leaves':serialized.data})


@login_required
@api_view(['POST'])
def updateLeaves(request,pk):
    new_obj2 =  Leaves.objects.get(id=pk)
    updatecheck = False
    
    if request.method == 'POST':
        leaves_Data = LeavesSerializer(new_obj2, data=request.POST, partial=True)
        if leaves_Data.is_valid():
            leaves_Data.save()
            updatecheck=True
    return Response({'updatecheck':updatecheck})



@login_required
@api_view(['GET'])
def deleteLeaves(request):
   user_id = request.GET.get('id')
   Leaves.objects.get(id=user_id).delete()
   return Response({'confirm':True})


# Generate Reports
@login_required
def generateReport(request,id):
    check=False
    form=emptyForm()
    if id==1:
        check=True
    if id==2:
        form=truckField()
    if id==3:
        form=customerField()
    if id==4:
        form=truckField()
    if id==5:
        pass
    if id==6:
        pass 
    if id==7:
        pass 
    if id==8:
        form=truckField()
    if id==9:
        form=truckField()
    a={'form': form}
    print(id,".........")
    b=role_check(request.user)
    c={'check':check,'id':id}
    context={**a,**b,**c}
    return render(request,'generateReport.html',context)



report_number=1000000000

@login_required
def Report(request):
    no = ''.join(str(random.randint(10,20)) for x in range(5))
    report_number=invoice_no+int(no)
    
    if request.method=='POST':
        id=request.POST["reportId"]
        choice=None
        customer=request.POST.get("customer")
        truck=request.POST.get("TruckNo")
        if customer:
            choice=customer
        if truck:
            choice=truck
        # print("HHH",truck)
        # customer=customerProfile.objects.get(id=request.POST["customer"])
        from_date = request.POST["fromDate"]
        to_date = request.POST["toDate"]
        csrf = request.POST["csrfmiddlewaretoken"]

        context={
            'category':request.POST.get("category"),
            'fromDate':request.POST["fromDate"],
            'toDate' : request.POST["toDate"],
             'choice' :  choice,
             'id' :  id,
              'date'  :  date.today(),
              'csrf'  :  csrf,
              'reportNo':report_number,
              'record_no':invoice_no-99990,
        }
        print(">dddddd>>>>",id)
        b=role_check(request.user)
        context={**context,**b}
        
        return render(request,'report.html',context)

#    Generate Invoice
@login_required
@api_view(['POST'])
def createReport(request):
    
    if request.method=="POST":
        list={}
       
        from_date = request.POST.get("fromDate")
        to_date = request.POST.get("toDate")
        category = request.POST.get("category")
        choice = request.POST.get("choice")
        reportId = request.POST.get("reportId")
        # customer = request.POST.get("customer")
        
        # if from_date and to_date:
        #     fromdate=datetime.strptime(from_date , '%Y-%m-%d')
        #     todate =datetime.strptime(to_date , '%Y-%m-%d')
        
        set_if_not_none(list,'date__gte',from_date)
        returned=set_if_not_none(list,'date__lte',to_date)
        
        # returned_list=set_if_not_none(list,'customer',customer)
        report_serializer=""
        report_serializer_1=None
        report_serializer_2=None
        report_serializer_3=None
        report_serializer_4=None
        print("report idddd",reportId)
        if reportId=='1':
            
            if category=="tax":
                
                returned_list=set_if_not_none(list,'payment_type',1)
                report_data=AllPayments.objects.filter(**returned_list)
                report_serializer=fetchInvoicePaymentSerializer(report_data,many=True)
            elif category=="trip":
                
                report_data=tripData.objects.filter(**returned)
                report_serializer=fetchtripdataSerializer(report_data,many=True)
            return Response({'report_data':report_serializer.data},status.HTTP_200_OK)
        elif reportId=='2':
            returned_list=set_if_not_none(list,'TruckNo',choice)
            report_data=tripData.objects.filter(**returned_list)
            
            report_serializer=fetchtripdataSerializer(report_data,many=True)
            return Response({'report_data':report_serializer.data},status.HTTP_200_OK)
            
        elif reportId=='3':
            returned_list=set_if_not_none(list,'customer',choice)
            report_data=tripData.objects.filter(**returned_list)
            report_serializer=fetchtripdataSerializer(report_data,many=True)    
            return Response({'report_data':report_serializer.data},status.HTTP_200_OK)

        elif reportId=='4':
            returned_list=set_if_not_none(list,'truck_no',choice)
            report_data=truckExpense.objects.filter(**returned_list)
            report_serializer=fetchtruckexSerializer(report_data,many=True) 
            return Response({'report_data':report_serializer.data},status.HTTP_200_OK)
        elif reportId=='5':
            report_data=staffExpense.objects.filter(**returned)
            report_serializer_1=fetchstaffexSerializer(report_data,many=True)
            report_data=truckExpense.objects.filter(**returned)
            report_serializer_2=fetchtruckexSerializer(report_data,many=True)
            report_data=officeExpense.objects.filter(**returned)
            report_serializer_3=fetchofficeexSerializer(report_data,many=True)
            report_data=otherExpense.objects.filter(**returned)
            report_serializer_4=fetchotherexSerializer(report_data,many=True)
            report_data=tripData.objects.filter(**returned)
            report_serializer=fetchtripdataSerializer(report_data,many=True)

            return Response({'report_data':report_serializer.data,'staff_expense':report_serializer_1.data,'truck_expense':report_serializer_2.data,'office_expense':report_serializer_3.data,'other_expense':report_serializer_4.data},status.HTTP_200_OK)
            # print("ssss",report_serializer_1.data)
            # print("aaa",report_serializer_2.data)
            # print("vvvv",report_serializer_3.data)
            # print("bbbb",report_serializer_4.data)
            
        elif reportId=='6':
            returned_list=set_if_not_none(list,'payment_type',1)
            report_data=AllPayments.objects.filter(**returned_list)
            report_serializer=fetchInvoicePaymentSerializer(report_data,many=True)
            return Response({'report_data':report_serializer.data},status.HTTP_200_OK)
        elif reportId=='7':
            report_data=tripData.objects.filter(**returned)
            report_serializer=fetchtripdataSerializer(report_data,many=True)
            return Response({'report_data':report_serializer.data},status.HTTP_200_OK)
        
        elif reportId=='8':
            returned_list=set_if_not_none(list,'truck_no',choice)
            report_data=truckExpense.objects.filter(**returned_list)
            report_serializer=fetchtruckexSerializer(report_data,many=True) 
            return Response({'report_data':report_serializer.data},status.HTTP_200_OK)

        elif reportId=='9':
            returned_list=set_if_not_none(list,'truck_no',choice)
            report_data=truckExpense.objects.filter(**returned_list)
            report_serializer=fetchtruckexSerializer(report_data,many=True) 
            return Response({'report_data':report_serializer.data},status.HTTP_200_OK)
            
            


        
    

    return Response({'message ':"no option slected"},status.HTTP_200_OK)

@login_required
def printReport(request):
    
    return render(request,'report_print.html',role_check(request.user))
# invoice_no=1000000000

# def Invoice(request):
#     no = ''.join(str(random.randint(0,10)) for x in range(5))
#     invoice_number=invoice_no+int(no)
    
#     if request.method=='POST':
        
#         customer=customerProfile.objects.get(id=request.POST["customer"])
#         from_date = request.POST["fromDate"]
#         to_date = request.POST["toDate"]
#         csrf = request.POST["csrfmiddlewaretoken"]

#         context={
#             'fromDate':request.POST["fromDate"],
#             'toDate' : request.POST["toDate"],
#              'customer' :  customer,
#              'location' :  customer.location,
#               'date'  :  date.today(),
#               'csrf':csrf,
#               'invoiceNo':invoice_number,
#               'record_no':invoice_no-99990,
#         }
        
#         return render(request,'invoice.html',context)

@login_required
def printInvoice(request):
    
    return render(request,'invoice_print.html',role_check(request.user))

# @api_view(['POST'])
# def saveinvoice(request):
    
#     if request.method=="POST":
#         customer=customerProfile.objects.get(id=request.POST["customer"])
#         invoice_number=request.POST["payment_no"]
#         payment_amount=int(request.POST["payment_amount"])
#         # payment type '1' means Invoice
#         payments=InvoicePaymentSerializer(data={"date":date.today(),"user":customer.user.id,"payment_no":invoice_number,"payment_type":1,"payment_amount":payment_amount,"payment_status":False},partial=True)
#         if payments.is_valid():
#             payments.save()
#         return Response(status.HTTP_200_OK)
#     return Response({status.HTTP_404_NOT_FOUND})


    

# # Generating pdf


# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         data = {
#             #  'today': datetime.date.today(), 
#              'amount': 39.99,
#             'customer_name': 'Cooper Mann',
#             'order_id': 1233434,
#         }
#         pdf = render_to_pdf('invoice_print.html', data)
#         return HttpResponse(pdf, content_type='application/pdf')







