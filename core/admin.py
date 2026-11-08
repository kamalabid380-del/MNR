from django.contrib import admin

from .models import (
    Category, CategoryCard, ContactMessage, EditorialBlock, HeroSlide,
    NewsletterSubscriber, Order, OrderItem, Page, Product, SiteSettings, StudioImage,
)

admin.site.site_header = "MNR Design Studio — Administration"
admin.site.site_title = "MNR Admin"
admin.site.index_title = "Store management"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ["title", "link", "order", "is_active"]
    list_editable = ["order", "is_active"]


@admin.register(CategoryCard)
class CategoryCardAdmin(admin.ModelAdmin):
    list_display = ["title", "link", "order", "is_active"]
    list_editable = ["order", "is_active"]


@admin.register(EditorialBlock)
class EditorialBlockAdmin(admin.ModelAdmin):
    list_display = ["title", "link", "order", "is_active"]
    list_editable = ["order", "is_active"]


@admin.register(StudioImage)
class StudioImageAdmin(admin.ModelAdmin):
    list_display = ["caption", "order"]
    list_editable = ["order"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "show_in_nav", "nav_order"]
    list_editable = ["show_in_nav", "nav_order"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "compare_price", "available", "is_featured", "order"]
    list_editable = ["price", "compare_price", "available", "is_featured", "order"]
    list_filter = ["available", "is_featured", "collections"]
    search_fields = ["name", "slug"]
    filter_horizontal = ["collections"]
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["subtotal"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone", "city", "total", "status", "created_at"]
    list_editable = ["status"]
    list_filter = ["status", "city"]
    search_fields = ["name", "phone", "email"]
    inlines = [OrderItemInline]
    readonly_fields = ["total", "created_at"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "handled", "created_at"]
    list_editable = ["handled"]
    list_filter = ["handled"]


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "created_at"]
    search_fields = ["email"]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "updated_at"]
    prepopulated_fields = {"slug": ("title",)}