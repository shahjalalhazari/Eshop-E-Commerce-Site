from django.shortcuts import render, redirect, HttpResponseRedirect
from sslcommerz_python.payment import SSLCSession
import requests, socket
from decimal import Decimal
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Order.models import Order,  Cart
from .models import BillingAddress
from .forms import BillingAddressForm


# CHECKOUT VIEW
@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if request.method == "POST":
        form = BillingAddressForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingAddressForm(instance=saved_address)
            messages.success(request, "Address Saved!")
    else:
        form = BillingAddressForm(instance=saved_address)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()
    return render(request, 'Payment/checkout.html', {'form': form, 'order_items': order_items, 'order_total': order_total, 'saved_address': saved_address})


# PAYMENT VIEW
@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.warning(request, "Please complete shipping address.")
        return redirect("payment:checkout")
    if not request.user.profile.is_fully_filled():
        messages.warning(request, "Please complete profile details!")
        return redirect("account:profile")
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id='eshop5f7d8f3d714de', sslc_store_pass='eshop5f7d8f3d714de@ssl')
    status_url = request.build_absolute_uri(reverse("payment:status"))
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    total_items = order_qs[0].orderitems.count()
    total_amount = order_qs[0].get_totals()
    mypayment.set_product_integration(total_amount=Decimal(total_amount), currency='BDT', product_category='Mixed', product_name=order_items, num_of_item=total_items, shipping_method='Courier', product_profile='None')
    #user info
    user = request.user
    name, email = user.profile.fullname, user.email,
    address, address2 = user.profile.address_1, user.profile.address_2,
    city, postcode, country = user.profile.city, user.profile.zipcode, user.profile.country,
    phone = user.profile.phone
    mypayment.set_customer_info(name=name, email=email, address1=address, address2=address2, city=city, postcode=postcode, country=country, phone=phone)
    #shipping address info
    ba_name = saved_address.name
    ba_address = saved_address.address
    ba_city = saved_address.city
    ba_zip_code = saved_address.zip_code
    ba_country = saved_address.country
    mypayment.set_shipping_info(shipping_to=ba_name, address=ba_address, city=ba_city, postcode=ba_zip_code, country=ba_country)
    response_data = mypayment.init_payment()
    return redirect(response_data['GatewayPageURL'])


# STATUS VIEW
@csrf_exempt
def status(request):
    if request.method == "POST" or request.method == "post":
        payment_data = request.POST
        status = payment_data['status']
        bank_tran_id = payment_data['bank_tran_id']
        if status == "VALID":
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request, "Your payment has been completed successfully!!! Page will be redirected after 5sec")
            return HttpResponseRedirect(reverse("payment:purchased", kwargs={'val_id': val_id, 'tran_id': tran_id}))
        elif status == "FAILED":
            messages.warning(request, "Payment Failed. Please try again! Page will be redirected after 5sec")
    return render(request, "Payment/status.html", {})


# PURCHASED VIEW
@login_required
def purchased(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    order.ordered = True
    order.orderId = tran_id
    order.paymentId = val_id
    order.save()
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
        return HttpResponseRedirect(reverse("store:home"))


# PAYMENT VIEW
@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {'orders': orders}
    except:
        messages.warning(request, "you don't have any orders!")
        return redirect("store:home")
    return render(request, "Payment/order.html", context)