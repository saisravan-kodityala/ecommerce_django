# store/views/cart.py
from django.shortcuts import render
from django.views import View
from store.models.products import Products

class Cart(View):
    def get(self, request):
        """
        Builds an items list for the template:
        items = [
          {'product': Product instance, 'qty': 2, 'line_total': 200},
          ...
        ]
        and grand_total as integer/decimal.
        """
        cart = request.session.get('cart', {})

        # Ensure keys are strings (session might store ints or strings)
        # We'll normalize product ids to strings when storing to session (see note below)
        product_ids = list(cart.keys())
        products = Products.get_products_by_id(product_ids) if product_ids else []

        items = []
        grand_total = 0

        for p in products:
            # get quantity from session cart. Try both string and int keys.
            qty = cart.get(str(p.id), cart.get(p.id, 0))
            try:
                qty = int(qty)
            except (TypeError, ValueError):
                qty = 0
            line_total = p.price * qty
            grand_total += line_total
            items.append({
                'product': p,
                'qty': qty,
                'line_total': line_total,
            })

        context = {
            'items': items,
            'grand_total': grand_total,
        }
        return render(request, 'cart.html', context)
