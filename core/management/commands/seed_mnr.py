"""Seed the MNR store from catalog.json and the downloaded homepage assets.

Idempotent: safe to run repeatedly. Usage: python manage.py seed_mnr
"""
import json
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import (
    Category, CategoryCard, EditorialBlock, HeroSlide, Page, Product,
    SiteSettings, StudioImage,
)

CATEGORIES = [
    # slug, name, intro, show_in_nav, nav_order
    ("sale", "Sale", "Selected pieces from the archive at special prices. Flat 40% off, live now — while stock lasts.", False, 0),
    ("kaur-bridals", "Kaur Bridals", "The signature bridal edit. Hand-embellished lehengas and shararas in jewel tones, crafted for the modern bride.", True, 1),
    ("celebrity-spotted", "Celebrity Spotted", "MNR on screen and in the front row — pieces worn by the house's celebrity patrons.", True, 2),
    ("luxury-pret", "Luxury Pret", "Ready-to-wear luxury pret. Effortless silhouettes, intricate detail, delivered ready to wear.", True, 3),
    ("bridals", "Bridals", "Wedding couture from the MNR atelier — regal bridal ensembles made to order in Lahore.", True, 4),
    ("formals", "Formals", "Formal elegance for the season's invitations — embroidered saris, ghararas and long shirts.", True, 5),
    ("women", "Women", "Ready to deliver womenswear. Shop the women's edit and receive your piece without the wait.", True, 6),
    ("menswear", "Menswear", "Ceremonial menswear — tailored waistcoats, sherwanis and kurtas with the house's signature finish.", True, 7),
    ("mnr-patrons", "MNR Patrons", "The women who wear MNR. A curated edit of pieces chosen by the house's patrons.", True, 8),
    ("punjab-festive-edit", "Punjab Festive Edit", "A festive celebration of Punjab — vibrant colour, traditional craft, joyful silhouettes.", False, 10),
    ("farid-manzil", "Farid Manzil", "Farid Manzil — Luxury Pret '26. An homage to the old city's havelis, rendered in thread and silk.", False, 11),
    ("guftagu", "Guftagu", "Guftagu — Eid-e-Bahar. Conversations in colour: a festive unstitched edit for the spring season.", False, 12),
    ("begum-shaadi", "Begum Shaadi", "Begum Shaadi '26 — the wedding season edit for the mother of the bride and the whole family.", False, 13),
    ("chai-coffee", "Chai Coffee", "Chai & Coffee — Luxury Pret Vol. 6. Easy, indulgent pret named after the house's favourite comforts.", False, 14),
    ("zarlish", "Zarlish", "Zarlish — Festive Unstitched Vol. VI. Shimmering fabrics and embroidered patches, ready to tailor.", False, 15),
    ("nikkah-mubarak", "Nikkah Mubarak", "Nikkah Mubarak — understated, luminous ensembles for the signing of the vows.", False, 16),
    ("zma-meena", "Zma Meena", "Zma Meena — jewel-toned festives inspired by the enamel craft of the north.", False, 17),
]

# Archived collections on the live site are curated here from related live edits.
CURATIONS = {
    "farid-manzil": "luxury-pret",
    "guftagu": "punjab-festive-edit",
    "zarlish": "formals",
    "mnr-patrons": "celebrity-spotted",
}

HEROES = [
    ("Kaur Bridals — the bridal edit", "home/hero-kaur-1.jpg", "/collections/kaur-bridals/"),
    ("Kaur Bridals — hand-embellished couture", "home/hero-kaur-2.jpg", "/collections/kaur-bridals/"),
    ("Kaur Bridals — now live", "home/hero-kaur-3.jpg", "/collections/kaur-bridals/"),
    ("Flat 40% OFF — the sale is live", "home/hero-sale-1.jpg", "/collections/sale/"),
    ("Sale — selected archive pieces", "home/hero-sale-2.jpg", "/collections/sale/"),
]

