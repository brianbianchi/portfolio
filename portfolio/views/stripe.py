import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from ..models import StripeSession

DOMAIN = os.environ["DOMAIN_NAME"]
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]


@login_required(login_url="/login")
def checkout(request) -> HttpResponse:
    try:
        prices = stripe.Price.list(lookup_keys=["new_league"], expand=["data.product"])
        price_item = prices.data[0]

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {"price": price_item.id, "quantity": 1},
            ],
            mode="subscription",
            success_url=DOMAIN
            + reverse("create_league")
            + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=DOMAIN + reverse("home"),
        )

        StripeSession.objects.create(
            user=request.user,
            stripe_checkout_session_id=checkout_session.id,
            stripe_price_id=price_item.id,
        )

        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(e)
        return HttpResponse("Server error", status=500)


def manage_stripe(request) -> HttpResponse:
    """
    Re-directs the user to a customer portal used to manage their subscription.
    """

    stripe_checkout_session_id = request.GET.get("session_id", None)
    if not stripe_checkout_session_id:
        return HttpResponse("Server error", status=500)

    checkout_record = StripeSession.objects.filter(
        stripe_checkout_session_id=stripe_checkout_session_id
    ).first()

    checkout_session = stripe.checkout.Session.retrieve(
        checkout_record.stripe_checkout_session_id
    )

    portal_session = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=DOMAIN + reverse("view_league", args=[checkout_record.id]),
    )
    return redirect(portal_session.url, code=303)


@csrf_exempt
def stripe_webhook(request) -> HttpResponse:
    """
    Stripe sends webhook events to this endpoint.
    Webhook signature is verified and db records are updated accordingly.
    """
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    signature = request.META["HTTP_STRIPE_SIGNATURE"]
    payload = request.body

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=signature, secret=webhook_secret
        )
    except ValueError as e:
        raise ValueError(e)
    except stripe.error.SignatureVerificationError as e:
        raise stripe.error.SignatureVerificationError(e)

    _update_record(event)
    return HttpResponse(status=200)


def _update_record(webhook_event) -> None:
    """
    https://docs.stripe.com/api/events/types
    """
    data_object = webhook_event["data"]["object"]
    event_type = webhook_event["type"]

    if event_type == "checkout.session.completed":
        checkout_record = StripeSession.objects.get(
            stripe_checkout_session_id=data_object["id"]
        )
        checkout_record.stripe_customer_id = data_object["customer"]
        checkout_record.is_paid = True
        checkout_record.save()
        print("Payment succeeded")
    elif event_type == "customer.subscription.created":
        print("Subscription created")
    elif event_type == "customer.subscription.updated":
        print("Subscription updated")
    elif event_type == "customer.subscription.deleted":
        checkout_record = StripeSession.objects.get(
            stripe_customer_id=data_object["customer"]
        )
        checkout_record.is_paid = False
        checkout_record.save()
        print(f"Subscription canceled: {data_object.id}")
