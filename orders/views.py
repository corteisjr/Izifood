from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .tasks import order_created
from .models import OrderItem, Product, Order
from decouple import config
from django.conf import settings
from .forms import OrderCreateForm
from cart.views import get_cart, cart_clear
from decimal import Decimal
# Mpesa payment Library
from pprint import pprint
from portalsdk import APIContext, APIMethodType, APIRequest
# PDF generation Library
from django.template.loader import render_to_string
import weasyprint



@staff_member_required
def invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

    # Generate PDF
    html = render_to_string('pdf.html', {'order': order})
    stylesheets = [weasyprint.CSS(f'{settings.STATIC_ROOT}css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=stylesheets)
    
    return response

def payment(request, order, total_price):
    api_context = APIContext()
    api_context.api_key = config('MPESA_API_KEY')
    api_context.public_key = config('MPESA_PUBLIC_KEY')
    api_context.ssl = True
    api_context.method_type = APIMethodType.POST
    api_context.address = 'api.sandbox.vm.co.mz'
    api_context.port = 18352
    api_context.path = '/ipg/v1x/c2bPayment/singleStage/'
    
    api_context.add_header('Origin', '*')

    api_context.add_parameter('input_TransactionReference','T12344C')
    api_context.add_parameter(f'input_CustomerMSISDN', '258' + order.telephone)
    api_context.add_parameter(f'input_Amount', str(total_price))
    api_context.add_parameter('input_ThirdPartyReference','111PA2D')
    api_context.add_parameter('input_ServiceProviderCode','171717')


    api_request = APIRequest(api_context)
    result = api_request.execute()

    pprint(result.status_code)
    pprint(result.headers)
    pprint(result.body)

def order_create(request):
    cart = get_cart(request)
    cart_qty = sum(item['quantity'] for item in cart.values())
    transport_cost = round((70 + (cart_qty // 10) * 1.5), 2)
    
    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            cf = order_form.cleaned_data
            transport = cf['transport']
            
            if transport == 'Recipient pickup':
                transport_cost = 0
            
            order = order_form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.transport_price = Decimal(transport_cost)
            order.save()
            
            product_ids = cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            
            total_price = sum(Decimal(product.price) * cart[str(product.id)]['quantity'] for product in products)
            
            if transport_cost:
                total_price += Decimal(transport_cost)
            else:
                total_price
            
            payment(request, order, total_price)
            for product in products:
                cart_item = cart[str(product.id)]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=cart_item['price'],
                    quantity=cart_item['quantity']
                )
            cart_clear(request)
            order_created.delay(order.id)
            
            return render(
                request,
                'order_created.html',
                {'order': order}
            )
    else:
        order_form = OrderCreateForm()
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'telephone': request.user.profile.phone_number,
                'address': request.user.profile.address,
                'postal_code': request.user.profile.postal_code,
                'city': request.user.profile.city
            }
            order_form = OrderCreateForm(initial=initial_data)
    
    return render(
        request,
        'order_create.html',
        {'cart': cart, 
         'order_form': order_form, 
         'transport_cost': transport_cost
         }
    )

def customer_invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user == order.user:        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

        # Generate PDF
        html = render_to_string('pdf.html', {'order': order})
        stylesheets = [weasyprint.CSS(f'{settings.STATIC_ROOT}css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(response, stylesheets=stylesheets)
        
        return response
    return redirect('profile')
    
