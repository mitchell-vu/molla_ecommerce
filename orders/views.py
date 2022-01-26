from django.shortcuts import render, redirect
from django.http import JsonResponse
from carts.models import CartItem
# from .forms import OrderForm
import datetime
from carts.views import get_cart
from .models import Order, Payment, OrderProduct
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def sendEmail(request, order):
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


# def payments(request):
#     try:
#         if request.is_ajax() and request.method == 'POST':
#             data = request.POST
#             order_id = data['orderID']
#             trans_id = data['transID']
#             payment_method = data['payment_method']
#             status = data['status']

#             # Lấy bản ghi order
#             order = Order.objects.get(
#                 user=request.user, is_ordered=False, order_number=order_id)
#             # Tạo 1 bản ghi payment
#             payment = Payment(
#                 user=request.user,
#                 payment_id=trans_id,
#                 payment_method=payment_method,
#                 amount_paid=order.order_total,
#                 status=status,
#             )
#             payment.save()

#             order.payment = payment
#             order.is_ordered = True
#             order.save()

#             # Chuyển hết cart_item thành order_product
#             cart_items = CartItem.objects.filter(user=request.user)
#             for item in cart_items:
#                 order_product = OrderProduct()
#                 order_product.order_id = order.id
#                 order_product.payment = payment
#                 order_product.user_id = request.user.id
#                 order_product.product_id = item.product_id
#                 order_product.quantity = item.quantity
#                 order_product.product_price = item.product.price
#                 order_product.ordered = True
#                 order_product.save()

#                 cart_item = CartItem.objects.get(id=item.id)
#                 product_variation = cart_item.variations.all()
#                 order_product = OrderProduct.objects.get(id=order_product.id)
#                 order_product.variations.set(product_variation)
#                 order_product.save()

#                 # Reduce the quantity of the sold products
#                 product = Product.objects.get(id=item.product_id)
#                 product.stock -= item.quantity
#                 product.save()

#             # Xóa hết cart_item
#             CartItem.objects.filter(user=request.user).delete()

#             # Gửi thư cảm ơn
#             sendEmail(request=request, order=order)

#             # Phản hồi lại ajax
#             data = {
#                 'order_number': order.order_number,
#                 'transID': payment.payment_id,
#             }
#         return JsonResponse({"data": data}, status=200)
#     except Exception as e:
#         return JsonResponse({"error": e}, status=400)


def place_order(request, total=0, quantity=0,):

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)

    if cart_items.count() <= 0:
        return redirect('store')

    grand_total = 0

    for cart_item in cart_items:
        total += cart_item.sub_total()
        quantity += cart_item.quantity
    grand_total = total

    if request.method == 'POST':
        print(request.POST)
        form = request.POST

        # Store all the billing information inside Order table
        data = Order()
        data.user = request.user
        data.full_name = form['full_name']
        data.phone = form['phone_number']
        data.email = form['email']

        data.address = form['address']
        data.province = form['province']
        data.city = form['city']

        data.order_note = form['order_note']
        data.order_total = grand_total
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()

        # Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        mt = int(datetime.date.today().strftime('%m'))
        dt = int(datetime.date.today().strftime('%d'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")         # 20210305
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.is_ordered = True
        
        data.save()

        # Move all cart items into ordered items
        order = Order.objects.get(order_number=data.order_number)

        for item in cart_items:
            order_product = OrderProduct()
            order_product.order = order
            order_product.product = item.product
            order_product.quantity = item.quantity
            order_product.product_price = item.product.price
            order_product.ordered = True

            order_product.save()

            product_variation = item.variations.all()
            order_product.variations.set(product_variation)
            
            order_product.save()

            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

            # Clear cart items
            CartItem.objects.filter(cart=cart).delete()

            # Send thank you mail
            # sendEmail(request=request, order=order)

        return redirect('account')
    
    else:
        return redirect('checkout')
