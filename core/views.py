"""Module for core views in the Django application."""

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseNotFound


class TermsView(View):
    """View for displaying the terms and conditions page."""

    def get(self, request, *args, **kwargs):
        """Handle GET request to render the terms and conditions page."""
        context = {}
        return render(request, "terms/terms.html", context)


class Custom404View(View):
    """View for displaying a custom 404 error page."""

    def get(self, request, *args, **kwargs):
        """Handle GET request to render the custom 404 error page."""
        context = {"hide_header": True, "hide_footer": True}
        html = render(request, "errors/404.html", context)
        return HttpResponseNotFound(html)
