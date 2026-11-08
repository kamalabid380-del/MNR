from decimal import Decimal

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CheckoutForm, ContactForm
from .models import (
    Category, CategoryCard, EditorialBlock, HeroSlide, NewsletterSubscriber,
    Order, OrderItem, Page, Product, SiteSettings, StudioImage,
)


def home(request):
    return render(request, "core/home.html", {
        "heroes": HeroSlide.objects.filter(is_active=True),
        "cards": CategoryCard.objects.filter(is_active=True),
        "editorials": EditorialBlock.objects.filter(is_active=True),
        "studio_images": StudioImage.objects.all(),
        "featured": Product.objects.filter(is_featured=True, available=True)[:8],
    })


def _sorted(products, sort):
    if sort == "price-asc":
        return products.order_by("price", "order")
    if sort == "price-desc":
        return products.order_by("-price", "order")
    if sort == "name":
        return products.order_by("name")
    return products.order_by("order", "id")


def collection(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = _sorted(category.products.all(), request.GET.get("sort", ""))
    return render(request, "core/collection.html", {"category": category, "products": products, "sort": request.GET.get("sort", "")})


def catalog(request):
    products = _sorted(Product.objects.all(), request.GET.get("sort", ""))
    return render(request, "core/collection.html", {"category": None, "products": products, "sort": request.GET.get("sort", ""), "is_catalog": True})


def search(request):
    q = request.GET.get("q", "").strip()
    products = Product.objects.none()
    if q:
        products = _sorted(Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q)), request.GET.get("sort", ""))
    return render(request, "core/collection.html", {"category": None, "products": products, "q": q, "sort": request.GET.get("sort", "")})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    more = Product.objects.filter(collections__in=product.collections.all(), available=True).exclude(pk=product.pk).distinct()[:4]
    return render(request, "core/product.html", {"product": product, "more": more})


def page(request, slug):
    return render(request, "core/page.html", {"page": get_object_or_404(Page, slug=slug)})


def _cart(request):
    return request.session.setdefault("cart", {})


def _cart_lines(request):
    cart = _cart(request)
    lines, total = [], Decimal("0")
    for pk, qty in list(cart.items()):
        product = Product.objects.filter(pk=int(pk)).first()
        if not product:
            cart.pop(pk, None)
            continue
        line_total = product.price * qty
        total += line_total
        lines.append({"product": product, "quantity": qty, "line_total": line_total})
    request.session.modified = True
    return lines, total


def _safe_next(request, fallback):
    nxt = request.POST.get("next", "")
    if nxt.startswith("/") and not nxt.startswith("//"):
        return nxt
    return fallback


def cart_detail(request):
    lines, total = _cart_lines(request)
    return render(request, "core/cart.html", {"lines": lines, "total": total})


@require_POST
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not product.available:
        messages.info(request, f"{product.name} is currently sold out.")
        return redirect("product", slug=product.slug)
    cart = _cart(request)
    cart[str(pk)] = min(cart.get(str(pk), 0) + 1, 20)
    request.session.modified = True
    messages.success(request, f"{product.name} added to your bag.")
    return redirect(_safe_next(request, "cart"))


@require_POST
def cart_update(request, pk):
    cart = _cart(request)
    try:
        qty = int(request.POST.get("quantity", "1"))
    except ValueError:
        qty = 1
    if qty > 0:
        cart[str(pk)] = min(qty, 20)
    else:
        cart.pop(str(pk), None)
    request.session.modified = True
    return redirect("cart")


@require_POST
def cart_remove(request, pk):
    cart = _cart(request)
    cart.pop(str(pk), None)
    request.session.modified = True
    return redirect("cart")


def checkout(request):
    lines, total = _cart_lines(request)
    if not lines:
        return redirect("catalog")
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total = total
            order.save()
            for line in lines:
                OrderItem.objects.create(
                    order=order, product=line["product"], name=line["product"].name,
                    price=line["product"].price, quantity=line["quantity"],
                )
            request.session["cart"] = {}
            request.session.modified = True
            return redirect("order_success", pk=order.pk)
    else:
        form = CheckoutForm()
    return render(request, "core/checkout.html", {"form": form, "lines": lines, "total": total})


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    site = SiteSettings.load()
    wa_text = f"Hello MNR, I placed order #{order.pk} ({order.name}, {order.city}). Total Rs. {order.total}."
    wa_link = f"{site.whatsapp_link}?text={wa_text.replace(' ', '%20')}" if site.whatsapp_link else ""
    return render(request, "core/order_success.html", {"order": order, "wa_link": wa_link})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you — your message has been sent. Our studio replies within one working day.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


@require_POST
def newsletter(request):
    email = request.POST.get("email", "").strip()
    if email:
        NewsletterSubscriber.objects.get_or_create(email=email)
        messages.success(request, "You are on the list — thank you.")
    nxt = request.POST.get("next", "")
    if nxt.startswith("/") and not nxt.startswith("//"):
        return redirect(nxt)
    return redirect("home")