CARDS = [
    ("Kaur Bridals", "home/cat-kaur-bridals.jpg", "/collections/kaur-bridals/"),
    ("Punjab Festive Edit", "home/cat-punjab-festive-edit.jpg", "/collections/punjab-festive-edit/"),
    ("Farid Manzil", "home/cat-farid-manzil.jpg", "/collections/farid-manzil/"),
    ("Guftagu", "home/cat-guftagu.jpg", "/collections/guftagu/"),
    ("Begum Shaadi", "home/cat-begum-shaadi.jpg", "/collections/begum-shaadi/"),
    ("Nikkah Mubarak", "home/cat-nikkah-mubarak.jpg", "/collections/nikkah-mubarak/"),
    ("Zarlish", "home/cat-zarlish.jpg", "/collections/zarlish/"),
    ("Luxury Pret", "home/cat-luxury-pret.jpg", "/collections/luxury-pret/"),
    ("Zma Meena", "home/cat-zma-meena.jpg", "/collections/zma-meena/"),
    ("Menswear", "home/cat-menswear.jpg", "/collections/menswear/"),
    ("MNR Patrons", "home/cat-mnr-patrons.jpg", "/collections/mnr-patrons/"),
    ("Chai Coffee", "home/cat-chai-coffee.jpg", "/collections/chai-coffee/"),
]

EDITORIALS = [
    ("Bridals", "home/edit-bridals.jpg", "/collections/bridals/"),
    ("Menswear", "home/edit-menswear.jpg", "/collections/menswear/"),
    ("Chai Coffee — Vol. 6", "home/edit-chai-coffee.jpg", "/collections/chai-coffee/"),
    ("Zarlish", "home/edit-zarlish.jpg", "/collections/zarlish/"),
]

PAGES = [
    ("About Us", "about-us", """
<p>Mohsin Naveed Ranjha Design Studio is a Lahore-based couture house celebrated for its bridal craftsmanship. Founded on the belief that every ensemble should feel like an heirloom, the studio pairs traditional subcontinental handwork — zardozi, kora, dabka and resham — with a contemporary, editorial eye.</p>
<h2>The Atelier</h2>
<p>Each MNR piece begins as a sketch in the Gulberg studio and passes through the hands of master artisans before it reaches the bride. From the first consultation to the final fitting, the process is personal, precise and entirely made in Lahore.</p>
<h2>The Edits</h2>
<p>Alongside the bridal couture, the house releases seasonal edits — Kaur Bridals, Farid Manzil, Guftagu, Zarlish, Chai &amp; Coffee and Zma Meena — spanning luxury pret, formals, menswear and festive unstitched fabric.</p>
<h2>Visit Us</h2>
<p>Bridal consultations are by appointment. Write to info@mohsinnaveedranjha.com or call +92 42 3575 8880 to book the studio.</p>
"""),
    ("FAQ's", "faqs", """
<h2>How do I place an order?</h2>
<p>Add pieces to your bag and check out with your delivery details. Every order is confirmed personally by the studio over WhatsApp or phone before it is processed. Cash on delivery is available across Pakistan.</p>
<h2>Do you ship internationally?</h2>
<p>Yes. The studio ships worldwide through tracked courier. International delivery timelines and charges are confirmed with your order on WhatsApp.</p>
<h2>How long does a bridal order take?</h2>
<p>Made-to-order bridals require 8–12 weeks depending on the embellishment. Ready-to-deliver womenswear and luxury pret ship within 5–7 working days.</p>
<h2>Can I book a studio appointment?</h2>
<p>Yes — bridal consultations are by appointment at the Gulberg, Lahore studio. Use the contact page or call +92 42 3575 8880.</p>
<h2>What is your exchange policy?</h2>
<p>Ready-to-wear pieces may be exchanged within 7 days of delivery, unworn and with tags intact. Made-to-order and sale pieces are final sale. See the Shipping Policy for full terms.</p>
"""),
    ("Privacy Policy", "privacy-policy", """
<p>MNR Design Studio respects your privacy. This policy explains what we collect and how it is used.</p>
<h2>What we collect</h2>
<p>When you order or write to us we collect your name, email, phone number and delivery address. Newsletter subscribers provide an email address only.</p>
<h2>How we use it</h2>
<p>Your details are used solely to confirm and deliver your order, respond to enquiries, and — if you subscribe — send the studio's seasonal announcements. We never sell or share your information with third parties beyond the courier handling your delivery.</p>
<h2>Your choices</h2>
<p>You may unsubscribe from announcements at any time, or write to info@mohsinnaveedranjha.com to request a copy or removal of your data.</p>
"""),
    ("Shipping Policy", "shipping-policy", """
<h2>Within Pakistan</h2>
<p>Ready-to-wear orders ship in 5–7 working days via tracked courier. Cash on delivery is available nationwide. Made-to-order bridals follow the timeline confirmed at booking (typically 8–12 weeks).</p>
<h2>International</h2>
<p>Worldwide shipping is available. Charges and delivery estimates are confirmed on WhatsApp before dispatch. Customs duties, where applicable, are the recipient's responsibility.</p>
<h2>Exchanges</h2>
<p>Ready-to-wear pieces may be exchanged within 7 days of delivery — unworn, with original tags and packaging. Made-to-order, customised and sale items are final sale. Pieces damaged in transit are replaced after courier verification.</p>
<h2>Order confirmation</h2>
<p>Every order is personally confirmed by the studio before processing. If we cannot reach you within 48 hours, the order is held and may be cancelled.</p>
"""),
    ("MNR London", "mnr-london", """
<p>MNR London brings the Lahore atelier's bridal and occasion wear to the United Kingdom. The London studio offers private consultations, trunk shows and made-to-measure ordering for the diaspora bride.</p>
<h2>Services</h2>
<ul>
<li>Private bridal consultations by appointment</li>
<li>Seasonal trunk shows of the current edits</li>
<li>Made-to-measure ordering with Lahore atelier fulfilment</li>
<li>UK-wide delivery and international shipping</li>
</ul>
<h2>Appointments</h2>
<p>To book a London consultation or ask about the next trunk show, write to info@mohsinnaveedranjha.com or message the studio on WhatsApp at +92 300 8451482.</p>
"""),
]


