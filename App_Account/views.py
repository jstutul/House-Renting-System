from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate,update_session_auth_hash
import requests
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from functools import wraps
from App_Rental.models import City,House,HouseImage,HOUSE_TYPE_LIST,HouseRent,ContractUs
from App_Rental.forms import HouseForm
from django.shortcuts import get_object_or_404
from datetime import date
from App_Account.models import *
from django.core.files.storage import FileSystemStorage
# from weasyprint import HTML


def house_owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.userprofile.userType == "1":
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'accessdenied.html')
        else:
            return redirect('App_Account:login')
    return wrapper

def renter_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userprofile.userType == "2":
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'accessdenied.html')
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request,'accessdenied.html')
        return view_func(request, *args, **kwargs)
    return wrapper


def SignupView(request):
    if request.method == 'POST':
        username        = request.POST['username']
        email           = request.POST['email']
        password        = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        userType        = request.POST['userType']
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists.")    
        elif password!=confirmPassword:
            messages.error(request,"Password not matching.")
        elif userType=="0":
            messages.error(request,"User type not selected.")
        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.is_active = False
            user.save()
            user.refresh_from_db()
            #User Activation
            current_site=get_current_site(request)
            user.userprofile.userType=userType
            user.save()
            user.refresh_from_db()
            mail_subject='EasyRent Account Activation'
            message=render_to_string('App_Account/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid':  urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request,"Registrations successfull")
            return redirect('/account/login?command=verification&email='+str(to_email))
        return render(request, 'App_Account/signup.html') 
    return render(request,'App_Account/signup.html')

def LoginView(request):
    auth.logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            # messages.success(request,"you are now authenticated")
            url=request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query 
                params=dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:   
                return redirect('home')
        else:
            messages.error(request, "invalid credential")
            return redirect('App_Account:login')
    context={}
    return render(request,'App_Account/login.html',context)

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "Successfully Logout")
    return redirect('App_Account:login')


def activateView(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Email Confiemd.')
        return redirect('App_Account:login')
    else:
        return HttpResponse('Activation link is invalid!')
    

@login_required(login_url='App_Account:login')      
def LogoutView(request):
    auth.logout(request)
    messages.success(request, "Successfully Logout")
    return redirect('App_Account:login')

@login_required(login_url='App_Account:login')  
def PasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('App_Account:dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'App_Account/change_password.html', {
        'form': form
    })

@login_required(login_url='App_Account:login') 
def DashboardView(request):
    houses=House.objects.all()
    users=UserProfile.objects.all()
    rented=HouseRent.objects.filter(is_paid=True)
    total=0
    for i in rented:
        total+=i.post.advacne_rent
    context={
        'housepost':houses.count,
        'approved':houses.filter(is_active=True,is_reject=False).count,
        'rejected':houses.filter(is_reject=True).count,
        'saled':houses.filter(is_rented=True).count,
        'users':users.count,
        'houseowner':users.filter(userType=1).count,
        'renter':users.filter(userType=2).count,
        'totalreneted':total
    }
    return render(request,'App_Dashboard/dashboard.html',context)    

@login_required(login_url='App_Account:login') 
def ProfileView(request):
    return render(request,'App_Dashboard/profile.html')    

@login_required(login_url='App_Account:login') 
def ProfileUpdateView(request):
    profile_instance = request.user.userprofile
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        mobile = request.POST.get('mobile')
        nid = request.POST.get('nid')
        city = request.POST.get('city')
        present_address = request.POST.get('presentAddress')
        permanent_address = request.POST.get('permanentAddress')
        
        request.user.first_name = first_name
        request.user.last_name = last_name
        profile_instance.mobile = mobile
        profile_instance.nid = nid
        profile_instance.city = city
        profile_instance.present_address = present_address
        profile_instance.permanent_address = permanent_address
        
        if 'photo' in request.FILES:
            photo_file = request.FILES['photo']
            profile_instance.photo = photo_file
        request.user.save()
        profile_instance.save()
        messages.success(request,"Profile update successfully.")
        return redirect('App_Account:profile') 
    return render(request,'App_Dashboard/profile_update.html')    

@house_owner_required
def RentListView(request):
    myrent_list=House.objects.filter(owner=request.user)
    context={
        'myrent_list':myrent_list
    }
    return render(request,'App_Dashboard/rentlist.html',context)

