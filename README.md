# MNR — Mohsin Naveed Ranjha Design Studio

A responsive Django e-commerce store for the MNR bridal couture house: homepage carousel, shop-by-category rail, editorial grid, campaign video, studio gallery, collection pages with sorting and filtering, product pages, cart, cash-on-delivery checkout with WhatsApp confirmation, contact form and newsletter.

## Step by step — run locally

1. Install Python 3.13, then install the dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Apply the database migrations:

   ```
   python manage.py migrate
   ```

3. Load the store content (70 products, collections, homepage images and video, pages, admin user):

   ```
   python manage.py seed_mnr
   ```

   The database and all media files are included in this repository, so this step is optional on a fresh clone — run it only to reset content.

4. Start the server:

   ```
   python manage.py runserver
   ```

5. Open the site: http://127.0.0.1:8000/

## Admin

- URL: http://127.0.0.1:8000/admin/
- Username: `admin`
- Password: `MNR@2026`

From the admin you can manage products, prices, sale compare-prices, collections, orders (with status), homepage slides and category cards, editorial blocks, studio images, the campaign video, site settings, pages, contact messages and newsletter subscribers.

## Project layout

- `mnr/` — Django project (settings, URLs)
- `core/` — store app: models, views, forms, admin, seed command
- `templates/core/` — all storefront templates (Tailwind CSS via CDN, Jost typeface)
- `static/css/site.css` — palette, scrollbar, carousel and reveal animations
- `media/` — homepage assets, campaign video and product photography
- `catalog.json` — product source data used by `seed_mnr`

## Notes

- Checkout is cash on delivery; every order is confirmed over WhatsApp by the studio.
- Prices are in PKR.
- The layout is fully responsive from 320px phones to wide desktops.