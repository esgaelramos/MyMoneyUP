from django.shortcuts import render
from django.views.generic import View, TemplateView

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