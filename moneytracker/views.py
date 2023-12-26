from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import transaction
from .models import Asset, Portfolio, PortfolioAsset, CustomUser, AssetPrice
from django.conf import settings

from Historic_Crypto import LiveCryptoData
from requests.exceptions import RequestException

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
            asset_info_list = []
            for asset_id in selected_asset_ids:
                asset = Asset.objects.get(id=asset_id)
                PortfolioAsset.objects.create(portfolio=portfolio, asset=asset, quantity=1)

                # we fetch Coinbase API to get asset info and append into the list
                try:
                    crypto_data = LiveCryptoData(f'{asset.symbol}').return_data()
                # Usamos .iloc[-1] para seleccionar el último elemento (la última fila) de un DataFrame de Pandas,
                # En este caso, nos da acceso al precio más reciente del ticker correspondiente
                    AssetPrice.objects.create(asset=asset, price=round(float(current_price), 2))
                    current_price = crypto_data['price'].iloc[-1]
                    asset_info_list.append(f'{asset.symbol}: {round(float(current_price), 2)}$')
                except RequestException as e:
                    print(f"Error fetching data for {asset.symbol}: {e}")
                    continue



            
            # Send a confirmation email if the portfolio was created
            if created_portfolio:
                message_body = f'Your portfolio has been created successfully.\n\nCheck real-time info about your favorite Crypto!:\n'
                message_body += '\n'.join(asset_info_list)
                send_mail(
                    'Confirmation of Portfolio Creation',
                    message_body,
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
