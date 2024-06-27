from django.urls import include, path

from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.LoginPageView.as_view(), name='login'),
    path('home', views.HomePageView.as_view(), name='home'),
    path('logs', views.LogsPageView.as_view(),
         name='logs'),
    path('stats', views.StatsPageView.as_view(),
         name='stats'),
    path('category', views.CategoryPageView.as_view(),
         name='category'),
    path('retailers', views.RetailersPageView.as_view(),
         name='retailers'),
    path('cron', views.CronPageView.as_view(),
         name='cron'),
    path('exceptions', views.ExceptionPageView.as_view(),
         name='exceptions'),
    path('get_total_product_count_last_10/',
         views.HomePageView.get_total_product_count_last_10,
         name="get_total_product_count_last_10"),
    path('get_yesterday_today_imports/',
         views.HomePageView.get_yesterday_today_imports,
         name="get_yesterday_today_imports"),
    path('docs/', include('docs.urls')),
    path('classification',
         views.ClassificationPageView.as_view(),
         name="classification"),
    path('openai_classification/',
         views.ClassificationPageView.openai_classification,
         name="openai_classification"),
]
