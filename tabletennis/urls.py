"""tabletennis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers

from league.views import HomeView, MainView, PlayerViewSet, LeagueViewSet, MatchViewSet, SetViewSet, RoundViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'players', PlayerViewSet)
router.register(r'leagues', LeagueViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'sets', SetViewSet)
router.register(r'rounds', RoundViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    #url(r'^$', MainView.as_view(), name='main'),
    url(r'^league/', include('league.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