@house_owner_required
def RentEditView(request,id):
    house = get_object_or_404(House, id=id)
    if request.method == 'POST':
        txtTitle = request.POST.get('txtTitle')
        txtCity = request.POST.get('txtCity')
        txtType = request.POST.get('txtType')
        txtBuilding = request.POST.get('txtBuilding')
        txtArea = request.POST.get('txtArea')
        txtParking = request.POST.get('txtParking')
        txtFloor = request.POST.get('txtFloor')
        txtBedroom = request.POST.get('txtBedroom')
        txtBath = request.POST.get('txtBath')
        txtAddress = request.POST.get('txtAddress')
        txtMapUrl = request.POST.get('txtMapUrl')
        txtMonthlyRent = request.POST.get('txtMonthlyRent')
        txtAdvance = request.POST.get('txtAdvance')
        txtDescription = request.POST['description']
        rentForm = request.POST.get('txtRentFrom')
        city = City.objects.get(id=txtCity)
        is_parking = True if txtParking == "1" else False  

        house.title = txtTitle
        house.city = city
        house.rent_from=rentForm
        house.address = txtAddress
        house.house_name = txtBuilding
        house.house_type = txtType
        house.house_area = txtArea
        house.description = txtDescription
        house.is_parking = is_parking
        house.total_bedrooms = txtBedroom
        house.total_bathrooms = txtBath
        house.floor_no = txtFloor
        house.map_link = txtMapUrl
        house.monthly_rent = txtMonthlyRent
        house.advacne_rent = txtAdvance

        if 'txtImages' in request.FILES:
            house.images.all().delete()
            txtImages = request.FILES.getlist('txtImages')
            for image_file_path in txtImages:
                house_image = HouseImage.objects.create(image=image_file_path)
                house.images.add(house_image)
        house.save()
        messages.success(request,"Rent post update successfully.")  
        return redirect( reverse("App_Account:editrent", args=[id]))  
    else:
        house_form = HouseForm(instance=house)
    new_cities = []
    cities = City.objects.filter(is_active=True)
    for city in cities:
        if city.id == house.city.id:
            new_cities.append({'id': city.id, 'name': city.name, 's': 'selected'})
        else:
            new_cities.append({'id': city.id, 'name': city.name, 's': ''})
    new_house_type = []
    house_type_list = list(HOUSE_TYPE_LIST)    
    for value,label in house_type_list:
        if value == house.house_type:
            new_house_type.append({'value': value, 'label': label, 's': 'selected'})
        else:
            new_house_type.append({'value': value, 'label': label, 's': ''})
    my_check=""
    if house.is_parking:
        my_check="checked"
    my_not_check=""
    if not house.is_parking:
        my_not_check="checked"
    context = {
        'cities': new_cities,
        'house':house,
        'house_form': house_form,
        'house_types': new_house_type,
        'my_not_check':my_not_check,
        'my_check':my_check,
        'current_date':date.today()
    }
    return render(request,'App_Dashboard/editrent.html',context)


@house_owner_required
def AddRentView(request):
    cities= City.objects.filter(is_active=True)
    house_type_list = list(HOUSE_TYPE_LIST)
    current_date = date.today()
    if request.method == 'POST':
        txtTitle = request.POST.get('txtTitle')
        txtCity = request.POST.get('txtCity')
        txtType = request.POST.get('txtType')
        txtBuilding = request.POST.get('txtBuilding')
        txtArea = request.POST.get('txtArea')
        txtParking = request.POST.get('txtParking')
        txtFloor = request.POST.get('txtFloor')
        txtBedroom = request.POST.get('txtBedroom')
        txtBath = request.POST.get('txtBath')
        txtAddress = request.POST.get('txtAddress')
        txtMapUrl = request.POST.get('txtMapUrl')
        txtMonthlyRent = request.POST.get('txtMonthlyRent')
        txtAdvance = request.POST.get('txtAdvance')
        rentForm = request.POST.get('txtRentFrom')
        txtDescription = request.POST['description']
        if txtParking=="1":
            txtParking=True
        else:
            txtParking=False    
        print(rentForm)
        owner = request.user
        city = City.objects.get(id=txtCity)
        house = House.objects.create(
            owner=owner,
            title=txtTitle,
            city=city,
            address=txtAddress,
            house_name=txtBuilding,
            rent_from=rentForm,
            house_type=txtType,
            house_area=txtArea,
            description=txtDescription,
            is_parking=txtParking,
            total_bedrooms=txtBedroom,
            total_bathrooms=txtBath,
            floor_no=txtFloor,
            map_link=txtMapUrl,
            monthly_rent=txtMonthlyRent,
            advacne_rent=txtAdvance
        )

        if 'txtImages' in request.FILES:
            txtImages = request.FILES.getlist('txtImages')
            print("img=1")
            for image_file_path in txtImages:
                print(image_file_path)
                house_image = HouseImage.objects.create(image=image_file_path)
                house.images.add(house_image)
        house.save()
        messages.success(request,"Rent post create successfully.")  
        return redirect("App_Account:addrent")  
    else:
        house_form = HouseForm()
    context={
        'cities':cities,
        'house_form': house_form, 
        'house_types':house_type_list,
        'current_date':current_date
    }
    return render(request,'App_Dashboard/addrent.html',context)


@house_owner_required
def RentDeleteView(request, id):
    try:
        house = get_object_or_404(House, id=id)
        if house:
            house.delete()
            messages.success(request, "Post deleted successfully.")
    except House.DoesNotExist:
        messages.info(request, "House not found.")
    return redirect("App_Account:rentlist")


@house_owner_required
def RentedListView(request):
    myrent_list=HouseRent.objects.filter(post__owner=request.user,is_paid=True)
    context={
        'myrent_list':myrent_list
    }
    return render(request,'App_Dashboard/rentedlist.html',context)    

