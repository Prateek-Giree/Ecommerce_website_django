# Generated by Django 4.2.18 on 2025-02-06 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0003_remove_user_address_remove_user_contactnumber_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
