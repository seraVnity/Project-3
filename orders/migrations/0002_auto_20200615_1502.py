# Generated by Django 3.0.1 on 2020-06-15 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cart',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
