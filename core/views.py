from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

class TermsView(View):
    def get(self, request, *args, **kwargs):
        context = {
            
        }
        return render(request, "terms/terms.html", context)