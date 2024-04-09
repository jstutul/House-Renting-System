from django.shortcuts import render,redirect
from App_Account.models import *
from App_Rental.models import *
from App_Rental.forms import CommentForm
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
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



def checkout(request):
    if request.method == 'POST':
        stripe_token = request.POST['stripeToken']
        try:
            charge = stripe.Charge.create(
                amount=1000,  # Amount in cents
                currency='usd',
                description='Example charge',
                source=stripe_token,
            )
            # Payment successful
            return render(request, 'success.html')
        except stripe.error.CardError as e:
            # Payment failed
            return render(request, 'failure.html', {'error': e.error.message})
    else:
        return render(request, 'checkout.html')