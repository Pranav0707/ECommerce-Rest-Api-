# Generated by Django 3.1.7 on 2022-06-02 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20220601_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='instamojo_response',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
