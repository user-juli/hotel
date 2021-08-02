# Generated by Django 3.2.5 on 2021-07-17 17:17

import app.models
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.CharField(max_length=100)),
                ('numb', models.BigIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=200)),
                ('phone', models.CharField(max_length=30)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Roomtype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('people', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('price_room', models.DecimalField(decimal_places=2, max_digits=10)),
                ('beds', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('D', 'Desocupada'), ('O', 'Ocupada')], default='D', max_length=1)),
                ('description', ckeditor.fields.RichTextField()),
                ('image_header', models.ImageField(default='rooms/None/no-img.jpg', upload_to='rooms/')),
                ('url', models.SlugField(max_length=255, unique=True)),
                ('roomtype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.roomtype')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin', models.DateField()),
                ('checkout', models.DateField()),
                ('adults', models.IntegerField()),
                ('children', models.IntegerField()),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.order')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.room')),
            ],
        ),
        migrations.CreateModel(
            name='ImagesRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=app.models.upload_gallery_image)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app.room')),
            ],
        ),
    ]
