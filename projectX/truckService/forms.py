from django import forms 
from .models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
class DateInput(forms.DateInput):
    input_type = 'date'

class tripForm(forms.ModelForm):
   
    class Meta:
        model = tripData 
        fields = [ 
            'date',
            'customer',
            'pickupPoint',
            'TruckNo',
            'DriverName',
            'nft',
            # 'Discharge_Point',
 
        ] 

class customerField(forms.ModelForm):
   
    class Meta:
        model = tripData 
        fields = [ 
           'customer',
        ]
class truckField(forms.ModelForm):
   
    class Meta:
        model = tripData 
        fields = [ 
           'TruckNo',
        ]

class emptyForm(forms.ModelForm):
   
    class Meta:
        model = tripData 
        fields = [ 
           
        ]
         
         
class NFTform(forms.ModelForm):
   
    class Meta:
        model = nft_detail 
        fields = [ 
        #    'id',  
        #    'trip',
           'order_no',
           'discharge_point',
        ]

    
class customer(forms.ModelForm):
   
    class Meta:
        model = customerProfile
        fields = [ 
            'location',
            'record_number',
            'building_number',
            'contact',
            'tripCharges', 
            'Vat',        
            'managing_by',
            
        ]
        labels = {
        'contact': _('Telephone'),
    }  


class staff(forms.ModelForm):
   
    class Meta:
        model = staffProfile
        fields = [ 
            'joiningDate',
            'visaExpiry',
            'passportExpiry', 
            'position',        
            
            
        ] 
    
     

class userForm(forms.ModelForm):
   
    class Meta:
        model = User
        fields = [ 
            'first_name',
            'last_name',
    
           
        ] 
    
class dischargeForm(forms.ModelForm):
   
    class Meta:
        model = DischargePiont 
        fields = [ 
            'locationName',
            # 'location',
            'Cost',
            'Vat',

        ] 
    

    
class truckForm(forms.ModelForm):
   
    class Meta:
        model = Trucks 
        fields = [ 
            'truckNumber',
            'MulikaExpDate',
            'LastMaintenanceKM',
            'NextMaintenanceKM',
        ] 
    

class staffexForm(forms.ModelForm):
   
    class Meta:
        model = staffExpense 
        fields = [ 

            'date',
            'staff',
            'salary',
            'visaFee',
            'eidFee',
            'medicalIns',
            'overTime',
            'others',
            'deduction',
            'remaining_salary',
            'vat',
            'receipt_no',
            'paid_by',
            'salary_paid_by',

            # 'totalAmount',
        ] 
class truckexForm(forms.ModelForm):
   
    class Meta:
        model = truckExpense 
        fields = [ 

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
            # 'totalAmount',
        ]
        labels = {
            'fuel_litters': _('Fuel Litres'),
        } 
        labels = {
            'fuel': _('Fuel Cost'),
        } 


class truckfuelForm(forms.ModelForm):
   
    class Meta:
        model = truckFuel 
        fields = [ 

            'date',
            'truck_no',
            'fuel_kilometers',  
            'fuel_litters',
            'fuel',
            # 'totalAmount',
        ]
        labels = {
            'fuel_litters': _('Fuel Litres'),
        } 
        labels = {
            'fuel': _('Fuel Cost'),
        } 
class officeexForm(forms.ModelForm):
   
    class Meta:
        model = officeExpense 
        fields = [ 

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
            # 'totalAmount',
        ] 
class otherexForm(forms.ModelForm):
   
    class Meta:
        model = otherExpense 
        fields = [ 

            'date',
            'vendor',
            'expenseName',
            'expenseAmount',
            'vat',
            'receipt_no',
            'paid_by',
            
        ] 

class attendanceForm(forms.ModelForm):
   
    class Meta:
        model = Attendance 
        fields = [ 

            'month',
            'employee',
            'presentDays',
            'absentDays',
            # 'deduction',
            # 'deduction_reason',
            
        ] 


class leavesForm(forms.ModelForm):
   
    class Meta:
        model = Leaves 
        fields = [ 

            'employee',
            'joiningDate',
            'lastLeaveDate',
            'lastReturnDate',
            'leaveRemaining',
            
        ] 


class billForm(forms.ModelForm):
   
    class Meta:
        model = billExpense 
        fields = [ 

            'date',
            'vendor',
            'bill_no',
            'paid_by',
            'amount',
            'channel',
            'vat',
            
        ] 


class deductionForm(forms.ModelForm):
   
    class Meta:
        model = deduction 
        fields = [ 

            'staff',
            'reason',
            'amount',
            
        ] 
            


