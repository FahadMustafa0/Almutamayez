from django.db.models.signals import post_delete, post_save, pre_delete,pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=tripData)
def post_save_create_profile(sender, instance, created, **kwargs):
    # print('sender', sender)
    # print('instance', instance)
    if created:
        newtripcustomer =instance.customer.id
        customerobj=customerProfile.objects.get(id=newtripcustomer)
        
        nft=instance.nft 
        instance.Vat=customerobj.Vat
        vat=customerobj.Vat
        tripcharges=customerobj.tripCharges
        totalcharges_1trip=tripcharges*nft
        instance.ReceivableAmount=totalcharges_1trip
        vat_amount_1trip=  totalcharges_1trip*vat  
        vat_amount_1trip=vat_amount_1trip/100  
        instance.vatAmount=vat_amount_1trip
        # print(">>>>>>>>>>>>>>>>",customerobj.Vat,totalcharges_1trip,vat_amount_1trip)
        instance.save()

        customerobj.noOfTrips +=instance.nft 
        customerobj.save()
        # calculating and saving Vat Amount And receivable amount
        # vat=customerobj.Vat
        # tripcharges=customerobj.tripCharges
        totalnft=customerobj.noOfTrips
        totalcharges=tripcharges*totalnft
        vat_amount=  totalcharges*vat  
        vat_amount=vat_amount/100  
        customerobj.vatAmount=vat_amount
        customerobj.ReceivableAmount=totalcharges+vat_amount
        customerobj.save()
    else:
        newtripcustomer =instance.customer.id
        customerobj=customerProfile.objects.get(id=newtripcustomer)
        # calculating and saving Vat Amount And receivable amount
        vat=customerobj.Vat
        tripcharges=customerobj.tripCharges
        totalnft=customerobj.noOfTrips
        totalcharges=tripcharges*totalnft
        vat_amount=  totalcharges*vat  
        vat_amount=vat_amount/100  
        customerobj.vatAmount=vat_amount
        customerobj.ReceivableAmount=totalcharges+vat_amount
        customerobj.save()



    
@receiver(post_delete, sender=tripData)
def post_delete_actions(sender, instance, **kwargs):
        newtripcustomer =instance.customer.id
        customerobj=customerProfile.objects.get(id=newtripcustomer)
        
        customerobj.noOfTrips -=instance.nft 
        customerobj.save()
        # calculating and saving Vat Amount And receivable amount
        vat=customerobj.Vat
        tripcharges=customerobj.tripCharges
        totalnft=customerobj.noOfTrips
        totalcharges=tripcharges*totalnft
        vat_amount=  totalcharges*vat  
        vat_amount=vat_amount/100  
        customerobj.vatAmount=vat_amount
        customerobj.ReceivableAmount=totalcharges+vat_amount
        customerobj.save()


# @receiver(pre_save, sender=tripData)
# def post_update_actions(sender, instance,created, **kwargs):
#     if created == False:
#         newtripcustomer =instance.id
#         customerobj=customerProfile.objects.get(id=newtripcustomer)
        
#         customerobj.noOfTrips -=instance.nft 
#         customerobj.save()
#         # calculating and saving Vat Amount And receivable amount
#         vat=customerobj.Vat
#         tripcharges=customerobj.tripCharges
#         totalnft=customerobj.noOfTrips
#         totalcharges=tripcharges*totalnft
#         vat_amount=  totalcharges*vat  
#         vat_amount=vat_amount/100  
#         customerobj.vatAmount=vat_amount
#         customerobj.ReceivableAmount=totalcharges+vat_amount
#         customerobj.save()