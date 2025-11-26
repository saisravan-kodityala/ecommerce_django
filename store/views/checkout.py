# store/views/checkout.py
from django.shortcuts import render, redirect
from django.views import View
from store.models.products import Products
from store.models.orders import Order
from store.models.customer import Customer

class CheckOut(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart')

        product_ids = list(cart.keys())
        products = Products.get_products_by_id(product_ids) if product_ids else []

        items = []
        grand_total = 0
        for p in products:
            qty = int(cart.get(str(p.id), cart.get(p.id, 0) or 0))
            line_total = p.price * qty
            grand_total += line_total
            items.append({'product': p, 'qty': qty, 'line_total': line_total})

        return render(request, 'checkout.html', {'items': items, 'grand_total': grand_total})

    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer')
        if not customer_id:
            return redirect(f"/login?return_url=/check-out")

        cart = request.session.get('cart', {}) or {}
        products = Products.get_products_by_id(list(cart.keys())) if cart else []

        for p in products:
            qty = int(cart.get(str(p.id), 0) or 0)
            if qty <= 0:
                continue
            order = Order(
                customer=Customer(id=customer_id),
                product=p,
                price=p.price,
                address=address,
                phone=phone,
                quantity=qty
            )
            order.save()

        request.session['cart'] = {}
        return redirect('orders')
