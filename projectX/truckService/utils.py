from email import message
import xhtml2pdf.pisa as pisa
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from .models import *
from rest_framework.response import Response



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



def is_user_admin_Permission(function):
    def wrap(request, *args, **kwargs):
        
        if request.user:
            role = UserProfile.objects.get(user=request.user).role
        
        if role=="admin":
            return function(request, *args, **kwargs)
        else:
            return JsonResponse({'allowed':True})

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def role_check(u):
    allowed=False
    dataEntry=True
    if(u.is_authenticated):
        role = UserProfile.objects.get(user=u).role
        print("------------",role)
        if role=="admin":
            allowed=True
        if role=="dataentry":
            dataEntry=False
        print("allowed:",allowed,dataEntry)
        return {'allowed':allowed,'dataentry':dataEntry}

# def is_user_admin_Permission(function):
#     def wrap(request, *args, **kwargs):
        
#         if request.user:
#             role = UserProfile.objects.get(user=request.user).role
        
#         if role=="admin":
#             return function(request, *args, **kwargs)
#         else:
#             return JsonResponse({'allowed':True})


       
#         u=request.user
#         if(u.is_authenticated):
#             return render(request,'index.html')
        
#         return render(request,'login.html',{'user':u})

#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap

