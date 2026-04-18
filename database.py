
import sqlite3
import os

DB_PATH = "greenvibe.db"


# ─────────────────────────────────────────────────────────────────────────────
#  SCHEMA + SEED DATA
# ─────────────────────────────────────────────────────────────────────────────

PLANTS_DATA = [
    # (name, price, type, image, light, space, description, bengali, season, water_freq, difficulty, air_purifier, edible, fragrant, care_notes)
    # ── Original 10 (kept, descriptions expanded) ────────────────────────────
       ("Krishnachura",  400, "Native Flowering", "assets/krishnachura.png",
     "High",   "Rooftop", "Iconic BD tree with flame-red flower clusters in summer. National favourite; drought-resistant once established.",
     "কৃষ্ণচূড়া", "Apr–Jun", "Weekly (young)", "Intermediate", 0, 0, 0,
     "Grow in large container when young; transplant to ground when possible. Full sun essential."),

    ("Shapla",        350, "Aquatic",          "assets/shapla.png",
     "High",   "Balcony", "National flower of Bangladesh. Grows in water containers or small ponds on balconies.",
     "শাপলা", "Jul–Nov", "Aquatic",           "Intermediate", 0, 1, 0,
     "Keep in at least 15 cm of water. Full sun 6+ hours. Change water weekly to prevent mosquitoes."),

    ("Neem",          300, "Medicinal Tree",   "assets/neem.png",
     "High",   "Rooftop", "Ancient medicinal tree; leaves, bark and seeds all have uses. Natural pesticide. Fast grower.",
     "নিম", "Year-round", "Weekly",            "Beginner",  0, 1, 0,
     "Extremely heat and drought tolerant. Grow in large pots. Prune annually for compact shape."),

    ("Tulsi",         120, "Medicinal Herb",   "assets/tulsi.png",
     "High",   "Balcony", "Holy basil; revered in subcontinental culture. Anti-inflammatory, antiviral properties. Repels mosquitoes.",
     "তুলসী", "Year-round", "Daily",            "Beginner",  0, 1, 1,
     "Pinch flower buds to keep leaves productive. Needs 6+ hours sun. Replace plant every 2 years."),

    ("Mehendi",       150, "Ornamental",       "assets/mehendi.png",
     "Medium", "Balcony", "Henna plant — small fragrant white flowers; leaves yield natural dye. Heat-loving; perfect for BD.",
     "মেহেদী", "Apr–Sep", "2–3×/week",         "Beginner",  0, 0, 1,
     "Prune lightly for dense growth. Harvest leaves in morning. Can be shaped into a small hedge."),

    ("Kadam",         380, "Native Flowering", "assets/kadam.png",
     "Medium", "Rooftop", "Iconic monsoon tree; spherical white-yellow flowers appear with first rains. Deep cultural significance.",
     "কদম", "Jun–Sep", "Regular",              "Intermediate", 0, 0, 1,
     "Needs space to grow; best in large rooftop planters. Loves humidity and monsoon rain."),

    ("Bamboo",        250, "Privacy Screen",   "assets/bamboo.png",
     "Low",    "Balcony", "Clumping varieties perfect for balcony privacy screens. Fastest growing plant on earth.",
     "বাঁশ", "Year-round", "Regular",           "Beginner",  1, 0, 0,
     "Use clumping species (not running) for containers. Fertilise monthly. Can grow 30 cm/day in monsoon."),

    ("Curry Leaf",    180, "Kitchen Herb",     "assets/curryleaf.png",
     "High",   "Balcony", "Essential BD/South Asian cooking ingredient. Fresh leaves far superior to dried. Grows bushy in pots.",
     "কারি পাতা", "Year-round", "Regular",      "Beginner",  0, 1, 0,
     "Harvest sprigs from outer branches. Fertilise every 2 weeks in growing season. Protect from frost."),

    ("Aparajita",     100, "Climbing Flower",  "assets/aparajita.png",
     "High",   "Balcony", "Butterfly pea vine — electric blue flowers. Tea from flowers turns purple with lemon. Fast-growing.",
     "অপরাজিতা", "Mar–Nov", "Regular",          "Beginner",  0, 1, 0,
     "Train up trellis or railing. Self-seeds freely. Flowers used for natural food colouring."),

    ("Brahmi",        140, "Medicinal Herb",   "assets/brahmi.png",
     "Medium", "Room",    "Brain tonic herb. Grows as a creeping ground cover; thrives in moist conditions. Can float in water.",
     "ব্রাহ্মী", "Year-round", "Keep moist",    "Beginner",  0, 1, 0,
     "Loves humid conditions — great for bathroom windowsills. Use in herbal tea or salads."),

    ("Areca Palm",    450, "Air Purifier",     "assets/areca.png",
     "Medium", "Room",    "Top-rated NASA air purifier. Elegant feathery fronds. Humidifies dry rooms naturally.",
     "আরেকা পাম", "Year-round", "2–3×/week",    "Beginner",  1, 0, 0,
     "Keep out of direct sun — leaves will yellow. Flush soil monthly. Repot every 2 years."),

    ("Paan",          130, "Culinary Vine",    "assets/paan.png",
     "Low",    "Room",    "Betel leaf vine; iconic in BD culture. Glossy heart-shaped leaves. Grows in shaded spots indoors.",
     "পান", "Year-round", "Regular",            "Beginner",  0, 1, 0,
     "Needs support to climb. Keep soil consistently moist. Prefers indirect light — shade is fine."),

    ("Lemon Grass",   160, "Herb",             "assets/lemongrass.png",
     "High",   "Rooftop", "Citrusy aroma; used in cooking and natural mosquito repellent. Very low maintenance in BD climate.",
     "লেমন গ্রাস", "Year-round", "Regular",      "Beginner",  0, 1, 1,
     "Divide clumps every 2 years. Harvest outer stalks from base. Use fresh or freeze for cooking."),

    ("Jasmine (Beli)", 200, "Fragrant Flower",  "assets/beli.png",
     "High",   "Balcony", "Intensely fragrant small white flowers; iconic in BD weddings and garlands. Blooms May–October.",
     "বেলি ফুল", "May–Oct", "Daily",             "Intermediate", 0, 0, 1,
     "Train on trellis. Feed with phosphorus fertiliser for more blooms. Flowers fully at dusk."),

    ("Gandharaj",     220, "Fragrant Flower",  "assets/gandharaj.png",
     "Medium", "Balcony", "Gardenia relative with intoxicating white flowers. Fills entire balcony with fragrance at night.",
     "গন্ধরাজ", "Mar–Jun", "Regular",            "Intermediate", 0, 0, 1,
     "Acidic soil preferred. Avoid moving pot when budding. Yellowing leaves signal iron deficiency."),

    ("Joba (Hibiscus)", 170, "Flowering Shrub", "assets/joba.png",
     "High",   "Rooftop", "State flower of Malaysia; hugely popular in BD. Large trumpet blooms in red, pink, yellow. Rapid grower.",
     "জবা", "Year-round", "Daily",               "Beginner",  0, 0, 0,
     "Prune by 1/3 after flowering for bushy shape. Feed monthly. Flowers last one day but bloom in succession."),

    ("Mint",          110, "Kitchen Herb",     "assets/mint.png",
     "Medium", "Room",    "Refreshing herb for drinks, cooking and digestion. Grows aggressively — best in contained pots.",
     "পুদিনা", "Year-round", "Regular",           "Beginner",  0, 1, 1,
     "Keep separate from other herbs — spreads fast. Harvest just before flowering for best flavour."),

    ("Drumstick (Moringa)", 280, "Nutritional Tree", "assets/moringa.png",
     "High",   "Rooftop", "Superfood tree — leaves, pods all edible and extremely nutritious. Fast-growing; thrives in BD heat.",
     "সজনে", "Year-round", "Weekly",              "Beginner",  0, 1, 0,
     "Grows from cuttings easily. Harvest leaves regularly to keep tree compact. Drought-tolerant once established."),

    ("Bamboo Palm",   380, "Indoor Palm",      "assets/bamboo_palm.png",
     "Low",    "Room",    "Elegant multi-stem palm for low-light interiors. Excellent air purifier; releases moisture.",
     "বাঁশ পাম", "Year-round", "2×/week",         "Beginner",  1, 0, 0,
     "Never let roots sit in water. Mist fronds in dry season. Excellent for air-conditioned rooms."),

    ("Duranta",       190, "Ornamental Hedge", "assets/duranta.png",
     "High",   "Rooftop", "Ornamental shrub with purple flowers and golden berries. Popular rooftop hedge in Dhaka.",
     "দুরান্তা", "Year-round", "Regular",          "Beginner",  0, 0, 0,
     "Fast growing; prune hard for dense hedge. Berries are toxic — caution with children. Full sun."),

    ("Snake Plant",   300, "Low Maintenance",  "assets/snake.png",
     "Low",    "Room",    "Thrives in near-darkness; one of the best bedroom plants for oxygen at night. Extremely drought-tolerant.",
     "সর্পগাছ", "Year-round", "Weekly",       "Beginner",  1, 0, 0,
     "Water only when soil is completely dry. Wipe leaves monthly. Repot every 2–3 years."),

    ("Money Plant",   200, "Easy Care",        "assets/money.png",
     "Medium", "Balcony", "Rapid climber; grows in water or soil. Excellent air purifier removing formaldehyde and benzene.",
     "মানি প্ল্যান্ট", "Year-round", "2–3×/week", "Beginner",  1, 0, 0,
     "Pinch tips for bushier growth. Can propagate in a water jar. Keep out of direct noon sun."),

    ("Aloe Vera",     250, "Medicinal",        "assets/aloe.png",
     "Low",    "Room",    "Gel soothes burns and skin irritation. Needs very well-drained soil; root rot is the main risk.",
     "ঘৃতকুমারী/অ্যালোভেরা", "Year-round", "Fortnightly",  "Beginner",  0, 1, 0,
     "Use terracotta pots for best drainage. Never let it sit in water. Harvest outer leaves first."),

    ("Spider Plant",  280, "Air Purifier",     "assets/spider.png",
     "Medium", "Balcony", "NASA-listed top air purifier. Produces baby 'spiderettes' perfect for propagation.",
     "স্পাইডার প্ল্যান্ট", "Year-round", "Regular",    "Beginner",  1, 0, 0,
     "Hang in indirect light. Remove spiderettes to encourage mother plant. Mist occasionally in dry weather."),

    ("Rose",          350, "Outdoor Beauty",   "assets/rose.png",
     "High",   "Balcony", "Classic garden flower. Over 100 species. Requires pruning, feeding, and pest watch.",
     "গোলাপ", "Oct–Mar", "Daily",             "Intermediate", 0, 0, 1,
     "Prune dead blooms for continuous flowering. Feed with rose fertiliser monthly. Watch for aphids."),

    ("ZZ Plant",      320, "Low Maintenance",  "assets/zz.png",
     "Low",    "Room",    "Rhizome stores water — virtually unkillable. Glossy dark-green leaves add sophistication.",
     "জেডজেড প্ল্যান্ট", "Year-round", "Every 2–3 weeks", "Beginner", 0, 0, 0,
     "Tolerates neglect remarkably well. Toxic if ingested — keep away from pets. Dust leaves occasionally."),

    ("Peace Lily",    270, "Air Purifier",     "assets/peace.png",
     "Medium", "Room",    "One of few flowering plants for low-light rooms. White spathes bloom twice a year.",
     "শান্তি লিলি", "Twice/yr", "Keep moist",  "Beginner",  1, 0, 0,
     "Drooping leaves signal it needs water — a helpful indicator. Avoid cold draughts."),

    ("Cactus",        150, "Easy Care",        "assets/cactus.png",
     "High",   "Rooftop", "Desert survivor needing almost no care. Hundreds of varieties. Perfect for sunny rooftops.",
     "ক্যাকটাস", "Year-round", "Monthly",      "Beginner",  0, 0, 0,
     "Use gritty well-draining soil. Never overwater. Handle with thick gloves. Loves full sun."),

    ("Marigold",      180, "Outdoor Beauty",   "assets/marigold.png",
     "Medium", "Rooftop", "Natural insect repellent. Bright orange and yellow flowers; blooms nearly year-round in BD.",
     "গাঁদা ফুল", "Oct–Mar", "Daily",          "Beginner",  0, 0, 0,
     "Deadhead spent blooms to extend flowering. Plant near vegetables to deter pests. Water at base."),

    ("Sunflower",     160, "Outdoor Beauty",   "assets/sunflower.png",
     "High",   "Rooftop", "Heliotropic — tracks the sun. Edible seeds rich in nutrients. Grows 1–3 m tall.",
     "সূর্যমুখী", "Nov–Feb", "Daily",           "Beginner",  0, 1, 0,
     "Plant in deep containers if in pots. Stake tall varieties. Harvest seeds when head droops and petals fall."),
     

("Madagascar Periwinkle", 80, "Flowering Shrub", "assets/periwinkle.png", 
    "Full Sun", "Balcony", "Known for its medicinal properties and continuous blooming. Very hardy and drought-tolerant.", 
    "নয়নতারা", "Year-round", "Moderate", "Beginner", 0, 0, 1, 
    "Avoid overwatering as it is prone to root rot. Pinch tips for a bushier growth."),

("Moss Rose", 50, "Succulent/Groundcover", "assets/moss_rose.png", 
    "High", "Window Sill", "Produces vibrant, rose-like flowers that open only in sunlight. Thick, fleshy leaves store water.", 
    "টাইম ফুল / পনতুলাকা", "Summer", "Low", "Beginner", 0, 0, 1, 
    "Use well-draining sandy soil. Deadhead faded blooms to encourage more flowers."),

("Crown of Thorns", 250, "Succulent Shrub", "assets/crown_of_thorns.png", 
    "High", "Rooftop", "Slow-growing shrub with sharp thorns and colorful bracts. Extremely resilient to heat.", 
    "কাঁটামুকুটি", "Year-round", "Low", "Intermediate", 0, 0, 1, 
    "Handle with care due to thorns and milky sap which can be irritating. Water only when soil is dry."),

("Flame of the Woods", 150, "Evergreen Shrub", "assets/ixora.png", 
    "Partial to Full Sun", "Garden/Large Pot", "Features dense clusters of small, star-shaped flowers. Popular for hedges.", 
    "রঙ্গন", "Summer-Monsoon", "Regular", "Beginner", 0, 0, 1, 
    "Prefers slightly acidic soil. Prune after flowering to maintain its shape."),

("Butterfly Pea", 120, "Climbing Vine", "assets/butterfly_pea.png", 
    "High", "Railing/Trellis", "Famous for its vivid blue edible flowers. Used globally for herbal blue tea.", 
    "অপরাজিতা", "Year-round", "Daily", "Beginner", 0, 0, 1, 
    "Provide a support or trellis for the vine to climb. Regularly remove seed pods to keep it blooming."),

("Golden Trumpet", 200, "Vining Shrub", "assets/allamanda.png", 
    "High", "Rooftop/Fence", "Large, bright yellow trumpet-shaped flowers. Grows vigorously in tropical climates.", 
    "অ্যালমন্ডা / কলকে", "Summer-Monsoon", "Moderate", "Intermediate", 0, 0, 1, 
    "Needs plenty of space and sun. Prune in late winter to encourage vigorous spring growth."),
 
]

