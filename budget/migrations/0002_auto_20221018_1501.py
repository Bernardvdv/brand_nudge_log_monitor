# Generated by Django 3.1.14 on 2022-10-18 15:01

import datetime

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('currency', models.CharField(max_length=10, unique=True)),
                ('country', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('person', models.CharField(max_length=180)),
                ('income_year', models.CharField(max_length=180)),
                ('income_month', models.CharField(max_length=180)),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=180, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='items',
            name='category',
            field=models.CharField(choices=[('Home', 'Home'),
                                            ('School', 'School'),
                                            ('Utility', 'Utilities'),
                                            ('Groceries', 'Groceries'),
                                            ('Data', 'Data'),
                                            ('Subscriptions',
                                             'Subscriptions'),
                                            ('Car', 'Car'),
                                            ('Other', 'Other')],
                                   default='Home', max_length=20),
        ),
        migrations.AddField(
            model_name='items',
            name='payment_date',
            field=models.DateField(default=datetime.datetime.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='items',
            name='person',
            field=models.CharField(choices=[('Bernard', 'Bernard'),
                                            ('Tania', 'Tania')],
                                   default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='items',
            name='month',
            field=models.ForeignKey(default=1, on_delete=django.db.models.
                                    deletion.CASCADE, to='budget.period'),
            preserve_default=False,
        ),
    ]
