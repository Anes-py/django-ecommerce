# 🛍️ Django E-commerce Starter — RotiKala Template

This is my **first full-stack Django E-commerce** project, built with the **RotiKala ready-made template**, designed to demonstrate key features of a modern online store.

---

## 🚀 Features

✅ **Template Rendering**  
Fully responsive, clean, modern template powered by Django’s template system.

✅ **Product Catalog**  
Dynamic product listings with categories, specs, pricing, and discounts.

✅ **Shopping Cart**  
Supports **anonymous** (guest) and **authenticated** user carts.  
Add, remove, update quantities seamlessly.

✅ **Order & Payment**  
Complete checkout flow: address, shipping, payment.  
Order history for logged-in users.

✅ **Comment & Review System**  
Threaded comments and replies with user auth.

✅ **Admin Panel**  
Django’s admin for managing products, orders, users, comments.

✅ **Optimized Queries & Performance**  
- QuerySets optimized with **`select_related`** and **`prefetch_related`** to reduce database hits.
- Heavy views use **`only`** and **`defer`** for memory efficiency.
- Pagination for product lists to prevent large query loads.
- Caching for frequently accessed views (e.g. homepage, product detail).
- Clean indexes for models to ensure fast lookups.

✅ **SEO Friendly & Secure**  
- Clean URLs - slugs

---

## ⚙️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML5, TailwindCSS, JavaScript (Built with a ready-made template for fast deployment)
- **Database:** postgreSql/MySQL (changeable)
- **Auth:** Django built-in auth with custom tweaks
