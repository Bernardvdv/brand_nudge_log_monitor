from django.urls import include, path

from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.LoginPageView.as_view(), name='login'),
    path('home', views.HomePageView.as_view(), name='home'),
]
