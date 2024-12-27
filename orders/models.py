from django.db import models
from listings.models import Product

ORDER_STATUS = (
    ('Created', 'Criado'),
    ('Processing', 'Processando'),
    ('Completed', 'Completo'),
    ('Shipped', 'Enviado'),
    ('Ready for pickup', 'Pronto para retirada'),
    ('Canceled', 'Cancelado')
)

TRANSPORT_CHOICES = [
    ('Moto taxi', 'Moto táxi'),
    ('Recipient pickup', 'Retirada no local')
]


class Order(models.Model):
    first_name = models.CharField('Nome', max_length=50)
    last_name = models.CharField('Sobrenome', max_length=50)
    email = models.EmailField('Email')
    telephone = models.CharField('Telefone', max_length=15)
    address = models.CharField('Endereço', max_length=250)
    postal_code = models.CharField('CEP', max_length=20)
    city = models.CharField('Cidade', max_length=100)
    created = models.DateTimeField('Criado em', auto_now_add=True)
    updated = models.DateTimeField('Atualizado em', auto_now=True)
    status = models.CharField('Status', max_length=20, choices=ORDER_STATUS, default='Created')
    transport = models.CharField('Transporte', max_length=20, choices=TRANSPORT_CHOICES, default='Moto taxi')
    transport_price = models.DecimalField('Preço do transporte', max_digits=10, decimal_places=2, default=0)
    note = models.TextField('Observação', blank=True)
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return f'Pedido #{self.id}'
    
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        total_cost += self.transport_price
        return total_cost
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Quantidade')
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
    