class Command(BaseCommand):
    help = "Seed categories, products, homepage content, pages and the admin user."

    def handle(self, *args, **options):
        self.seed_settings()
        cats = self.seed_categories()
        self.seed_products(cats)
        self.seed_home()
        self.seed_pages()
        self.seed_admin()
        self.stdout.write(self.style.SUCCESS("MNR seed complete."))

    def seed_settings(self):
        site = SiteSettings.load()
        site.logo = "home/mnr-crest.png"
        site.logo_footer = "home/mnr-crest-footer.png"
        site.campaign_video = "home/kaur-campaign.mp4"
        site.campaign_poster = "home/hero-kaur-1.jpg"
        site.save()

    def seed_categories(self):
        cats = {}
        for slug, name, intro, in_nav, nav_order in CATEGORIES:
            cat, _ = Category.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "intro": intro, "show_in_nav": in_nav, "nav_order": nav_order},
            )
            cats[slug] = cat
        return cats

    def seed_products(self, cats):
        path = settings.BASE_DIR / "catalog.json"
        entries = json.loads(path.read_text(encoding="utf-8"))
        for i, e in enumerate(entries):
            image = e.get("image") or ""
            product, _ = Product.objects.update_or_create(
                slug=e["handle"],
                defaults={
                    "name": e["name"],
                    "description": e.get("description", ""),
                    "price": Decimal(str(e["price"])),
                    "compare_price": Decimal(str(e["compare_price"])) if e.get("compare_price") else None,
                    "image": image,
                    "available": e.get("available", True),
                    "is_featured": i < 8,
                    "order": i,
                },
            )
            slugs = list(e.get("collections", []))
            for target, source in CURATIONS.items():
                if source in slugs and target not in slugs:
                    slugs.append(target)
            product.collections.set([cats[s] for s in slugs if s in cats])
        self.stdout.write(f"  products: {len(entries)}")

    def seed_home(self):
        for i, (title, image, link) in enumerate(HEROES):
            HeroSlide.objects.update_or_create(
                title=title, defaults={"image": image, "link": link, "order": i, "is_active": True},
            )
        for i, (title, image, link) in enumerate(CARDS):
            CategoryCard.objects.update_or_create(
                title=title, defaults={"image": image, "link": link, "order": i, "is_active": True},
            )
        for i, (title, image, link) in enumerate(EDITORIALS):
            EditorialBlock.objects.update_or_create(
                title=title, defaults={"image": image, "link": link, "order": i, "is_active": True},
            )
        captions = [
            "Inside the MNR bridal studio", "Hand embellishment in progress",
            "The atelier at work", "Bridal fitting", "Craft detail", "The finished ensemble",
        ]
        for i, caption in enumerate(captions, start=1):
            StudioImage.objects.update_or_create(
                order=i, defaults={"image": f"home/studio-{i}.jpg", "caption": caption},
            )

    def seed_pages(self):
        for title, slug, body in PAGES:
            Page.objects.update_or_create(slug=slug, defaults={"title": title, "body": body.strip()})

    def seed_admin(self):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "abidkamal336@gmail.com", "MNR@2026")
            self.stdout.write("  admin user created (admin / MNR@2026)")