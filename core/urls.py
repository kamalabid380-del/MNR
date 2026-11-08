from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("collections/all/", views.catalog, name="catalog"),
    path("collections/<slug:slug>/", views.collection, name="collection"),
    path("products/<slug:slug>/", views.product_detail, name="product"),
    path("search/", views.search, name="search"),
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:pk>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:pk>/success/", views.order_success, name="order_success"),
    path("contact/", views.contact, name="contact"),
    path("newsletter/", views.newsletter, name="newsletter"),
    path("pages/<slug:slug>/", views.page, name="page"),
]