from django.shortcuts import render

from .models import HomeNewsBadge


def home(request):
    badge = HomeNewsBadge.objects.filter(is_active=True).first()
    return render(request, "core/home.html", {"home_news_badge": badge})
