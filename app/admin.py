from django.contrib import admin
from . models import Customer,Roomtype,Room,Reservation,ImagesRoom,OrderItem,Order

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','type_id', 'numb', 'name', 'last_name', 'user', 'email')

@admin.register(Roomtype)
class RoomtypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'people')

class ImageInline(admin.TabularInline):
    model = ImagesRoom
    readonly_fields = ('image_preview',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id','name','roomtype','price_room','beds','description','image_header','status')
    inlines = [
        ImageInline
    ]

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('url', )
        form = super(RoomAdmin, self).get_form(request, obj, **kwargs)
        return form

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','customer','date_ordered','complete','transaction_id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','room','order','quantity','date_added')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'checkin', 'checkout', 'customer', 'order', 'adults', 'children')
