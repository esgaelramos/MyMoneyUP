from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context={
        }
        return render(request, "core/index.html", context)