# ── Extended plant table columns ──────────────────────────────────────────────
CREATE_PLANTS = """
CREATE TABLE IF NOT EXISTS plants (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    price       INTEGER NOT NULL,
    type        TEXT    NOT NULL,
    image       TEXT    NOT NULL,
    light       TEXT,
    space       TEXT,
    description TEXT,
    bengali     TEXT,
    season      TEXT,
    water_freq  TEXT,
    difficulty  TEXT,
    air_purifier INTEGER DEFAULT 0,
    edible       INTEGER DEFAULT 0,
    fragrant     INTEGER DEFAULT 0,
    care_notes   TEXT
)
"""

CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT UNIQUE NOT NULL,
    password   TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_CART = """
CREATE TABLE IF NOT EXISTS cart (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT NOT NULL,
    plant_name TEXT NOT NULL,
    price      INTEGER NOT NULL,
    qty        INTEGER DEFAULT 1,
    added_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_WISHLIST = """
CREATE TABLE IF NOT EXISTS wishlist (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT NOT NULL,
    plant_name TEXT NOT NULL,
    added_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(username, plant_name)
)
"""

CREATE_NOTES = """
CREATE TABLE IF NOT EXISTS plant_notes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT NOT NULL,
    plant_name TEXT NOT NULL,
    note       TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_ORDERS = """
CREATE TABLE IF NOT EXISTS orders (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT NOT NULL,
    items_json TEXT NOT NULL,
    total      INTEGER NOT NULL,
    placed_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Execute CREATE statements one by one to avoid issues
    c.execute(CREATE_USERS)
    c.execute(CREATE_PLANTS)
    c.execute(CREATE_CART)
    c.execute(CREATE_WISHLIST)
    c.execute(CREATE_NOTES)
    c.execute(CREATE_ORDERS)

    # Default admin
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?,?)", ("admin", "1234"))

    # Seed plants — insert only if name doesn't already exist (prevents duplicate loop)
    for p in PLANTS_DATA:
        name = p[0]
        c.execute(
            "SELECT id FROM plants WHERE name=?", (name,)
        )
        if c.fetchone() is None:
            c.execute(
                """INSERT INTO plants
                   (name,price,type,image,light,space,description,
                    bengali,season,water_freq,difficulty,
                    air_purifier,edible,fragrant,care_notes)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                p
            )

    conn.commit()
    conn.close()


