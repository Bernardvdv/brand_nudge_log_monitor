from django.urls import include, path

from . import views

urlpatterns = [
    # path("accounts/", include("django.contrib.auth.urls")),
    path('', views.LoginPageView.as_view(), name='login'),
    # path('home', views.HomePageView.as_view(), name='home'),
    # path('breakdown', views.BreakdownPageView.as_view(),
    #      name='breakdown'),
    # path('ajax_get_expenses/', views.HomePageView.ajax_get_expenses,
    #      name="ajax_get_expenses"),
    # path('get_revenue_source/', views.HomePageView.get_revenue_source,
    #      name="get_revenue_source"),
]
