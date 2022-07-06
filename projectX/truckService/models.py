from concurrent.futures import process
from datetime import datetime
from dis import dis
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.core.validators import MaxValueValidator, MinValueValidator
# from this.models import Location

COLOR_CHOICES = (
    ('green','GREEN'),
    ('blue', 'BLUE'),
    ('red','RED'),
    ('orange','ORANGE'),
    ('black','BLACK'),
)

LOCATION_CHOICES = (
    ('sharja','Sharja'),
    ('airport', 'Airport'),
    ('baladiya','Baladiya'),
)
MANAGING_BY = (
    ('Owner','Owner'),
    ('Real_Estate', 'Real Estate'),
    ('Other','Other'),
)

MONTHS = (
    ('Jan','Jan'),
    ('Feb', 'Feb'),
    ('March','March'),
    ('April','April'),
    ('May', 'May'),
    ('Jun','Jun'),
    ('July','July'),
    ('August', 'August'),
    ('Sep','Sep'),
    ('Oct','Oct'),
    ('Nov', 'Nov'),
    ('Dec','Dec'),
)
CHANNEL = (
    ('cash','Cash'),
    ('online', 'Online'),
    ('cheque','Cheque'),
    ('card','Card'),
)

ROLE_CHOICES = (
    ('admin','Admin'),
    ('dataentry', 'Data Entry Operator'),
    ('accounts','Accounts'),
)
SALARY_CHOICES = (
    ('exchange', 'Exchange'),
    ('By Hand','By Hand'),
    ('Both','Both'),
)

    
class Role(models.Model):
    roleName =models.CharField(max_length=100,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
            return str(self.roleName)

class pickupPoint(models.Model):
    pointName =models.CharField(max_length=100,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
            return str(self.pointName)

class Location(models.Model):
    locationName =models.CharField(max_length=100,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
            return str(self.locationName)



class UserProfile(models.Model):
     user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
     role=  models.CharField(max_length=100,null=True, choices=ROLE_CHOICES)
     def __str__(self):
            return str(self.user)
# # Customer profile
# class userProfile(models.Model):
#      user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='forignUser')
#      type= models.ForeignKey(Role,on_delete=models.CASCADE, related_name='typeid',null=True) 
#      contact= models.CharField(max_length=30,null=True)
#     #  location = models.CharField(max_length=100,null=True, choices=LOCATION_CHOICES) 
#      location =models.ForeignKey(Location,on_delete=models.CASCADE, related_name='location',null=True)
#      tripCharges=models.IntegerField(null=True)
#      Vat=models.IntegerField(null=True)
#      noOfTrips=models.IntegerField(null=True)
#      vatAmount=models.IntegerField(null=True)
#      ReceivableAmount=models.IntegerField(null=True)
#      joiningDate=models.DateField(null=True)
#      visaExpiry=models.DateField(null=True)
#      passportExpiry=models.DateField(null=True)
#      position=models.CharField(max_length=100 , null=True)
     
#      def __str__(self):
#             return str(self.user.first_name)

# Customer profile
class customerProfile(models.Model):
     user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='forignUser')
     type= models.ForeignKey(Role,on_delete=models.CASCADE, related_name='typeid',null=True) 
     contact= models.CharField(max_length=30,null=True)
     location = models.CharField(max_length=100,null=True) 
    #  location =models.ForeignKey(Location,on_delete=models.CASCADE, related_name='location',null=True)
     record_number = models.CharField(max_length=100,null=True) 
     building_number = models.CharField(max_length=100,null=True) 
     tripCharges=models.DecimalField(null=True,default=0,max_digits=100,decimal_places=2)
     Vat=models.IntegerField(null=True)
     noOfTrips=models.IntegerField(null=True,default=0)
     vatAmount=models.IntegerField(null=True,default=0)
     managing_by=  models.CharField(max_length=100,null=True, choices=MANAGING_BY)
     estate_name=  models.CharField(max_length=100,null=True,default="---")
     contact_person=  models.CharField(max_length=100,null=True,default="---")
     email=  models.CharField(max_length=100,null=True, default="---")
     ReceivableAmount=models.IntegerField(null=True,default=0)
     created_date = models.DateTimeField(auto_now_add=True)
     modified_date = models.DateTimeField(auto_now=True)
     def __str__(self):
            return str(self.user.first_name+' '+self.user.last_name)
 

# Staff profile
class staffProfile(models.Model):
     user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='forignUser1')
     type= models.ForeignKey(Role,on_delete=models.CASCADE, related_name='typeid1',null=True) 
     joiningDate=models.DateField(null=True)
     visaExpiry=models.DateField(null=True,verbose_name = "Visa/EID Expiry")
     passportExpiry=models.DateField(null=True)
     position=models.CharField(max_length=100 , null=True)
     created_date = models.DateTimeField(auto_now_add=True)
     modified_date = models.DateTimeField(auto_now=True)
     def __str__(self):
            return str(self.user.first_name+" "+self.user.last_name)


# Discharge Tabel
class DischargePiont(models.Model):
     locationName = models.CharField(max_length=200)
    #  location =models.CharField(max_length=200)
     Cost = models.IntegerField(null=True)
     Vat = models.IntegerField(null=True)
     created_date = models.DateTimeField(auto_now_add=True)
     modified_date = models.DateTimeField(auto_now=True)
     def __str__(self):
            return str(self.locationName)
# Discharge Tabel
class deduction(models.Model):
     staff = models.ForeignKey(staffProfile,  related_name="ss", on_delete=models.CASCADE,null=True)
     reason =models.CharField(max_length=200)
     amount = models.IntegerField(null=True)
     total_fine = models.IntegerField(null=True,default=0)
     created_date = models.DateTimeField(auto_now_add=True)
     modified_date = models.DateTimeField(auto_now=True)
     def __str__(self):
            return str(self.staff)

            
class remaining_deduction(models.Model):
     staff = models.ForeignKey(staffProfile,  related_name="sas", on_delete=models.CASCADE,null=True)
     total_payable = models.IntegerField(null=True,default=0)
     deduct = models.IntegerField(null=True,default=0)
     created_date = models.DateTimeField(auto_now_add=True)
     modified_date = models.DateTimeField(auto_now=True)
     def __str__(self):
            return str(self.total_payable)            


class Trucks(models.Model):
     truckNumber = models.IntegerField( primary_key=True )
     MulikaExpDate =models.DateField()
     LastMaintenanceKM =models.IntegerField()
     NextMaintenanceKM= models.IntegerField()
     created_date = models.DateTimeField(auto_now_add=True)
     modified_date = models.DateTimeField(auto_now=True)
     def __str__(self):
            return str(self.truckNumber)

# Truck Fuel data 

class truckFuel(models.Model):
     date = models.DateField()
     truck_no =models.ForeignKey(Trucks,on_delete=models.CASCADE,null=True)
     fuel_kilometers=models.IntegerField(null=True,default=0)
     fuel_litters=models.IntegerField(null=True,default=0)
     fuel = models.IntegerField(null=True,default=0)
     created_date = models.DateTimeField(auto_now_add=True)
     modified_date = models.DateTimeField(auto_now=True)
     def __str__(self):
            return str(self.truck_no)



class tripData(models.Model):
    date = models.DateField(null=True)
    customer = models.ForeignKey(customerProfile, related_name="customer", on_delete=models.CASCADE,null=True)
    pickupPoint = models.CharField(max_length=100, default='')
    TruckNo = models.ForeignKey(Trucks,  related_name="truck" , on_delete=models.CASCADE,null=True)
    DriverName = models.ForeignKey(staffProfile,  related_name="DriverName", on_delete=models.CASCADE,null=True)
    nft = models.IntegerField(null=True,default=0,validators=[ MaxValueValidator(8),MinValueValidator(1)])
    # Discharge_Point = models.ForeignKey(DischargePiont, related_name="dischargepoint", default='',on_delete=models.CASCADE,null=True)
    Vat=models.IntegerField(null=True,default=0)
    vatAmount=models.IntegerField(null=True,default=0)
    ReceivableAmount=models.DecimalField(null=True,default=0,max_digits=100,decimal_places=2)
    discharge_cost=models.IntegerField(null=True,default=0)
    discharge_vat=models.IntegerField(null=True,default=0)
    total_discharge_cost=models.IntegerField(null=True,default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
            return str(self.id)
    class Meta:
        verbose_name='TripData'
        verbose_name_plural='TripData'
    # dischargePoint = models.ForeignKey(DischargePiont,on_delete=models.CASCADE, null=True)

class nft_detail(models.Model):
    trip= models.ForeignKey(tripData,on_delete=models.CASCADE, related_name='trip_data',null=True) 
    order_no =models.CharField(max_length=100,null=True)
    discharge_point = models.CharField(max_length=100,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
            return str(self.order_no)

class staffExpense(models.Model):
    date = models.DateField(null=True)
    staff = models.ForeignKey(staffProfile, related_name="staff", on_delete=models.CASCADE)
    salary = models.IntegerField(null=True,default=0)
    salary_paid_by = models.CharField(max_length=100, null=True, verbose_name = "Mode of Payment",choices=SALARY_CHOICES)
    visaFee = models.IntegerField(null=True,default=0)
    exchange =models.CharField(null=True,max_length=200)
    by_hand = models.CharField(null=True,max_length=200)
    eidFee = models.IntegerField(null=True,default=0)
    medicalIns = models.IntegerField(null=True,default=0)
    overTime = models.IntegerField(null=True,default=0)
    others = models.IntegerField(null=True,default=0)
    deduction = models.IntegerField(null=True,default=0)
    vat=models.IntegerField(null=True,default=0, verbose_name = "VAT Amount")
    paid_by = models.ForeignKey(staffProfile,  related_name="staffd", on_delete=models.CASCADE,null=True)
    receipt_no =models.CharField(null=True,max_length=200,blank=True)
    totalAmount = models.IntegerField(null=True,default=0)
    remaining_salary=models.IntegerField(null=True,default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
            return str(self.staff.user.first_name+" "+self.staff.user.last_name+" Expense")    

class truckExpense(models.Model):
    date = models.DateField(null=True)
    truck_no = models.ForeignKey(Trucks, related_name="truckex", on_delete=models.CASCADE)
    renewalFee = models.IntegerField(null=True,default=0)
    fuel_kilometers=models.IntegerField(null=True,default=0)
    fuel_litters=models.IntegerField(null=True,default=0)
    fuel = models.IntegerField(null=True,default=0)
    maintenance = models.IntegerField(null=True,default=0)
    repair_replace = models.IntegerField(null=True,default=0)
    parking = models.IntegerField(null=True,default=0)
    others = models.IntegerField(null=True,default=0)
    vat=models.IntegerField(null=True,default=0, verbose_name = "VAT Amount")
    receipt_no =models.CharField(null=True,max_length=200,blank=True)
    paid_by = models.ForeignKey(staffProfile,  related_name="staffc", on_delete=models.CASCADE,null=True)
    totalAmount = models.IntegerField(null=True,default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
            return str(self.truck_no) 

class officeExpense(models.Model):
    date = models.DateField(null=True,)
    vendor = models.CharField(null=True,max_length=200)
    officeRent = models.IntegerField(null=True,default=0)
    utilityBills = models.IntegerField(null=True,default=0)
    stationary = models.IntegerField(null=True,default=0)
    kitchen = models.IntegerField(null=True,default=0)
    others = models.IntegerField(null=True,default=0)
    vat=models.IntegerField(null=True,default=0, verbose_name = "VAT Amount")
    receipt_no =models.CharField(null=True,max_length=200,blank=True)
    paid_by = models.ForeignKey(staffProfile,  related_name="staffa", on_delete=models.CASCADE,null=True)
    totalAmount = models.IntegerField(null=True,default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
      

class billExpense(models.Model):
    date = models.DateField(null=True)
    vendor = models.CharField(null=True,max_length=200)
    bill_no  = models.IntegerField(null=True,default=0)
    paid_by  = models.CharField(null=True,max_length=200)
    amount = models.IntegerField(null=True,default=0)
    channel= models.CharField(null=True,max_length=250, choices=CHANNEL) 
    vat=models.IntegerField(null=True,default=0, verbose_name = "VAT Amount")
    totalAmount = models.IntegerField(null=True,default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
            return str(self.bill_no)    

class otherExpense(models.Model):
    date = models.DateField(null=True)
    vendor = models.CharField(null=True,max_length=200)
    expenseName = models.CharField(null=True,max_length=200)
    expenseAmount = models.IntegerField(null=True,default=0)
    vat=models.IntegerField(null=True,default=0, verbose_name = "VAT Amount")
    receipt_no =models.CharField(null=True,max_length=200,blank=True)
    paid_by = models.ForeignKey(staffProfile,  related_name="staffb", on_delete=models.CASCADE,null=True)
    totalAmount = models.IntegerField(null=True,default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
            return str(self.expenseName) 
   
class Expenses(models.Model):
    staffExpenses = models.IntegerField(null=True,default=0)
    officeExpenses = models.IntegerField(null=True,default=0)
    truckExpenses = models.IntegerField(null=True,default=0)
    otherExpenses = models.IntegerField(null=True,default=0)
    totalExpenses = models.IntegerField(null=True,default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
            return str(self.date)    
   

class AllPayments(models.Model):
    date= models.DateField()
    # from_to_date=models.CharField(max_length=255)
    user=models.ForeignKey(User, related_name="user_payments", on_delete=models.CASCADE)
    payment_no=models.IntegerField()
    vendor = models.CharField(null=True,max_length=200)
    expense_type = models.CharField(null=True,max_length=200)
    payment_type=models.IntegerField()
    payment_amount=models.IntegerField(null=True,default=0)
    reason=models.CharField(max_length=255,null=True,blank=True)
    processed_by=models.CharField(max_length=255,null=True,blank=True)
    channel=models.CharField(max_length=255,blank=True,null=True)
    payment_status=models.BooleanField()
    tripsAmount=models.IntegerField(blank=True,null=True)
    tax=models.IntegerField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
            return str(self.payment_no)   
    

class Attendance(models.Model):
    month = models.CharField(max_length=250, choices=MONTHS) 
    employee = models.ForeignKey(staffProfile,related_name="employee",on_delete=models.CASCADE,null=True)
    presentDays = models.IntegerField(null=True,default=0)
    absentDays = models.IntegerField(null=True,default=0)
    # deduction = models.IntegerField(null=True,default=0)
    # deduction_reason = models.CharField(max_length=250, null=True) 
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
            return str(self.month)   

class Leaves(models.Model):
     
    employee = models.ForeignKey(staffProfile,on_delete=models.CASCADE,null=True)
    joiningDate=models.DateField(null=True)
    lastLeaveDate=models.DateField(null=True)
    lastReturnDate=models.DateField(null=True)
    leaveRemaining = models.IntegerField(null=True,default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
            return str(self.employee)  






 



