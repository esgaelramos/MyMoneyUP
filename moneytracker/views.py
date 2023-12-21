"""Module for moneytracker views in the Django application."""

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User

from .models import Asset, Portfolio, PortfolioAsset, CustomUser


class TrackerView(View):
    """View for handling asset tracking functionality."""

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to render the asset tracker page.

        This method retrieves all available assets from the database and
        displays them on the asset tracker page, allowing the user to view
        the list of assets.
        """
        assets = Asset.objects.all()
        context = {
            "assets": assets,
        }
        return render(request, "moneytracker/tracker.html", context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to process asset tracking data.

        This method processes the submitted data from the asset tracking form.
        It involves creating or updating user data, creating a portfolio
        for the user if it doesn't exist, and adding selected assets to the
        user's portfolio. Additionally, it sends a confirmation email if a
        new portfolio is created.
        """
        # Get the email and the selected assets from the form
        email = request.POST.get('email')
        selected_asset_ids = request.POST.getlist('assets')

        # Begin an atomic transaction to ensure data integrity
        with transaction.atomic():
            # Create user if it doesn't exist and associate with a CustomUser
            user, created_user = User.objects.get_or_create(email=email)
            if created_user:
                user.username = user.email  # or any logic to assign a username
                user.set_unusable_password()  # util if the user can't auth
                user.save()

            custom_user, _ = CustomUser.objects.get_or_create(user=user)

            # Create a portfolio for the CustomUser if it doesn't exist
            portfolio, created_portfolio = \
                Portfolio.objects.get_or_create(user=custom_user)

            # Add the selected assets to the portfolio
            for asset_id in selected_asset_ids:
                asset = Asset.objects.get(id=asset_id)
                PortfolioAsset.objects.\
                    create(portfolio=portfolio, asset=asset, quantity=1)

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
    """View for displaying the about page of app."""

    def get(self, request, *args, **kwargs):
        """Handle GET request to render the about page."""
        context = {}
        return render(request, "moneytracker/about.html", context)


class ContactView(View):
    """View for handling contact page and functionality."""

    def get(self, request, *args, **kwargs):
        """Handle GET request to render the contact page."""
        context = {}
        return render(request, "moneytracker/contact.html", context)

    def post(self, request, *args, **kwargs):
        """Handle POST request to send a contact email."""
        if request.method == 'POST':
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            to_email = request.POST.get('to_email')

            send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
            # TODO: EDIT THIS MANAGE OF CONTACT!
            # (DONT USE HttpResponse, BETTER USE REDIRECT, NOT?)
            return HttpResponse("Mail Sent Successfully!")

        return HttpResponse("Error: This form accepts POST requests only?")
