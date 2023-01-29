from django.contrib import admin

# from .models import BaseConfig, Category, Income, Items, Period


class ItemsAdmin(admin.ModelAdmin):
    list_filter = ('month',)
    save_as = True


# admin.site.register(Income)
# admin.site.register(Items, ItemsAdmin)
# admin.site.register(BaseConfig)
# admin.site.register(Period)
# admin.site.register(Category)
