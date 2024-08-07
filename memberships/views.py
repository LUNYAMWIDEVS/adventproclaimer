from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse

from .models import Membership, UserMembership, Subscription

import paypalrestsdk

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None

def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None

def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
        membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None

@login_required
def profile_view(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)
    context = {
        'user_membership': user_membership,
        'user_subscription': user_subscription
    }
    return render(request, "memberships/profile.html", context)

class MembershipSelectView(LoginRequiredMixin, ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self, request, **kwargs):
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)
        selected_membership_type = request.POST.get('membership_type')

        selected_membership = Membership.objects.get(
            membership_type=selected_membership_type)

        if user_membership.membership == selected_membership:
            if user_subscription is not None:
                messages.info(request, """You already have this membership. Your
                              next payment is due {}""".format('get this value from PayPal'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # assign to the session
        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('memberships:payment'))

@login_required
def PaymentView(request):
    user_membership = get_user_membership(request)
    try:
        selected_membership = get_selected_membership(request)
    except:
        return redirect(reverse("memberships:select"))

    if request.method == "POST":
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('memberships:update-transactions')),
                "cancel_url": request.build_absolute_uri(reverse('memberships:select'))},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": selected_membership.membership_type,
                        "sku": "item",
                        "price": str(selected_membership.price),
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": str(selected_membership.price),
                    "currency": "USD"},
                "description": f"Membership subscription for {selected_membership.membership_type}"}]})

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        else:
            messages.error(request, "An error occurred while creating PayPal payment")
            return redirect(reverse('memberships:select'))

    context = {
        'selected_membership': selected_membership
    }

    return render(request, "memberships/membership_payment.html", context)

@login_required
def updateTransactionRecords(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        user_membership = get_user_membership(request)
        selected_membership = get_selected_membership(request)
        user_membership.membership = selected_membership
        user_membership.save()

        sub, created = Subscription.objects.get_or_create(
            user_membership=user_membership)
        sub.paypal_subscription_id = payment_id
        sub.active = True
        sub.save()

        try:
            del request.session['selected_membership_type']
        except:
            pass

        messages.info(request, f'Successfully created {selected_membership} membership')
        return redirect(reverse('memberships:select'))
    else:
        messages.error(request, "Payment execution failed")
        return redirect(reverse('memberships:select'))

@login_required
def cancelSubscription(request):
    user_sub = get_user_subscription(request)

    if not user_sub.active:
        messages.info(request, "You don't have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    agreement = paypalrestsdk.BillingAgreement.find(user_sub.paypal_subscription_id)
    if agreement.cancel({"note": "Cancel the subscription"}):
        user_sub.active = False
        user_sub.save()

        free_membership = Membership.objects.get(membership_type='Free')
        user_membership = get_user_membership(request)
        user_membership.membership = free_membership
        user_membership.save()

        messages.info(request, "Successfully cancelled membership. We have sent an email")
        return redirect(reverse('memberships:select'))
    else:
        messages.error(request, "An error occurred while cancelling the subscription")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
