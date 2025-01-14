from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required
from ecommerce_project.decorators import user_created_order


urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('admin/order/<int:order_id>/pdf/', staff_member_required(views.invoice_pdf), name='invoice_pdf'),
    path('order/<int:order_id>/pdf/', user_created_order(views.customer_invoice_pdf), name='customer_invoice_pdf')
]