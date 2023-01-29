# from .models import Period
#
#
# def get_selected_month(pk):
#     """
#     Helper to return the current selected period
#     :param pk: Primary key for the month
#     :return: Current month
#     """
#     count_months = Period.objects.all()
#     if count_months and pk is not None:
#         selected_month = Period.objects.get(pk=pk)
#         return selected_month
#     # FIXME: Return something better here if pk
#     #  does not exist as a get parameter
#     return
#
#
# def get_months():
#     """
#     Helper to get all months to allow the user to select the period
#     :return: All months queryset
#     """
#     months = Period.objects.all()
#     return months
#
#
# def get_month_param(request):
#     """
#     Helper to get the get paramter from the URL
#     :return: Month ID as primary key
#     """
#     month_id = request.GET.get('month')
#     return month_id
