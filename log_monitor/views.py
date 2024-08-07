import json
import re

import openai
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from .forms import LoginForm
from .helpers import create_db_con
from .models import Retailers


class LoginPageView(View):
    template_name = 'log_monitor/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Login failed!'
        return render(request, self.template_name,
                      context={'form': form, 'message': message})


class HomePageView(TemplateView):
    template_name = 'log_monitor/main.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cursor = create_db_con()

        retailer_count_query = """
                                SELECT COUNT(DISTINCT retailer) 
                                FROM public.statistics;
                                """
        all_products_query = """
                                SELECT SUM(CAST (itemcount AS INTEGER)) 
                                FROM public.statistics 
                                WHERE created = current_date
                                """
        error_count_today_query = """
                                SELECT count(message) 
                                FROM public.log 
                                WHERE created::date = now()::date;
                                """
        stats_query = """
                        SELECT created, retailer, itemcount, "itemCountYesterday", expectedlinks, navigationlinks,
                        duration 
                        FROM statistics 
                        WHERE created = current_date
                        """

        cursor.execute(retailer_count_query)
        retailer_records = cursor.fetchall()

        cursor.execute(all_products_query)
        all_records_count = cursor.fetchall()

        cursor.execute(error_count_today_query)
        today_error_count = cursor.fetchall()

        cursor.execute(stats_query)
        stats_records = cursor.fetchall()

        context['retailer_info'] = Utils.get_retailers(self)
        context['retailer_count'] = retailer_records[0][0]
        context['all_records_count'] = all_records_count[0][0]
        context['today_error_count'] = today_error_count[0][0]
        context['stats_records'] = stats_records
        return context

    def get_total_product_count_last_10(request):
        last_10_count_products = """
                SELECT 
                created, SUM(CAST (itemcount AS INTEGER))
                FROM public.statistics
                WHERE created > current_date - interval '10' day 
                GROUP BY created;
                """
        cursor = create_db_con()
        cursor.execute(last_10_count_products)
        product_count_last_10_records = cursor.fetchall()
        months = []
        count = []
        for x, y in product_count_last_10_records:
            months.append(x)
            count.append(y)
        data = {
            'months': months,
            'label': count,
        }

        return JsonResponse(data)

    def get_yesterday_today_imports(request):
        yesterday_today_imports = """
                SELECT 
                retailer, itemcount, "itemCountYesterday" 
                FROM statistics 
                WHERE created = current_date
                """

        cursor = create_db_con()
        cursor.execute(yesterday_today_imports)
        product_count_last_10_records = cursor.fetchall()

        retailer = []
        today = []
        yesterday = []
        for y in product_count_last_10_records:
            if y[0] not in retailer:
                retailer.append(y[0])
                today.append(y[1])
                yesterday.append(y[2])

        data = {
            'retailer': retailer,
            'today': today,
            'yesterday': yesterday
        }
        return JsonResponse(data)


class LogsPageView(TemplateView):
    template_name = 'log_monitor/logs.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        logs_query = """
        SELECT 
        created, name, level, message, function, lineno 
        FROM public.log 
        ORDER by created DESC LIMIT 100;
        """
        cursor = create_db_con()
        cursor.execute(logs_query)
        logs_last_100 = cursor.fetchall()

        context['logs_last_100'] = logs_last_100
        context['retailer_info'] = Utils.get_retailers(self)
        return context


class StatsPageView(TemplateView):
    template_name = 'log_monitor/stats.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stats_query = """
        SELECT  
        created, retailer, itemcount, "itemCountYesterday", expectedlinks, navigationlinks, duration 
        FROM
        public.statistics
        ORDER by created DESC LIMIT 100;
        """

        cursor = create_db_con()
        cursor.execute(stats_query)
        stats_limit_100 = cursor.fetchall()

        context['retailer_info'] = Utils.get_retailers(self)
        context['stats_limit_100'] = stats_limit_100
        return context


class CronPageView(TemplateView):
    template_name = 'log_monitor/cron.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cron_query = """
                    SELECT
                    date, line 
                    FROM public.cron_logs 
                    LIMIT 100;
                    """

        cursor = create_db_con()
        cursor.execute(cron_query)
        cron_limit_100 = cursor.fetchall()

        context['retailer_info'] = Utils.get_retailers(self)
        context['cron_limit_100'] = cron_limit_100
        return context


class RetailersPageView(TemplateView):
    template_name = 'log_monitor/retailers.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_retailers(self):
        retailers = Retailers.objects.all()
        return retailers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_retailers = self.get_retailers()
        context['retailer_info'] = Utils.get_retailers(self)
        context['retailers_detail'] = get_retailers
        return context


class CategoryPageView(TemplateView):
    template_name = 'log_monitor/category.html'

    def get(self, request):
        retailer = self.request.GET.get('c')

        yesterday_query = """
        SELECT
        category, count(category)
        FROM %s 
        WHERE date = current_date - 1
        GROUP BY category;
        """

        todays_query = """
        SELECT
        category, count(category)
        FROM %s 
        WHERE date = current_date
        GROUP BY category;
        """

        cursor = create_db_con()
        try:
            cursor.execute(yesterday_query % retailer)
            cat_yesterday = cursor.fetchall()
        except:
            cat_yesterday = None
        try:
            cursor.execute(todays_query % retailer)
            cat_today = cursor.fetchall()
        except:
            cat_today = None

        if cat_yesterday and cat_today:
            result = []
            for item1, item2 in zip(cat_today, cat_yesterday):
                if item1[0] == item2[0]:
                    variance = self.get_percentage_diff(item2[1], item1[1])
                    result.append([item1[0], item1[1], item2[1], variance])
        else:
            result = None

        retailer_info = Utils.get_retailers(self)
        return render(request, self.template_name, context={"cat_counts": result,
                                                            "retailer_info": retailer_info,
                                                            "retailer": retailer})

    def get_percentage_diff(self, previous, current):
        try:
            percentage = round(abs(previous - current) / max(previous, current) * 100, 2)
        except ZeroDivisionError:
            percentage = float('inf')
        return percentage


class Utils:
    def get_retailers(self):
        retailer_info = Retailers.objects.values_list('retailer', 'table_name')
        return retailer_info


class ExceptionPageView(TemplateView):
    template_name = 'log_monitor/exception_logs.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exception_logs_query = """
        SELECT 
        created, name, url, message 
        FROM public.exception_logs
        ORDER by created DESC LIMIT 1500;
        """

        cursor = create_db_con()
        cursor.execute(exception_logs_query)
        exception_logs = cursor.fetchall()

        context['exception_logs'] = exception_logs
        return context
