from django.shortcuts import render,redirect,HttpResponse
from App_Account.models import *
from App_Rental.models import *
from App_Rental.forms import CommentForm
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
import stripe
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal,InvalidOperation
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY
def Home(request):
    rentpost=House.objects.filter(is_active=True,is_rented=False)
    userlist=UserProfile.objects.all()
    context={
        'toppost':rentpost[:6],
        'totalrent':rentpost.count(),
        'houseowner':userlist.filter(userType="1").count(),
        'renter':userlist.filter(userType="2").count()
    }
    return render(request,'index.html',context)

@login_required(login_url='App_Account:login')
def Details(request,id):
    try:
        singlepost=House.objects.get(id=id)
        relatedpost = House.objects.filter(city=singlepost.city).exclude(id=id)[:5]
        house_type_list = list(HOUSE_TYPE_LIST)  
        houseType=""  
        for value,label in house_type_list:
            if value == singlepost.house_type:
                houseType=label
        comments = HouseComment.objects.filter(post=singlepost, reply=None).order_by('-id')
        if request.method=="POST":
            comment_form =CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = comment_form.cleaned_data.get('content')
                reply_id = request.POST.get('comment_id')
                comment_qs = None
                if reply_id:
                    comment_qs = HouseComment.objects.get(id=reply_id)
                comment = HouseComment.objects.create(post=singlepost,user=request.user,content=content,reply=comment_qs)
                comment.save()
        else:
            comment_form = CommentForm()    
               
    except House.DoesNotExist:
        return redirect("home")
    contex={
            'rent':singlepost,
            'houseType':houseType,
            'relatedpost':relatedpost,
            'comments': comments,
            'comment_form': comment_form,
        }
    if request.is_ajax():
        html = render_to_string('comment_section.html', contex, request=request)
        return JsonResponse({'form': html}) 
    return render(request,'details.html',contex)





def create_checkout_session(request,id):
    house=House.objects.get(id=id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': house.title,
                    },
                    'unit_amount': int(house.advacne_rent)*100,  # Amount in cents
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success'))+  f'?session_id={{CHECKOUT_SESSION_ID}}',
        cancel_url=request.build_absolute_uri(reverse('cancel')),
    )
    order=HouseRent.objects.create(
        post=house,
        user = request.user,
        transaction_id =session.id
    )
    order.save()
    return redirect(session.url)

def success(request):
    transaction_id = request.GET.get('session_id')
    if transaction_id:
        try:
            order = HouseRent.objects.get(transaction_id=transaction_id)
            order.is_paid = True
            order.save()

            house= House.objects.get(id=order.post.id)

            if not house.is_rented:
                house.is_rented=True
                house.save()
                mail_subject='EasyRent Order Confirmation'
                message=render_to_string('orderconfirmation.html',{
                    'user': request.user,
                    'house': house,
                    'order':order,
                })
                to_email = request.user.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
            context={
                'order':order,

            }
            return render(request, 'success.html',context)
        except HouseRent.DoesNotExist:
            return HttpResponse("Order not found.")
    else:
        return HttpResponse("Transaction ID not provided.")
def cancel(request):
    return render(request, 'cancel.html')


def RentPost(request):
    if request.method == 'GET':
        txtSearch = request.GET.get('txtSearch','')
        txtCity = request.GET.get('txtCity','0')
        txtType = request.GET.get('txtType','0')
        txtMin = request.GET.get('txtMin',0)
        txtMax = request.GET.get('txtMax',0)

        try:
            txtMin_decimal = Decimal(txtMin)
        except (InvalidOperation, ValueError):
            txtMin_decimal = Decimal(0)

        try:
            txtMax_decimal = Decimal(txtMax)
        except (InvalidOperation, ValueError):
            txtMax_decimal = Decimal(0)

        rentpost = House.objects.filter(is_active=True, is_rented=False)

        if txtSearch:
            rentpost = rentpost.filter(title__icontains=txtSearch)

        if txtCity and txtCity != '0':
            rentpost = rentpost.filter(city=txtCity)

        if txtType and txtType != '0':
            rentpost = rentpost.filter(house_type=txtType)

        if txtMin_decimal!=0:
            print(txtMin_decimal)
            rentpost = rentpost.filter(monthly_rent__gte=txtMin_decimal)

        if txtMax_decimal!=0:
            rentpost = rentpost.filter(monthly_rent__lte=txtMax_decimal)

        post_count=rentpost.count()
        paginator =Paginator(rentpost,1)
        page = request.GET.get('page')
        paged_rents = paginator.get_page(page)

        cities = City.objects.all()
        new_cities=[]
        for city in cities:
            if int(city.id) == int(txtCity):
                new_cities.append({'id': city.id, 'name': city.name, 's': 'selected'})
            else:
                new_cities.append({'id': city.id, 'name': city.name, 's': ''})
        new_house_type = []
        house_type_list = list(HOUSE_TYPE_LIST)    
        for value,label in house_type_list:
            if value == txtType:
                new_house_type.append({'value': value, 'label': label, 's': 'selected'})
            else:
                new_house_type.append({'value': value, 'label': label, 's': ''})
        print(new_house_type)

    context={
        'rentpost':paged_rents,
        'cities':new_cities,
        'house_types':new_house_type,
        'post_count':post_count
    }
    return render(request,'post.html',context)

def ContactView(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        about=request.POST.get("about")
        ContractUs.objects.create(
            name=name,
            email=email,
            message=about
        ).save()
        messages.success(request,"your message is accepted ,wait for reply")
        return redirect('contact')
    return render(request,'contact.html')



def FaqView(request):
    return render(request,'faq.html')

def AboutView(request):
    return render(request,'about.html')
