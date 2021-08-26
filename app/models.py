from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.text  import slugify
from ckeditor.fields import RichTextField

class Customer(models.Model):
    type_id = models.CharField(max_length = 100)
    numb = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 120)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length = 30)

    def __str__(self):
        return self.name

class Roomtype(models.Model):
    name = models.CharField(max_length = 120)
    people = models.IntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    class Status(models.TextChoices):
        DESOCUPADA = 'D', _('Desocupada')
        OCUPADA = 'O', _('Ocupada')
    name = models.CharField(max_length=120)
    roomtype = models.ForeignKey(Roomtype,on_delete=models.CASCADE,)
    price_room = models.DecimalField(max_digits=10, decimal_places=2)
    beds = models.CharField(max_length=100)
    status = models.CharField(max_length=1,choices=Status.choices,default=Status.DESOCUPADA,)
    description = RichTextField()
    image_header = models.ImageField(upload_to='rooms/', default = 'rooms/None/no-img.jpg')
    url = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.url = slugify(self.name)
        super(Room, self).save(*args, **kwargs)

    @property
    def imageURL(self):
        try:
            url = self.image_header.url
        except:
            url = ''
        return url

def upload_gallery_image(instance, filename):
    return f"rooms/{instance.room.name}/{filename}"

class ImagesRoom(models.Model):
    image = models.ImageField(upload_to=upload_gallery_image)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{0}" width="150" height="150" />'.format(self.image.url))
        else:
            return '(No image)'

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    """@property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.quantity > 0:
                shipping = True
        return shipping"""

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.room.price_room * self.quantity
        return total

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    checkin = models.CharField(max_length=100)
    checkout = models.CharField(max_length=100)
    adults = models.CharField(max_length=100)
    children = models.CharField(max_length=100, null=True)
