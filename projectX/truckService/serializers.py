from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user','role']



class locationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','locationName']

        
# class pickupLocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = pickupPoint
#         fields = ['id','pointName']
# for customers


class customerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # location =pickupLocationSerializer()
    class Meta:
        model = customerProfile
        fields = ['id','user','type_id','contact','location','record_number','building_number','managing_by','tripCharges','Vat','noOfTrips','vatAmount','ReceivableAmount','estate_name','contact_person','email']

class staffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # location =locationSerializer()
    class Meta:
        model = staffProfile
        fields = ['id','user','type_id','joiningDate','visaExpiry','passportExpiry','position']

class fetchCustomerprofileSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    # location =pickupLocationSerializer()
    class Meta:
        model = customerProfile
        fields = ['id','user','type_id','contact','location','record_number','building_number','managing_by','tripCharges','Vat','noOfTrips','vatAmount','ReceivableAmount','estate_name','contact_person','email']

class fetchStaffprofileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = staffProfile
        fields = ['id','user','type_id','joiningDate','visaExpiry','passportExpiry','position']

# for Discharge point


class dischargeSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # location =locationSerializer()
    class Meta:
        model = DischargePiont
        fields = ['id','locationName','Vat','Cost']


class fetchdischargeSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # location =locationSerializer()
    class Meta:
        model = DischargePiont
        fields = ['id','locationName','Vat','Cost']

class deductionSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # location =locationSerializer()
    class Meta:
        model = deduction
        fields = ['id','staff','reason','amount']


class fetchdeductionSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    staff=staffSerializer(read_only=True)
    class Meta:
        model = deduction
        fields = ['id','staff','reason','amount','total_fine']



class trucksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trucks
        fields = ['truckNumber','MulikaExpDate','LastMaintenanceKM','NextMaintenanceKM']




class truckFuelSerializer(serializers.ModelSerializer):
    # truckNo = serializers.RelatedField(source='truckNumber', read_only=True)
    # truckNo = trucksSerializer(read_only=True)

    class Meta:
        model = truckFuel
        fields = ['id','date','truck_no','fuel_kilometers','fuel_litters','fuel']




class tripdataSerializer1(serializers.ModelSerializer):
    # customer= customerSerializer(read_only=True)
    # TruckNo=truckFuelSerializer(read_only=True)
    # DriverName=staffSerializer(read_only=True)
    class Meta:
        model = tripData
        fields = ['id','date','customer','pickupPoint','TruckNo','DriverName','nft']
class tripdataSerializer(serializers.ModelSerializer):
    # customer= customerSerializer(read_only=True)
    # TruckNo=truckFuelSerializer(read_only=True)
    # DriverName=staffSerializer(read_only=True)
    class Meta:
        model = tripData
        fields = ['id','date','customer','pickupPoint','TruckNo','DriverName','nft','vatAmount','ReceivableAmount']


class fetchtripdataSerializer(serializers.ModelSerializer):
    customer= customerSerializer(read_only=True)
    TruckNo=trucksSerializer(read_only=True)
    DriverName=staffSerializer(read_only=True)
    # nft_details=nft_detail(read_only=True)
    class Meta:
        model = tripData
        fields = '__all__'
class nftTripDataSerialzer(serializers.ModelSerializer):
    nft_detail = serializers.SerializerMethodField()
    class Meta:
        model=tripData
        fields = '__all__'
    def get_nft_detail(self, obj):
        custom_list = nft_detail.objects.filter(trip=obj)
        custom_list=NFTSerializer(custom_list,many=True)
        print(custom_list.data,"???????????????????????????????????")
        return custom_list.data 

class NFTSerializer(serializers.ModelSerializer):
    # customer= customerSerializer(read_only=True)
    # TruckNo=truckFuelSerializer(read_only=True)
    # DriverName=staffSerializer(read_only=True)

    # trip=fetchtripdataSerializer()
    class Meta:
        model = nft_detail
        fields = '__all__'
class fetchNFTSerializer(serializers.ModelSerializer):
    # customer= customerSerializer(read_only=True)
    # TruckNo=truckFuelSerializer(read_only=True)
    # trip=tripData(read_only=True)   
    trip=tripdataSerializer(read_only=True)
    class Meta:
        model = nft_detail
        fields = '__all__'

# --------------------------------------------------

class staffexSerializer(serializers.ModelSerializer):
    # customer= customerSerializer(read_only=True)
    # TruckNo=truckFuelSerializer(read_only=True)
    # DriverName=staffSerializer(read_only=True)
    class Meta:
        model = staffExpense
        fields = [
            'id',
            'date',
            'staff',
            'salary',
            'salary_paid_by',
            'exchange',
            'by_hand',
            'visaFee',
            'eidFee',
            'medicalIns',
            'overTime',
            'others',
            'deduction',
            'vat',
            'paid_by',
            'receipt_no',
            'totalAmount',
            'remaining_salary',
            ]


class fetchstaffexSerializer(serializers.ModelSerializer):
    staff=staffSerializer(read_only=True)
    paid_by=staffSerializer(read_only=True)
    class Meta:
        model = staffExpense
        fields = [
            'id',
            'date',
            'staff',
            'salary',
            'salary_paid_by',
            'exchange',
            'by_hand',
            'visaFee',
            'eidFee',
            'medicalIns',
            'overTime',
            'others',
            'deduction',
            'vat',
            'paid_by',
            'receipt_no',
            'totalAmount',
            'remaining_salary',]


