# Generated by Django 3.0.1 on 2020-06-15 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_topping_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='topping',
            name='name',
            field=models.CharField(max_length=64, null=True),
        ),
    ]