from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from django.views.generic import TemplateView,DetailView,ListView,CreateView
from .utils import cookieCart, cartData, guestOrder
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta

class HomeView(TemplateView):
    template_name = 'index.html'

"""class SearchView(ListView):
    template_name = 'search.html'
    model = Room
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        adults = int(self.request.GET['a'])
        children = int(self.request.GET['c'])
        query = adults + children
        results = Room.objects.all().values('id','name','price_room','beds','image_header','url','roomtype__name','roomtype__people').filter(status='D',roomtype__people=query)
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['srooms']= self.get_queryset()
        return context"""

"""class RoomDetailView(DetailView):
    template_name = 'available.html'
    model = Room
    context_object_name = 'available'
    slug_field = 'url'
    slug_url_kwarg = 'url'

    def get_queryset(self):
        return self.model.objects.filter(url=self.kwargs['url'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.all().values('id','name','description','status','price_room','beds','image_header','url','roomtype__name','roomtype__people').filter(status='D')
        context['imagesroom'] = ImagesRoom.objects.filter(room=self.get_object()).all()
        return context"""


"""def detail(request, id):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Room.objects.all().values('id','name','description','status','price_room','beds','image_header','url','roomtype__name','roomtype__people').filter(id=id)
    imagesroom = ImagesRoom.objects.filter(room=id).all()
    context = {'products':products, 'cartItems':cartItems, 'imagesroom':imagesroom}
    return render(request,'available.html',context)"""

def detail(request):
    adults = int(request.GET.get('a'))
    children = int(request.GET.get('c'))
    checkin = datetime.strptime(request.GET.get('din'),"%Y-%m-%d").date()
    checkout = datetime.strptime(request.GET.get('dout'),"%Y-%m-%d").date()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    query = adults + children
    night = (checkout - checkin).days
    products = Room.objects.all().values('id','name','description','status','price_room','beds','image_header','url','roomtype__name','roomtype__people').filter(status='D',roomtype__people=query)

    context = {'products':products, 'items':items, 'order':order, 'cartItems':cartItems, 'adults':adults, 'children':children, 'checkin':checkin, 'checkout':checkout, 'night':night}
    return render(request,'available.html',context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)

def checkout(request):
    adults = request.GET.get('a')
    children = request.GET.get('c')
    checkin = request.GET.get('din')
    checkout = request.GET.get('dout')
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'adults':adults, 'children':children, 'checkin':checkin, 'checkout':checkout}
    return render(request, 'checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('Product:',productId)

    customer = request.user.customer
    product = Room.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,  product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    Reservation.objects.create(customer=customer, order=order, checkin=data['checkin'], checkout=data['checkout'], adults=data['adults'], children=data['children'])

    return JsonResponse('Payment complete!', safe=False)