class truckexSerializer(serializers.ModelSerializer):
    # customer= customerSerializer(read_only=True)
    # TruckNo=truckFuelSerializer(read_only=True)
    # DriverName=staffSerializer(read_only=True)
    class Meta:
        model = truckExpense
        fields = [ 
            'id',
            'date',
            'truck_no',
            'renewalFee',
            'fuel_kilometers',
            'fuel_litters',
            'fuel',
            'maintenance',
            'repair_replace',
            'parking',
            'others',
            'vat',
            'receipt_no',
            'paid_by',
            'totalAmount',
        ] 

class fetchtruckexSerializer(serializers.ModelSerializer):
    truck_no=trucksSerializer(read_only=True)
    paid_by=staffSerializer(read_only=True)
    class Meta:
        model = truckExpense
        fields = [ 
            'id',
            'date',
            'truck_no',
            'renewalFee',
            'fuel_kilometers',
            'fuel_litters',
            'fuel',
            'maintenance',
            'repair_replace',
            'parking',
            'others',
            'vat',
            'receipt_no',
            'paid_by',
            'totalAmount',
        ] 



class officeexSerializer(serializers.ModelSerializer):
    # customer= customerSerializer(read_only=True)
    # TruckNo=truckFuelSerializer(read_only=True)
    # DriverName=staffSerializer(read_only=True)
    
    class Meta:
        model = officeExpense
        fields = [ 
            'id',
            'date',
            'vendor',
            'officeRent',
            'utilityBills',
            'stationary',
            'kitchen',
             
            'others',
            'vat',
            'receipt_no',
            'paid_by',
            'totalAmount',
        ] 

class fetchofficeexSerializer(serializers.ModelSerializer):
    paid_by=staffSerializer(read_only=True)
    class Meta:
        model = officeExpense
        fields = [ 
            'id',
            'date',
            'vendor',
            'officeRent',
            'utilityBills',
            'stationary',
            'kitchen',
             
            'others',
            'vat',
            'receipt_no',
            'paid_by',
            'totalAmount',
        ] 


class otherexSerializer(serializers.ModelSerializer):
    # customer= customerSerializer(read_only=True)
    # TruckNo=truckFuelSerializer(read_only=True)
    # DriverName=staffSerializer(read_only=True)
    class Meta:
        model = otherExpense
        fields = [ 
            'id',
            'date',
            'vendor',
            'expenseName',
            'expenseAmount',
            'vat',
            'receipt_no',
            'paid_by',
            'totalAmount',
            
        ] 


class fetchotherexSerializer(serializers.ModelSerializer):
    paid_by=staffSerializer(read_only=True)
    class Meta:
        model = otherExpense
        fields = [ 
            'id',
            'date',
            'vendor',
            'expenseName',
            'expenseAmount',
            'vat',
            'receipt_no',
            'paid_by',
            'totalAmount',
            
        ] 


class ExpenseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Expenses
        fields = [ 
            'id',
            'staffExpenses',
            'officeExpenses',
            'truckExpenses',
            'otherExpenses',
            'totalExpenses',
            
        ]


class incomeExpenseSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = AllPayments
        fields = [ 
            'date',
            'user',
            'payment_type',
            'payment_status',
            'payment_no',
            'payment_amount',
            
            ]

class InvoicePaymentSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = AllPayments
        fields = [ 
            'id',
            'date',
            'vendor',
            'expense_type',
            'user',
            'payment_no',
            'payment_type',
            'payment_amount',
            'payment_status',
            'tax',
            'tripsAmount',

            
            ]
class fetchInvoicePaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AllPayments
        fields = [ 
            'id',
            'date',
            'vendor',
            'expense_type',
            'user',
            'payment_no',
            'payment_type',
            'payment_amount',
            'payment_status',
            'processed_by',
            'channel',
            'tax',
            'tripsAmount',
            ]


class InvoicesAutoDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = AllPayments
        fields = [ 
        
            'payment_no',
            'payment_amount',
            # 'payment_status',
            
            ]


class AttendanceSerializer(serializers.ModelSerializer):
    # customer= customerSerializer(read_only=True)
    # TruckNo=truckFuelSerializer(read_only=True)
    # DriverName=staffSerializer(read_only=True)
    class Meta:
        model = Attendance
        fields = '__all__'



class fetchAttendanceSerializer(serializers.ModelSerializer):
    
    employee=staffSerializer(read_only=True)
    class Meta:
        model = Attendance
        fields = '__all__'



class LeavesSerializer(serializers.ModelSerializer):
    # customer= customerSerializer(read_only=True)
    # TruckNo=truckFuelSerializer(read_only=True)
    # DriverName=staffSerializer(read_only=True)
    class Meta:
        model = Leaves
        fields = '__all__'


class fetchLeavesSerializer(serializers.ModelSerializer):
    
    employee=staffSerializer(read_only=True)
    class Meta:
        model = Leaves
        fields = '__all__'



class billSerializer(serializers.ModelSerializer):
    # customer= customerSerializer(read_only=True)
    # TruckNo=truckFuelSerializer(read_only=True)
    # DriverName=staffSerializer(read_only=True)
    class Meta:
        model = billExpense
        fields = '__all__'


class ramainingSerializer(serializers.ModelSerializer):
    # customer= customerSerializer(read_only=True)
    # TruckNo=truckFuelSerializer(read_only=True)
    # DriverName=staffSerializer(read_only=True)
    class Meta:
        model = remaining_deduction
        fields = '__all__'


class fetchRemainingSerializer(serializers.ModelSerializer):
    
    staff=staffSerializer(read_only=True)
    class Meta:
        model = remaining_deduction
        fields = '__all__'