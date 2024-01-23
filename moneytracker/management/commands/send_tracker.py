"""
Script to send tracker emails of the day.

This script identifies the users that want to receive their tracker email today
and then send it to them with the Assets and DailyAssetInfo they have in their
portfolio.

Example:
    python manage.py send_tracker
"""

import datetime
from datetime import timedelta
from typing import Any

from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from moneytracker.models import (
    CustomUser, DailyAssetInfo, Performance, Portfolio, PortfolioAsset
)


class Command(BaseCommand):
    """Django management command to send tracker emails to users."""

    def get_today_users(self) -> list:
        """
        Get a list of users who have opted to receive tracker emails today.

        Users are selected based on whether their preferred email frequency
        matches the current day.

        Returns:
            list: List of users who should receive an email today.
        """
        today = datetime.date.today()
        weekday_today = today.strftime('%A')
        date_14_days_ago = today - timedelta(days=14)
        date_a_month_ago = today - timedelta(days=28)
        today_users = []

        # Filter performances by 'Daily' periodicity
        daily_performances = Performance.objects.filter(Q(periodicity='Daily'))

        # Filter performances by weekday_today and 'Weekly' periodicity
        # or 'Monthly' periodicity with last_time_sent <= date_a_month_ago
        # Or by 'Biweekly' periodicity with last_time_sent <= date_14_days_ago
        weekly_monthly_biweekly_performances = Performance.objects.filter(
            Q(days_to_send_email=weekday_today) & (
                Q(periodicity='Weekly')
                | Q(periodicity='Monthly', last_time_sent__lte=date_a_month_ago)  # noqa: E501
                | Q(periodicity='Biweekly', last_time_sent__lte=date_14_days_ago)  # noqa: E501
            )
        )

        # Combine the results of both queries
        performances = daily_performances | weekly_monthly_biweekly_performances  # noqa: E501

        for performance in performances:
            today_users.append(performance.user)
        return today_users

    def get_user_portfolios_assets(self, user: CustomUser) -> list:
        """
        Retrieve all assets in a user's portfolio.

        Args:
            user (CustomUser): User object to find the portfolio assets for.

        Returns:
            list: List of PortfolioAsset objects for the given user.
        """
        portfolio = Portfolio.objects.get(user=user)
        portfolios_assets = PortfolioAsset.objects.filter(portfolio=portfolio)
        return portfolios_assets

    def get_user_assets(self, user: CustomUser) -> list:
        """
        Extract the assets for a given user from their portfolio assets.

        Args:
            user (CustomUser): User object to gather assets for.

        Returns:
            list: List of Asset objects associated with the user.
        """
        portfolios_assets = self.get_user_portfolios_assets(user=user)
        assets = []
        for portfolio_asset in portfolios_assets:
            assets.append(portfolio_asset.asset)
        return assets

    def get_asset_info(self, asset) -> DailyAssetInfo:
        """
        Fetch the latest DailyAssetInfo for a given asset.

        Args:
            asset: The Asset object to fetch information for.

        Returns:
            DailyAssetInfo: The most recent DailyAssetInfo object for the given
            asset.
        """
        return DailyAssetInfo.objects.filter(asset=asset).latest('timestamp')

    def body_email(self, user) -> str:
        """
        Construct the body of the email to be sent to the user.

        This includes information about each asset owned by the user.

        Args:
            user: The user object to construct the email body for.

        Returns:
            str: The body of the email.
        """
        body = ''
        user_assets = self.get_user_assets(user)
        for asset in user_assets:
            asset_info = self.get_asset_info(asset)
            body += f'{asset_info}\n\n'
        return body

    def handle(self, *args: Any, **options: Any):
        """
        Entry point for the Django management command.

        It sends emails containing financial tracker information to users based
        on their email preferences.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.
        """
        today_users = self.get_today_users()
        print(today_users)
        for user in today_users:
            email_body = self.body_email(user)
            send_mail(subject='Your tracker information is here!',
                      message=email_body,
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[user.user.email],
                      fail_silently=True)
