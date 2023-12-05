from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import HttpResponseNotFound

class TermsView(View):
    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, "terms/terms.html", context)
    
class Custom404View(View):
    def get(self, request, *args, **kwargs):
        html = render(request, "errors/404.html")
        return HttpResponseNotFound(html)