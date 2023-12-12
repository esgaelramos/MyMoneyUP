from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import transaction
from .models import Asset, Portfolio, PortfolioAsset, CustomUser
from django.conf import settings

import pandas as pd
from Historic_Crypto import Cryptocurrencies
from Historic_Crypto import LiveCryptoData

# Create your views here.
class TrackerView(View):
    def get_available_assets(self):
        # Accedemos a la COINBASE API para obtener la lista de activos disponibles
        coin_list = Cryptocurrencies().find_crypto_pairs()
        available_assets = coin_list['id'].tolist()
        return available_assets

    def get(self, request, *args, **kwargs):
        ## assets = Asset.objects.all() Ahora la lista de activos nos la da la API, no la bd
        available_assets = self.get_available_assets()
        context={
            "available_assets": available_assets,
        }
        return render(request, "moneytracker/tracker.html", context)

    def post(self, request, *args, **kwargs):
        # Get the email and the selected assets from the form
        email = request.POST.get('email')
        selected_assets_tickers = request.POST.getlist('assets')

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
            asset_data_dict = {}
            for ticker in selected_assets_tickers:
                data = LiveCryptoData(ticker).return_data()
                data['ticker'] = ticker
                data['price'] = data['price'].astype(float).round(2)
                data.sort_values(by=['price'], inplace=True)
                asset_data_dict[ticker] = data
                

                # Debemos añadir el activo al modelo portfolio
                PortfolioAsset.objects.create(portfolio=portfolio, asset=ticker, quantity=1)
            
            
            # Send a confirmation email if the portfolio was created
            if created_portfolio:

                email_body = f'Your portfolio has been created successfully. Current Prices:\n\n'
                df = pd.DataFrame.from_dict(asset_data_dict, orient='index')
                html_table = df.to_html()


                # Agregar la información de cada activo al cuerpo del correo
                for ticker, data in asset_data_dict.items():
                    print(ticker, data)
                    email_body += f'Ticker: {ticker}, Precio: {data["price"]}\n'
                send_mail(
                    'Confirmation of Portfolio Creation',
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=True,
                    html_message = html_table
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
            print(settings.EMAIL_HOST_USER)
            return HttpResponse("Correo enviado con éxito!")

        return HttpResponse("Error: Este formulario solo acepta solicitudes POST.")
