from django.shortcuts import render,redirect
from App_Account.models import *
from App_Rental.models import *

def Home(request):
    rentpost=House.objects.filter(is_active=True)
    userlist=UserProfile.objects.all()
    context={
        'toppost':rentpost[:6],
        'totalrent':rentpost.count(),
        'houseowner':userlist.filter(userType="1").count(),
        'renter':userlist.filter(userType="2").count()
    }
    return render(request,'index.html',context)

def Details(request,id):
    try:
        singlepost=House.objects.get(id=id)
        house_type_list = list(HOUSE_TYPE_LIST)  
        houseType=""  
        for value,label in house_type_list:
            if value == singlepost.house_type:
                houseType=label
    except House.DoesNotExist:
        return redirect("home")
    contex={
            'rent':singlepost,
            'houseType':houseType
        }
    return render(request,'details.html',contex)