# Generated by Django 5.0.3 on 2024-04-26 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_userprofile_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='reward',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]