# ─────────────────────────────────────────────────────────────────────────────
#  QUERY HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _conn(): return sqlite3.connect(DB_PATH)


def get_all_plants():
    with _conn() as conn:
        return conn.execute("SELECT id,name,price,type,image,light,space,description,"
                            "bengali,season,water_freq,difficulty,"
                            "air_purifier,edible,fragrant,care_notes FROM plants ORDER BY id").fetchall()


def get_plants_by_filter(light=None, space=None, difficulty=None,
                          air_purifier=None, edible=None, fragrant=None,
                          search=None):
    query  = ("SELECT id,name,price,type,image,light,space,description,"
              "bengali,season,water_freq,difficulty,"
              "air_purifier,edible,fragrant,care_notes FROM plants WHERE 1=1")
    params = []
    if light:       query += " AND light=?";        params.append(light)
    if space:       query += " AND space=?";        params.append(space)
    if difficulty:  query += " AND difficulty=?";   params.append(difficulty)
    if air_purifier is not None:
        query += " AND air_purifier=?"; params.append(int(air_purifier))
    if edible is not None:
        query += " AND edible=?";       params.append(int(edible))
    if fragrant is not None:
        query += " AND fragrant=?";     params.append(int(fragrant))
    if search:
        query += " AND (name LIKE ? OR bengali LIKE ? OR description LIKE ?)"
        like = f"%{search}%"
        params.extend([like, like, like])
    query += " ORDER BY id"
    with _conn() as conn:
        return conn.execute(query, params).fetchall()


