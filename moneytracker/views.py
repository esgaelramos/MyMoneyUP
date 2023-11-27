from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.core.mail import send_mail
from django.http import HttpResponse
# Create your views here.
class Tracker(View):
    def get(self, request, *args, **kwargs):
        context={
        }
        return render(request, "moneytracker/tracker.html", context)


class About(View):
    def get(self, request, *args, **kwargs):
        context={
        }
        return render(request, "moneytracker/about.html", context)
    

class Contact(View):
    def get(self, request, *args, **kwargs):
        context={
        }
        return render(request, "moneytracker/contact.html", context)
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            to_email = request.POST.get('to_email')
            
            send_mail(subject, message, 'tuemail@gmail.com', [to_email])
            return HttpResponse("Correo enviado con éxito!")

        return HttpResponse("Error: Este formulario solo acepta solicitudes POST.")


