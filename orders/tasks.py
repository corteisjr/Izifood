from celery import shared_task 
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from io import BytesIO
import weasyprint
from .models import Order

@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Pedido nr. {order.id}'
    message = f'Caro {order.first_name},\n\n' \
              f'Você fez um pedido com sucesso.\n' \
              f'ID do pedido: {order.id}.'
    mail_sent = EmailMessage(subject,
                          message,
                          'yoocomerce@shop.com',
                            [order.email])

    # Gererate PDF
    html = render_to_string('pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(f'{settings.STATIC_ROOT}css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    
    # Attach PDF file
    mail_sent.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    mail_sent.send()
    return mail_sent
  
  
@shared_task
def status_change_notification(order_id):
    """
    Task to send an e-mail notification when an order status
    is changed.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Pedido nr. {order.id}'
    message = f'Caro {order.first_name},\n\n' \
              f'O status do seu pedido foi atualizado.\n' \
              f'Novo status: {order.status}.'
    mail_sent = send_mail(subject,
                          message,
                          'yoocomerce@shop.com',
                            [order.email])
    
    return mail_sent