@house_owner_required
def RentedListDetailsView(request,id):
    myrent_list=HouseRent.objects.get(id=id)
    if myrent_list.post.owner != request.user:
        return render(request, 'accessdenied.html')
    context={
        'singlerented':myrent_list
    }
    return render(request,'App_Dashboard/renteddetails.html',context)    







@admin_required
def PendingRentListView(request):
    myrent_list=House.objects.all()
    print(myrent_list)
    context={
        'myrent_list':myrent_list
    }
    return render(request,'App_Admin/pendingrentlist.html',context)
@admin_required
def PendingRentPreviewiew(request,id):
    house = get_object_or_404(House, id=id)
    house_form = HouseForm(instance=house)
    new_cities = []
    cities = City.objects.filter(is_active=True)
    for city in cities:
        if city.id == house.city.id:
            new_cities.append(city)
    new_house_type = []
    house_type_list = list(HOUSE_TYPE_LIST)    
    for value,label in house_type_list:
        if value == house.house_type:
            new_house_type.append({'value': value, 'label': label, 's': 'selected'})
    context = {
        'cities': new_cities,
        'house':house,
        'house_form': house_form,
        'house_types': new_house_type,
    }
    return render(request,'App_Admin/pendingpreview.html',context)


@admin_required
def ApprovePendingRentListView(request,id):
    try:
        house = get_object_or_404(House, id=id)
        if house:
            house.is_active=True
            house.is_reject=False
            house.save()
            messages.success(request, "Post approved successfully.")
    except House.DoesNotExist:
        messages.info(request, "Post not found.")
    return redirect("App_Account:pendingrentlist")

@admin_required
def CancelPendingRentListView(request,id):
    try:
        house = get_object_or_404(House, id=id)
        if house:
            house.is_active=False
            house.is_reject=True
            house.save()
            messages.success(request, "Post cancel successfully.")
    except House.DoesNotExist:
        messages.info(request, "Post not found.")
    return redirect("App_Account:pendingrentlist")


from django.shortcuts import render
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime, timedelta,time
from django.template.loader import get_template

@admin_required
def PurchaseReportListView(request):
    return render(request,'App_Dashboard/purchasereport.html')

@admin_required
def ReportView(request):
    fdate = request.GET.get('fromdate', '')
    tdate = request.GET.get('todate', '')
    fdate_obj = datetime.strptime(fdate, '%Y-%m-%d')
    tdate_obj = datetime.strptime(tdate, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)

    newdata = HouseRent.objects.filter(
        is_paid=True,
        created__range=[fdate_obj, tdate_obj]
    )

    # Prepare data to pass to the template
    sales_data = [
        {
            "SL": i + 1,  # Use counter variable i + 1 as SL (starts from 1)
            "Title": item.post.title,
            "HouseOwner": item.post.owner,
            "Renter": item.user,
            "PurchaseDate": item.created,
            "PayAmount": item.post.advacne_rent,
            "DueAmount": item.due_amount,
            "Status": item.is_paid
        }
        for i, item in enumerate(newdata)
    ]
    print(f"{fdate} to {tdate}")
    context = {'sales': sales_data,'daterange':f"{fdate} to {tdate}"}
    return render_to_pdf('App_Dashboard/report.html', context)

def render_to_pdf(template_src, context_dict):
    """
    Helper function to render HTML template as PDF using xhtml2pdf.
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None




@admin_required
def UserReportView(request):
    return render(request,'App_Dashboard/userreport.html')

@admin_required
def UserWiseReportView(request):
    usertype = request.GET.get('userType', '')
    if usertype=="0":
        newdata = UserProfile.objects.all()
    else:
        newdata = UserProfile.objects.filter(userType=str(usertype))

    # Prepare data
    user_data = [
        {
            "SL": i + 1,
            "Username": item.user.username,
            "Email": item.user.email,
            "City": item.city,
            "Phone": item.mobile,
            "Address": item.present_address,
            "Photo": item.photo.url if item.photo else '',  # Check if photo exists
            "Nid": item.nid,
            "UserType": item.get_user_type_display(),  # Use the custom method to get user type display name
        }
        for i, item in enumerate(newdata)
    ]

    print(user_data)
    # Set typeName based on usertype for context
    typeName = dict(USER_TYPE_LIST).get(usertype, "")

    context = {'sales': user_data, 'usertype': typeName}
    return render_to_pdf('App_Dashboard/userreportdata.html', context)

@admin_required
def ContactMessage(request):
    contacts=ContractUs.objects.all()
    print(contacts)
    context={
        'contacts':contacts
    }
    return render(request,'App_Dashboard/contact.html',context)





##RENTED USER######

@renter_required
def PurchaseListView(request):
    myrent_list=HouseRent.objects.filter(user=request.user,is_paid=True)
    context={
        'myrent_list':myrent_list
    }
    return render(request,'App_Dashboard/purchase_list.html',context)

@renter_required
def PurchaseDetailsView(request,id):
    myrent_list=HouseRent.objects.get(id=id)
    if myrent_list.user != request.user:
        return render(request, 'accessdenied.html')
    context={
        'singlerented':myrent_list
    }
    return render(request,'App_Dashboard/purchasedetails.html',context)    

