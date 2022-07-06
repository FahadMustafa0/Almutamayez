from django.contrib import admin
from django.urls import path
from truckService import views
from .utils import is_user_admin_Permission

urlpatterns = [
    path('login_check/', views.login_check, name='login_check'),
    path('create_user/', views.createUser, name='create_user'),
    path('create_users/', views.create_users, name='create_users'),
    path('index/', views.index, name='index'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),   

    path('tripdata/', views.tripdata, name='trip-data'),
    path('customerlocationfetch/', views.customerlocationfetch, name='trip-customerlocationfetch'),
    path('addTripdata/', views.addTripdata, name='addTripdata'),
    path('manageTripdata/', views.manageTripdata, name='manageTripdata'),
    path('tripslistshow/', views.tripslistshow, name='tripslistshow'),
    path('nftlistshow/', views.nftlistshow, name='nftlistshow'),
    path('updateTripdata/<int:pk>/', views.updateTripdata, name='updateTripdata'),

    path('deleteTripdata/', is_user_admin_Permission(views.deleteTripdata), name='deleteTripdata'),
    
    path('customer/', views.customerView, name='customer'),
    path('customerlist/', views.customerList, name='customerlist'),
    path('updatecustomer/<int:pk>/', views.updateCustomer, name='updatecustomer'),
    path('deletecustomer/', is_user_admin_Permission(views.deleteCustomer), name='deletecustomer'),
    path('customerlistshow/', views.customerListShow, name='customerlistshow'),
    path('createcustomer/', views.createCustomer, name='createcustomer'),

    path('createstaff/', views.createStaff, name='createstaff'),
    path('addstaff/', views.addstaff, name='addstaff'),
    path('managestaff/', views.staffList, name='managestaff'),
    path('stafflistshow/', views.staffListShow, name='stafflistshow'),  
    path('updatestaff/<int:pk>/', views.updateStaff, name='updatestaff'),
    path('deletestaff/', is_user_admin_Permission(views.deleteStaff), name='deletestaff'),

    path('createdischargepoint/', views.createDischarge, name='createdischargepoint'),
    path('addDischarge/', views.addDischarge, name='adddischarge'),
    path('dischargepointlist/', views.dischargepointList, name='dischargepointlist'),
    path('dischargelistshow/', views.dischargeListShow, name='dischargelistshow'),
    path('updateDischargepoint/<int:pk>/', views.updatedischargepoint, name='updateDischargepoint'),
    path('deletedischargepoint/', is_user_admin_Permission(views.deleteDischargepoint), name='deletedischargepoint'),

    path('deduction/', views.creatededuction, name='deduction'),
    path('addDeduction/', views.addDeduction, name='addDeduction'),
    path('managededuction/', views.managededuction, name='managededuction'),
    path('deductionlistshow/', views.deductionlistshow, name='deductionlistshow'),
    path('updateDeduction/<int:pk>/', views.updateDeduction, name='updateDeduction'),
    path('deletededuction/', is_user_admin_Permission(views.deletededuction), name='deletededuction'),


    path('createtruck/', views.createTrucks, name='createtruck'),
    path('addtruck/', views.addTrucks, name='addtruck'),
    path('managetrucks/', views. managetrucks, name='managetrucks'),
    path('trucklistshow/', views.trucklistshow, name='trucklistshow'),
    path('updateTrucks/<int:truckno>/', views.updateTruck, name='updateTrucks'),
    path('deletetruck/', is_user_admin_Permission(views.deleteTruck), name='deletetruck'),


    path('fuelData/', views.manageFuelData, name='fuelData'),
    path('fuelDataShow/', views.FuelDataShow, name='fuelDataShow'),

    path('expenses/', views.Expenses, name='expenses'),
    path('addexpenses/', views.addExpenses, name='addexpenses'),

    path('managestaffexpense/', views. manageStaffExpense, name='managestaffexpense'),
    path('staffexpenselistshow/', views.staffExpenseListshow, name='staffexpenselistshow'),
    path('updatestaffexpense/<int:pk>/', views.updateStaffExpense, name='updatestaffexpense'),
    path('deletestaffexpence/', is_user_admin_Permission(views.deleteStaffExpense), name='deletestaffexpence'),
    
    path('managetruckexpense/', views. manageTruckExpense, name='managetruckexpense'),
    path('truckexpenselistshow/', views.truckExpenseListshow, name='truckexpenselistshow'),
    path('updatetruckexpense/<int:pk>/', views.updateTruckExpense, name='updatetruckexpense'),
    path('deletetruckexpence/', is_user_admin_Permission(views.deleteTruckExpense), name='deletetruckexpence'),
    
    path('manageofficeexpense/', views. manageOfficeExpense, name='manageofficeexpense'),
    path('officeexpenselistshow/', views.officeExpenseListshow, name='officeexpenselistshow'),
    path('updateofficeexpense/<int:pk>/', views.updateOfficeExpense, name='updateofficeexpense'),
    path('deleteofficeexpence/', is_user_admin_Permission(views.deleteOfficeExpense), name='deleteofficeexpence'),

    path('manageotherexpense/', views. manageOtherExpense, name='manageotherexpense'),
    path('otherexpenselistshow/', views.otherExpenseListshow, name='otherexpenselistshow'),
    path('updateotherexpense/<int:pk>/', views.updateOtherExpense, name='updatestaffexpense'),
    path('deleteotherexpence/', is_user_admin_Permission(views.deleteOtherExpense), name='deleteotherexpence'),

    path('managebillexpense/', views. manageBillExpense, name='managebillexpense'),
    path('billexpenselistshow/', views.billExpenseListshow, name='billexpenselistshow'),
    path('updatebillexpense/<int:pk>/', views.updateBillExpense, name='updatebillexpense'),
    path('deletebillexpence/', is_user_admin_Permission(views.deleteBillExpense), name='deletebillexpence'),

    path('managetotalexpense/', views. manageTotalExpense, name='managetotalexpense'),
    path('totalexpenselistshow/', views.totalExpenseListshow, name='totalexpenselistshow'),
    # path('updatetotalexpense/<int:pk>/', views.updateTotalExpense, name='updatetotalexpense'),
    # path('deletetotalexpence/', views.deleteTotalExpense, name='deletetotalexpence'),

    path('generateinvoice/', views. generateInvoice, name='generateinvoice'),
    path('createinvoice/', views.createInvoice, name='createinvoice'),
    path('invoice/', views.Invoice, name='invoice'),
    path('invoice_print/', views.printInvoice, name='invoice_print'),
    path('invoice/', views.Invoice, name='invoice'),
    path('saveinvoice/', views.saveinvoice, name='saveinvoice'),
    # path('pdf/', views.GeneratePdf.as_view(), name='pdf'),
    path('generatepdf/', views.GeneratePdf.as_view(), name='generatepdf'),

#   Payments Module APis

    path('pendinginvoices/', views.pendingInvoices, name='pendinginvoices'),
    path('pendinginvoicedata/', views.pendingInvoiceData, name='pendinginvoicedata'),
    path('paymentsautodata/', views.paymentsAutoData, name='paymentsautodata'),
    path('updatestatus/', views.updatingReceivedStatus, name='receivedPayments'),
    path('receivedinvoices/', views.receivedInvoices, name='receivedInvoices'),
    path('receivedinvoicedata/', views.receivedInvoiceData, name='receivedinvoicedata'),
    path('payments/', views.Payments, name='payments'),

    path('pendingbills/', views.pendingBills, name='pendingbills'),
    path('pendingbillData/', views.pendingBillData, name='pendingbillData'),
    path('paidbills/', views.paidBills, name='paidbills'),
    path('allpaymentsdata/', views.allPaymentsData, name='allpaymentsdata'),
    path('allpayments/', views.allPayments, name='allpayments'),
    

    path('income/', views.Income, name='income'),



    # path('createattendance/', views.createDischarge, name='createattendance'),
    path('attendance/', views.attendance, name='attendance'),
    path('addattendance/', views.addAttendance, name='addattendance'),
    path('manageattendance/', views.manageAttendance, name='manageattendance'),
    path('attendancelistshow/', views.attendanceListshow, name='attendancelistshow'),
    path('updateAttendance/<int:pk>/', views.updateAttendace, name='updateAttendance'),
    path('deleteAttendance/', is_user_admin_Permission(views.deleteAttendance), name='deleteAttendance'),
    
    
    path('leaves/', views.leaves, name='leaves'),
    path('joiningdatefetch/', views.joiningDatefetch , name='joiningdatefetch'),

    path('addleaves/', views.addLeaves, name='addleaves'),
    path('manageleaves/', views.manageLeaves, name='manageleaves'),
    path('leaveslistshow/', views.leavesListshow, name='leaveslistshow'),
    path('updateLeaves/<int:pk>/', views.updateLeaves, name='updateLeaves'),
    path('deleteLeaves/', is_user_admin_Permission(views.deleteLeaves), name='deleteLeaves'),
    


    path('generatereport/<int:id>/', views.generateReport, name='generatereport'),
    path('report/', views.Report, name='report'),
    path('createreport/', views.createReport, name='createreport'),
    
    path('report_print/', views.printInvoice, name='report_print'),
    # path('invoice/', views.Invoice, name='invoice'),
    # path('saveinvoice/', views.saveinvoice, name='saveinvoice'),
    # # path('pdf/', views.GeneratePdf.as_view(), name='pdf'),
    # path('generatepdf/', views.GeneratePdf.as_view(), name='generatepdf'),

    ]