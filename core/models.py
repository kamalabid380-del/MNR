from django.db import models


class SiteSettings(models.Model):
    brand_name = models.CharField(max_length=120, default="Mohsin Naveed Ranjha")
    short_name = models.CharField(max_length=20, default="MNR")
    tagline = models.CharField(max_length=80, default="Design Studio")
    logo = models.ImageField(upload_to="home/", blank=True)
    logo_footer = models.ImageField(upload_to="home/", blank=True)
    announcement_1 = models.CharField(max_length=160, default="Flat 40% OFF | Live now")
    announcement_2 = models.CharField(max_length=160, blank=True, default="Kaur Bridals | Live Now")
    phone = models.CharField(max_length=40, default="+92 42 3575 8880")
    whatsapp_number = models.CharField(max_length=20, default="923008451482", help_text="Digits only, country code first.")
    email = models.EmailField(default="info@mohsinnaveedranjha.com")
    address = models.CharField(max_length=200, default="MNR Design Studio, Gulberg, Lahore, Pakistan")
    facebook_url = models.URLField(blank=True, default="https://www.facebook.com/mohsinnaveedranjha")
    instagram_url = models.URLField(blank=True, default="https://www.instagram.com/mohsinnaveedranjha")
    youtube_url = models.URLField(blank=True, default="https://www.youtube.com/@mohsinnaveedranjha")
    tiktok_url = models.URLField(blank=True, default="https://www.tiktok.com/@mohsinnaveedranjha")
    studio_text = models.TextField(default="We invite you to embark on a journey of bridal elegance and personalized style by booking an appointment at our prestigious bridal studio.")
    studio_button = models.CharField(max_length=60, default="Book an Appointment")
    campaign_video = models.FileField(upload_to="home/", blank=True)
    campaign_poster = models.ImageField(upload_to="home/", blank=True)
    footer_note = models.CharField(max_length=160, default="© Mohsin Naveed Ranjha — Design Studio. All rights reserved.")

    class Meta:
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.brand_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def whatsapp_link(self):
        digits = "".join(c for c in self.whatsapp_number if c.isdigit())
        return f"https://wa.me/{digits}" if digits else ""


class HeroSlide(models.Model):
    title = models.CharField(max_length=120, help_text="Used as the image alt text.")
    image = models.ImageField(upload_to="home/")
    link = models.CharField(max_length=200, default="/collections/kaur-bridals/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class CategoryCard(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="home/")
    link = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class EditorialBlock(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="home/")
    link = models.CharField(max_length=200)
    button_label = models.CharField(max_length=40, default="Shop Now")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class StudioImage(models.Model):
    image = models.ImageField(upload_to="home/")
    caption = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Studio image {self.pk}"


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    intro = models.TextField(blank=True)
    show_in_nav = models.BooleanField(default=False)
    nav_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["nav_order", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True, help_text="HTML allowed.")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    compare_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Original price — shown struck through when higher than price.")
    image = models.ImageField(upload_to="products/")
    collections = models.ManyToManyField(Category, related_name="products", blank=True)
    available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

    @property
    def on_sale(self):
        return bool(self.compare_price and self.compare_price > self.price)


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("dispatched", "Dispatched"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.TextField()
    city = models.CharField(max_length=80)
    notes = models.TextField(blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} — {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} × {self.quantity}"

    @property
    def subtotal(self):
        return (self.price or 0) * (self.quantity or 0)


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    handled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.created_at:%d %b %Y}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Page(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    body = models.TextField(help_text="HTML allowed.")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title