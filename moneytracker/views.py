from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import transaction
from .models import Asset, Portfolio, PortfolioAsset, CustomUser
from django.conf import settings

# Create your views here.
class TrackerView(View):
    def get(self, request, *args, **kwargs):
        assets = Asset.objects.all()
        context={
            "assets": assets,
        }
        return render(request, "moneytracker/tracker.html", context)

    def post(self, request, *args, **kwargs):
        # Get the email and the selected assets from the form
        email = request.POST.get('email')
        selected_asset_ids = request.POST.getlist('assets')

        # Begin an atomic transaction to ensure data integrity
        with transaction.atomic():
            # Create a user if it doesn't exist and associate it with a CustomUser
            user, created_user = User.objects.get_or_create(email=email)
            if created_user:
                user.username = user.email  # or any logic to assign a username
                user.set_unusable_password()  # If you don't plan for the user to authenticate with a password
                user.save()

            custom_user, _ = CustomUser.objects.get_or_create(user=user)

            # Create a portfolio for the CustomUser if it doesn't exist
            portfolio, created_portfolio = Portfolio.objects.get_or_create(user=custom_user)

            # Add the selected assets to the portfolio
            for asset_id in selected_asset_ids:
                asset = Asset.objects.get(id=asset_id)
                PortfolioAsset.objects.create(portfolio=portfolio, asset=asset, quantity=1)
            
            # Send a confirmation email if the portfolio was created
            if created_portfolio:
                send_mail(
                    'Confirmation of Portfolio Creation',
                    'Your portfolio has been created successfully.',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=True,
                )

        return redirect('moneytracker:about')


class AboutView(View):
    def get(self, request, *args, **kwargs):
        context={
        }
        return render(request, "moneytracker/about.html", context)


class ContactView(View):
    def get(self, request, *args, **kwargs):
        context={
        }
        return render(request, "moneytracker/contact.html", context)
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            to_email = request.POST.get('to_email')
            
            send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
            # TODO: EDIT THIS MANAGE OF CONTACT! (DONT USE HttpResponse, BETTER USE REDIRECT, NOT?)
            return HttpResponse("Correo enviado con éxito!")

        return HttpResponse("Error: Este formulario solo acepta solicitudes POST.")
