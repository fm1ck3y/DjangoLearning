# Generated by Django 4.1.2 on 2022-10-04 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_stock_ticker'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]