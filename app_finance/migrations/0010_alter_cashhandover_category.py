# Generated by Django 4.1.5 on 2023-02-04 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_finance', '0009_alter_depositsreturned_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashhandover',
            name='category',
            field=models.CharField(choices=[('BK', 'Bank'), ('IP', 'In Person')], default='IP', max_length=2),
        ),
    ]
