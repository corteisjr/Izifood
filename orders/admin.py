import xlsxwriter
from django.contrib import admin
from datetime import datetime

from django.http import HttpResponse

from .models import Order, OrderItem, Product


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
        header_list.append(f'{product.name} qty')
        header_list.append(f'{product.name} price')
    
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
            
        for product in prod_tracker:
            for qty_price in prod_tracker[product].values():
                data_row.append(qty_price)
            order_price_total += (prod_tracker[product]['qty'] * prod_tracker[product]['price'])
        
        data_row.append(order_price_total)
        
        for column, item in enumerate(data_row):
            worksheet.write(row + 1, column, item)
            
    workbook.close()
    
    return response


export_orders_to_xlsx.short_description = 'Exportar para XLSX'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'telephone', 'address', 'postal_code', 'city', 'created', 'updated', 'status', 'transport', 'transport_price', 'note']
    list_filter = ['status', 'created', 'updated']
    inlines = [OrderItemInline]
   
    actions = [export_orders_to_xlsx] 
    
    
    
