# Generated by Django 3.1.7 on 2022-06-02 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20220602_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='instamojo_response',
            field=models.TextField(blank=True, null=True),
        ),
    ]
