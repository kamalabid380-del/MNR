from .models import Category, SiteSettings


def site(request):
    cart = request.session.get("cart", {})
    return {
        "site": SiteSettings.load(),
        "nav_categories": Category.objects.filter(show_in_nav=True),
        "cart_count": sum(cart.values()),
    }