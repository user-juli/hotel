# Generated by Django 3.2.5 on 2021-08-23 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210807_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='adults',
            field=models.CharField(default='2021-08-23', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='children',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
