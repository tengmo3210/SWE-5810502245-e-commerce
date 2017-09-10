from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
@login_required(login_url='/accounts/login/')
def checkout(request):
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    customer_id = request.user.userstripe.stripe_id

    if request.method == "POST":
        token = request.POST['stripeToken']
        try:
            customer = stripe.Customer.retrieve(customer_id)
            customer.sources.create(source= token )
            charge = stripe.Charge.create(
                amount=1000, ##Amount in cent
                currency="usd",
                customer = customer,
                description="Example charge"
            )
        except stripe.error.CardError as e:
            pass

    context = {'publishKey' : publishKey}
    template = 'checkout.html'
    return render(request,template,context)