def validate_user(username, password):
    with _conn() as conn:
        return conn.execute(
            "SELECT 1 FROM users WHERE username=? AND password=?",
            (username, password)).fetchone() is not None


def register_user(username, password):
    try:
        with _conn() as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?,?)",
                         (username, password))
        return True
    except sqlite3.IntegrityError:
        return False


# Cart ─────────────────────────────────────────────────────────────────────────

def add_to_cart(username, plant_name, price):
    with _conn() as conn:
        conn.execute(
            "INSERT INTO cart (username,plant_name,price) VALUES (?,?,?)",
            (username, plant_name, price))


def get_cart(username):
    with _conn() as conn:
        return conn.execute(
            "SELECT plant_name,price,qty,added_at FROM cart WHERE username=? ORDER BY added_at DESC",
            (username,)).fetchall()


def remove_from_cart(username, plant_name):
    with _conn() as conn:
        conn.execute(
            "DELETE FROM cart WHERE username=? AND plant_name=? AND id=("
            "SELECT id FROM cart WHERE username=? AND plant_name=? LIMIT 1)",
            (username, plant_name, username, plant_name))


def clear_cart(username):
    with _conn() as conn:
        conn.execute("DELETE FROM cart WHERE username=?", (username,))


# Wishlist ─────────────────────────────────────────────────────────────────────

