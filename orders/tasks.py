from celery import shared_task 
from django.core.mail import send_mail
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
    mail_sent = send_mail(subject,
                          message,
                          'yoocomerce@shop.com',
                            [order.email])
    return mail_sent