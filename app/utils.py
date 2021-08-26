import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:',cart)

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Room.objects.get(id=i)
            total = (product.price_room * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price_room,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)

        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems, 'order':order, 'items':items}

def guestOrder(request, data):
    print('User is not logged in..')
    print('COOKIES:', request.COOKIES)
    type_id = data['form']['type_id']
    numb = data['form']['numb']
    name = data['form']['name']
    last_name = data['form']['last_name']
    email = data['form']['email']
    phone = data['form']['phone']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email,)
    customer.type_id = type_id
    customer.numb = numb
    customer.name = name
    customer.last_name = last_name
    customer.phone = phone
    customer.save()

    order = Order.objects.create(customer=customer, complete=False,)

    for item in items:
        product = Room.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(room=product, order=order,quantity=item['quantity'])
        "Room.objects.filter(id=product).update(Status='Ocupada')"
    return customer, order
