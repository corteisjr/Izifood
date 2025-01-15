from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator

from cart.forms import CartAddProductForm
from listings.forms import ReviewForm
from .models import Category, Product, Review


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    request_category = None
    products = Product.objects.all()
    
    if category_slug:
        request_category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=request_category)
    
    # Pagination
    if len(products) > 0:
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        products = paginator.get_page(page)
    
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    
    return render(
        request,
        'product/list.html',
        {
            'categories': categories,
            'request_category': request_category,
            'products': products,
            'parameters': parameters
        }
    )
    

def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category_id=category.id, slug=product_slug)
    
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            cf = review_form.cleaned_data
            author_name = "Anonymous"
            if request.user.is_authenticated and request.user.first_name != '':
                author_name = request.user.first_name
            Review.objects.create(
                product=product,
                author=author_name,
                rating=cf['rating'],
                text=cf['text']
            )
        return redirect(
            'product_detail',
            category_slug=category_slug, product_slug=product_slug
        )
    else:
        review_form = ReviewForm()
        cart_product_form = CartAddProductForm()
        return render(
            request, 
            'product/detail.html', 
            {
                'product': product,
                'review_form' : review_form,
                'cart_product_form': cart_product_form,
            }
        )