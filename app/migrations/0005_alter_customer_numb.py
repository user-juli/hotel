# Generated by Django 3.2.5 on 2021-08-02 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_customer_numb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='numb',
            field=models.IntegerField(),
        ),
    ]
