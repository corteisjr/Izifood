import xlsxwriter
from django.contrib import admin
from datetime import datetime

from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html

from .tasks import status_change_notification
from .models import Order, OrderItem, Product


def order_pdf(obj):
    return format_html(
        '<a href="{}" target="_blank">PDF</a>',
        reverse('invoice_pdf', args=[obj.id]))
    
order_pdf.short_description = 'Fatura PDF'

def export_orders_to_xlsx(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    datetimeObj = datetime.now()
    timestamp = datetimeObj.strftime("%d-%b-%Y %H:%M:%S")

    content_disposition = f'attachment; filename=orders_{timestamp}.xlsx'
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = content_disposition
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    fields = [
        field for field in opts.get_fields()
        if not field.one_to_many
    ]
    header_list = [field.name for field in fields]

    products = Product.objects.all()
    for product in products:
        header_list.extend((f'{product.name} qty', f'{product.name} price'))
    header_list.append('order_price_total')

    # Cabeçalho
    for column, item in enumerate(header_list):
        worksheet.write(0, column, item)

    # Linhas
    for row, obj in enumerate(queryset):
        prod_tracker = {product.name:{'qty':0, 'price':0} for product in products}

        order_items = obj.items.all()
        for item in order_items:
            prod_tracker[item.product.name]['qty'] = item.quantity
            prod_tracker[item.product.name]['price'] = item.price

        data_row = []
        order_price_total = 0

        for field in fields:
            value = getattr(obj, field.name)
            if field.name == 'transport_cost':
                order_price_total += value
            if isinstance(value, datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)

        for product, value_ in prod_tracker.items():
            data_row.extend(iter(value_.values()))
            order_price_total += (prod_tracker[product]['qty'] * prod_tracker[product]['price'])

        data_row.append(order_price_total)

        for column, item in enumerate(data_row):
            worksheet.write(row + 1, column, item)

    workbook.close()

    return response


export_orders_to_xlsx.short_description = 'Exportar para XLSX'

def status_change(queryset, status):
    for order in queryset:
        order.status = status
        order.save()
        status_change_notification.delay(order.id)    
    

def status_processing(modeladmin, request, queryset):
    status_change(queryset, 'Processing') 

status_processing.short_description = 'Mudar status para Processando'


def status_Completed(modeladmin, request, queryset):
    status_change(queryset, 'Completed')


status_Completed.short_description = 'Mudar status para Completo'

def status_Canceled(modeladmin, request, queryset):
    status_change(queryset, 'Canceled')


status_Canceled.short_description = 'Mudar status para Cancelado'


def status_Shipped(modeladmin, request, queryset):
    status_change(queryset, 'Shipped')


status_Shipped.short_description = 'Mudar status para Enviado'

def status_Ready_for_pickup(modeladmin, request, queryset):
    status_change(queryset, 'Ready for pickup')


status_Ready_for_pickup.short_description = 'Mudar status para Pronto para retirada'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'telephone', 'address', 'postal_code', 'city', 'created', 'updated', 'status', 'transport', order_pdf]
    list_filter = ['status', 'created', 'updated']
    inlines = [OrderItemInline]
   
    actions = [
        export_orders_to_xlsx, 
        status_processing,
        status_Completed,
        status_Canceled,
        status_Shipped,
        status_Ready_for_pickup
    ] 
    
    
    
