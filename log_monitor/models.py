from django.db import models


class Retailers(models.Model):
    proxies = [
        ("Residential", "Residential"),
        ("Non-residential", "Non-residential"),
        ("None", "None"),
    ]
    DEFAULT = "None"

    date = models.DateField()
    retailer = models.CharField(max_length=180, unique=True)
    cron_time = models.TimeField(auto_now=False, auto_now_add=False)
    retailer_url = models.CharField(max_length=180, unique=True)
    proxy_used = models.CharField(
        max_length=50,
        choices=proxies,
        default=DEFAULT
    )
    table_name = models.CharField(max_length=180, unique=False)

    class Meta:
        verbose_name_plural = "Retailers"

    def __str__(self):
        return self.retailer
