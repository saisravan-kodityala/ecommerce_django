# store/views/home.py
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.paginator import Paginator
from django.views import View

from store.models.products import Products
from store.models.category import Category


class Index(View):
    """
    Handles POST (add/remove cart) and GET (redirect to /store with same querystring).
    Keep POST target as 'homepage' in templates so this handles Add To Cart.
    """

    def post(self, request):
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        remove_all = request.POST.get('remove_all')

        cart = request.session.get('cart', {})
        product_id = str(product_id)  # normalize key

        if remove_all:
            cart.pop(product_id, None)
        else:
            qty = cart.get(product_id, 0)
            try:
                qty = int(qty)
            except (TypeError, ValueError):
                qty = 0

            if remove:
                if qty <= 1:
                    cart.pop(product_id, None)
                else:
                    cart[product_id] = qty - 1
            else:
                cart[product_id] = qty + 1

        request.session['cart'] = cart
        return redirect('homepage')

    def get(self, request):
        # Keep previous behavior: redirect to /store with same querystring
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')



def store(request):
    """
    Renders the store page. Supports ?category=<id> and pagination via ?page=<n>.
    """
    if not request.session.get('cart'):
        request.session['cart'] = {}

    # grab categories (your Category.get_all_categories should return iterable)
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    page_number = request.GET.get('page')

    if categoryID:
        products_qs = Products.get_all_products_by_categoryid(categoryID)
        # try to find the selected category object for template usage (optional)
        selected_category = None
        try:
            selected_category = next((c for c in categories if str(c.id) == str(categoryID)), None)
        except Exception:
            selected_category = None
    else:
        products_qs = Products.get_all_products()
        selected_category = None

    # paginate (12 per page)
    paginator = Paginator(products_qs, 12)
    products_page = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': products_page,
        'selected_category': selected_category,
    }
    return render(request, 'index.html', context)
