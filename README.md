<div align="center">

# 🌿 GreenVibe

### A futuristic desktop plant store & AI-powered smart planner for Bangladesh
*Built with Python · PyQt6 · SQLite*

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-6.4%2B-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-F0C040?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-5.0-brightgreen?style=for-the-badge)

<br>

![SDG 11](https://img.shields.io/badge/SDG_11-Sustainable_Cities-FF6B00?style=flat-square)
![SDG 13](https://img.shields.io/badge/SDG_13-Climate_Action-3F7E44?style=flat-square)
![SDG 15](https://img.shields.io/badge/SDG_15-Life_on_Land-56C02B?style=flat-square)
![SDG 2](https://img.shields.io/badge/SDG_2-Zero_Hunger-DDA63A?style=flat-square)
![SDG 3](https://img.shields.io/badge/SDG_3-Good_Health-4C9F38?style=flat-square)

</div>

---

## 📖 About

**GreenVibe** is a full-featured desktop application for discovering, buying, and planning Bangladesh-native and tropical plants. It combines a photo-based plant store with a multi-mode AI-style smart planner, shopping cart, wishlist, order history, and personal plant notes — all backed by a local SQLite database with zero external setup.

Built with **PyQt6** for a native, high-performance UI with custom QSS stylesheets and 4 switchable colour themes. The app features 36 plants with Bengali names, seasonal calendars, care guides, and SDG alignment — designed for urban gardeners in Dhaka and across Bangladesh.

---

## ✨ Features

### 🏪 Plant Store
- Browse **36 plants** — Bangladesh-native, tropical, medicinal, ornamental, edible
- Every plant card shows: English name, **Bengali name (বাংলা)**, price, type, photo, tags, and truncated description
- Full **Plant Detail dialog** with large photo, care guide, badges, and personal notes
- **Advanced filters**: Sunlight level · Space type · Difficulty · Air Purifier · Edible · Fragrant
- **Live search bar**: search by English name, Bengali name, or description keyword
- Real-time card rendering; emoji fallback if photo is missing

### 📅 Smart Space Planner — 5 modes

| Mode | What it does |
|---|---|
| **Space** | Pick sunlight level + space type → personalised plant list + care tip + SDG note |
| **Season** | Pick the current month → see what's in peak season in Bangladesh right now |
| **Budget** | Pick your budget tier → plants that fit your wallet |
| **Purpose** | Pick a goal (Air Purifier / Fragrance / Edible / Privacy Screen etc.) → matching plants |
| **Skill** | Pick your experience level → Beginner / Intermediate / Expert plant list |

### 🛒 Shopping Cart
- Add from Store, Planner, Wishlist, or the Detail dialog
- View cart with timestamps and total price
- Place order (moves to Order History) or clear cart
- Fully persisted per user in SQLite

### 📦 Order History
- Full order log with order ID, items, total price, and timestamp
- Items stored as JSON; rendered in a clean scrollable list

### 💚 Wishlist
- One-click wishlist toggle on every plant card and in the detail popup
- Persistent per-user in SQLite
- Dedicated Wishlist screen to browse and act on saved plants

### 📝 Personal Plant Notes
- Write and save notes per plant, per user
- Accessible in the Plant Detail dialog
- Persisted in SQLite across sessions

### 🎨 4 Colour Themes

| Theme | Feel |
|---|---|
| **Forest Dark** | Deep green-black — the signature GreenVibe look |
| **Deep Ocean** | Dark blue-teal futuristic palette |
| **Midnight Purple** | Dark purple-green for night-mode lovers |
| **Light Garden** | Clean white and green for daytime use |

Switch themes live from ⚙ Settings — rebuilds the entire UI with no restart.

### 👤 Multi-user System
- Register and log in with persistent accounts
- Each user has completely separate cart, wishlist, notes, and order history
- Default account: `admin` / `1234`

---

## 🗂️ Project Structure

```
GreenVibe/
│
├── main.py              # All screens, widgets, theme engine — PyQt6
├── database.py          # SQLite schema, 36-plant seed data, all DB functions
├── planner.py           # Recommendation engine (space, season, budget, purpose, skill)
├── LAUNCH_APP.bat       # Windows one-click launcher — installs PyQt6, starts app
├── requirements.txt     # PyQt6>=6.4.0
├── greenvibe.db         # SQLite database (auto-created on first run)
│
└── assets/              # 36 plant photos + login hero background (37 files total)
    ├── hero_bg.png
    ├── snake.png        money.png        aloe.png         spider.png
    ├── rose.png         zz.png           peace.png        cactus.png
    ├── marigold.png     sunflower.png    krishnachura.png shapla.png
    ├── neem.png         tulsi.png        mehendi.png      kadam.png
    ├── bamboo.png       curryleaf.png    aparajita.png    brahmi.png
    ├── areca.png        paan.png         lemongrass.png   beli.png
    ├── gandharaj.png    joba.png         mint.png         moringa.png
    ├── bamboo_palm.png  duranta.png      periwinkle.png   moss_rose.png
    ├── crown_of_thorns.png  ixora.png   butterfly_pea.png  allamanda.png
```

---

## 🚀 Getting Started

### Option 1 — Double-click launcher *(Windows, recommended)*

```
Double-click LAUNCH_APP.bat
```

The launcher checks for Python, installs PyQt6 automatically if missing, then starts the app.

### Option 2 — Manual setup

**1. Clone the repository**
```bash
git clone https://github.com/AxisDe/GreenVibe.git
cd GreenVibe
```

**2. Install dependencies**
```bash
pip install PyQt6>=6.4.0
```

**3. Run**
```bash
python main.py
```

### Requirements

| Package | Version |
|---|---|
| Python | 3.10 or higher |
| PyQt6 | 6.4.0 or higher |

---

## 🔑 Default Login

| Username | Password |
|---|---|
| `admin` | `1234` |

You can register new accounts from the Login screen.

---

## 🌱 Full Plant Catalogue (36 Plants)

| # | English Name | Bengali | Type | Space | Light |
|---|---|---|---|---|---|
| 1 | Krishnachura | কৃষ্ণচূড়া | Native Flowering | Rooftop | High |
| 2 | Shapla | শাপলা | Aquatic | Balcony | High |
| 3 | Neem | নিম | Medicinal Tree | Rooftop | High |
| 4 | Tulsi | তুলসী | Medicinal Herb | Balcony | High |
| 5 | Mehendi | মেহেদী | Ornamental | Balcony | Medium |
| 6 | Kadam | কদম | Native Flowering | Rooftop | Medium |
| 7 | Bamboo | বাঁশ | Privacy Screen | Balcony | Low |
| 8 | Curry Leaf | কারি পাতা | Kitchen Herb | Balcony | High |
| 9 | Aparajita | অপরাজিতা | Climbing Flower | Balcony | High |
| 10 | Brahmi | ব্রাহ্মী | Medicinal Herb | Room | Medium |
| 11 | Areca Palm | আরেকা পাম | Air Purifier | Room | Medium |
| 12 | Paan | পান | Culinary Vine | Room | Low |
| 13 | Lemon Grass | লেমন গ্রাস | Herb | Rooftop | High |
| 14 | Jasmine (Beli) | বেলি ফুল | Fragrant Flower | Balcony | High |
| 15 | Gandharaj | গন্ধরাজ | Fragrant Flower | Balcony | Medium |
| 16 | Joba (Hibiscus) | জবা | Flowering Shrub | Rooftop | High |
| 17 | Mint | পুদিনা | Kitchen Herb | Room | Medium |
| 18 | Drumstick (Moringa) | সজনে | Nutritional Tree | Rooftop | High |
| 19 | Bamboo Palm | বাঁশ পাম | Indoor Palm | Room | Low |
| 20 | Duranta | দুরান্তা | Ornamental Hedge | Rooftop | High |
| 21 | Snake Plant | সর্পগাছ | Low Maintenance | Room | Low |
| 22 | Money Plant | মানি প্ল্যান্ট | Easy Care | Balcony | Medium |
| 23 | Aloe Vera | ঘৃতকুমারী | Medicinal | Room | Low |
| 24 | Spider Plant | স্পাইডার প্ল্যান্ট | Air Purifier | Balcony | Medium |
| 25 | Rose | গোলাপ | Outdoor Beauty | Balcony | High |
| 26 | ZZ Plant | জেডজেড প্ল্যান্ট | Low Maintenance | Room | Low |
| 27 | Peace Lily | শান্তি লিলি | Air Purifier | Room | Medium |
| 28 | Cactus | ক্যাকটাস | Easy Care | Rooftop | High |
| 29 | Marigold | গাঁদা ফুল | Outdoor Beauty | Rooftop | Medium |
| 30 | Sunflower | সূর্যমুখী | Outdoor Beauty | Rooftop | High |
| 31 | Madagascar Periwinkle | নয়নতারা | Flowering Shrub | Balcony | Full Sun |
| 32 | Moss Rose | টাইম ফুল | Succulent | Window Sill | High |
| 33 | Crown of Thorns | কাঁটামুকুটি | Succulent Shrub | Rooftop | High |
| 34 | Flame of the Woods (Ixora) | রঙ্গন | Evergreen Shrub | Garden | Partial–Full Sun |
| 35 | Butterfly Pea | অপরাজিতা | Climbing Vine | Railing | High |
| 36 | Golden Trumpet (Allamanda) | অ্যালমন্ডা | Vining Shrub | Rooftop | High |

---

## 🤖 Smart Planner — Space Mode Matrix

| Sunlight | Room | Balcony | Rooftop |
|---|---|---|---|
| **Low** | Snake Plant, ZZ Plant, Aloe Vera, Paan, Bamboo Palm | Snake Plant, ZZ Plant, Bamboo, Brahmi | Cactus, ZZ Plant, Bamboo Palm |
| **Medium** | Peace Lily, Money Plant, Areca Palm, Brahmi, Mint | Money Plant, Spider Plant, Mehendi, Gandharaj, Jasmine, Aparajita | Marigold, Rose, Kadam, Curry Leaf, Joba, Duranta |
| **High** | Aloe Vera, Snake Plant, Tulsi | Rose, Spider Plant, Aparajita, Joba, Jasmine, Mehendi, Lemon Grass | Sunflower, Marigold, Krishnachura, Neem, Moringa, Shapla, Joba, Duranta |

---

## 🗃️ Database Schema

Six tables, all created automatically on first run:

```sql
users        (id, username, password, created_at)

plants       (id, name, price, type, image, light, space, description,
              bengali, season, water_freq, difficulty,
              air_purifier, edible, fragrant, care_notes)

cart         (id, username, plant_name, price, qty, added_at)

wishlist     (id, username, plant_name, added_at)

plant_notes  (id, username, plant_name, note, updated_at)

orders       (id, username, items_json, total, placed_at)
```

---

## 🌍 SDG Alignment

| Goal | How GreenVibe contributes |
|---|---|
| **SDG 2** Zero Hunger | Edible plants (Moringa, Curry Leaf, Mint, Shapla, Aparajita) for urban food security |
| **SDG 3** Good Health | Medicinal plants (Tulsi, Neem, Aloe Vera, Brahmi); air purifier picks for indoor air quality |
| **SDG 11** Sustainable Cities | Urban greening — balcony, rooftop, and room gardens; natural sound and privacy screens |
| **SDG 13** Climate Action | Rooftop gardens reduce indoor temperature 4–6°C; carbon absorption promoted |
| **SDG 15** Life on Land | Bangladesh-native plant promotion; pollinator support (bees, butterflies) via flowering species |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | [PyQt6](https://pypi.org/project/PyQt6/) 6.4+ |
| Styling | Qt Stylesheets (QSS) — 4 custom themes, live switching |
| Signals | `pyqtSignal` for all cross-widget communication |
| Image handling | `QPixmap` with aspect-ratio-preserving centre-crop |
| Database | SQLite 3 via Python `sqlite3` stdlib — zero install |
| Language | Python 3.10+ |
| Launcher | Windows Batch Script |

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

Made with 🌿 by [AxisDe](https://github.com/AxisDe) — MD. Annafee Islam

*If you found this useful, drop a ⭐ on the repo!*

</div>
