from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('admin/order/<int:order_id>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('order/<int:order_id>/pdf/', views.customer_invoice_pdf, name='customer_invoice_pdf')
]