def toggle_wishlist(username, plant_name):
    with _conn() as conn:
        exists = conn.execute(
            "SELECT 1 FROM wishlist WHERE username=? AND plant_name=?",
            (username, plant_name)).fetchone()
        if exists:
            conn.execute(
                "DELETE FROM wishlist WHERE username=? AND plant_name=?",
                (username, plant_name))
            return False  # removed
        else:
            conn.execute(
                "INSERT INTO wishlist (username,plant_name) VALUES (?,?)",
                (username, plant_name))
            return True  # added


def get_wishlist(username):
    with _conn() as conn:
        return [r[0] for r in conn.execute(
            "SELECT plant_name FROM wishlist WHERE username=? ORDER BY added_at DESC",
            (username,)).fetchall()]


# Orders ───────────────────────────────────────────────────────────────────────

def place_order(username, items, total):
    import json
    with _conn() as conn:
        conn.execute(
            "INSERT INTO orders (username,items_json,total) VALUES (?,?,?)",
            (username, json.dumps(items), total))
    clear_cart(username)


def get_orders(username):
    import json
    with _conn() as conn:
        rows = conn.execute(
            "SELECT id,items_json,total,placed_at FROM orders WHERE username=? ORDER BY placed_at DESC",
            (username,)).fetchall()
    return [(r[0], json.loads(r[1]), r[2], r[3]) for r in rows]


# Plant notes ──────────────────────────────────────────────────────────────────

def save_note(username, plant_name, note):
    with _conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO plant_notes (username,plant_name,note,updated_at) "
            "VALUES (?,?,?,CURRENT_TIMESTAMP)",
            (username, plant_name, note))


def get_note(username, plant_name):
    with _conn() as conn:
        r = conn.execute(
            "SELECT note FROM plant_notes WHERE username=? AND plant_name=?",
            (username, plant_name)).fetchone()
    return r[0] if r else ""


# Stats ────────────────────────────────────────────────────────────────────────

def get_stats():
    with _conn() as conn:
        n_plants  = conn.execute("SELECT COUNT(*) FROM plants").fetchone()[0]
        n_users   = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        n_orders  = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        n_revenue = conn.execute("SELECT COALESCE(SUM(total),0) FROM orders").fetchone()[0]
    return {"plants": n_plants, "users": n_users,
            "orders": n_orders, "revenue": n_revenue}
