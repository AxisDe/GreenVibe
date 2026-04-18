

from typing import Tuple


# ─────────────────────────────────────────────────────────────────────────────
#  RECOMMENDATION DATABASE
#  Structure: (light, space) → (plant_list, care_tip, seasonal_tip, sdg_note)
# ─────────────────────────────────────────────────────────────────────────────

RECOMMENDATIONS = {
    ("Low", "Room"): (
        ["Snake Plant", "ZZ Plant", "Aloe Vera", "Paan", "Bamboo Palm"],
        "These plants thrive in rooms with minimal natural light — perfect for Dhaka apartments with north-facing windows.",
        "In monsoon season, reduce watering by half as humidity is naturally high.",
        "These plants remove indoor pollutants (formaldehyde, benzene) — directly supporting SDG 3 (Good Health)."
    ),
    ("Low", "Balcony"): (
        ["Snake Plant", "ZZ Plant", "Bamboo", "Brahmi"],
        "Shaded balconies facing away from direct sun suit these resilient species perfectly.",
        "Bamboo grows fastest in monsoon — expect up to 10–15 cm per week June–August.",
        "Bamboo on balconies creates natural sound barriers and cooling — supporting SDG 11 (Sustainable Cities)."
    ),
    ("Low", "Rooftop"): (
        ["Cactus", "ZZ Plant", "Bamboo Palm"],
        "Even with shade from adjacent buildings, these species manage well with diffused light.",
        "Cacti enter a natural dormancy in Bangladesh's brief cool season (Dec–Jan) — reduce watering to once every 6 weeks.",
        "Rooftop greenery reduces urban heat island effect by up to 3°C — SDG 13 (Climate Action)."
    ),
    ("Medium", "Room"): (
        ["Peace Lily", "Money Plant", "Areca Palm", "Brahmi", "Mint"],
        "These flourish in rooms with east or west-facing windows — 3–5 hours of indirect sun daily.",
        "In summer (Apr–Jun), rotate pots 180° monthly so all sides receive equal light.",
        "Areca Palm releases moisture into dry air-conditioned rooms, reducing the need for humidifiers — SDG 12 (Responsible Consumption)."
    ),
    ("Medium", "Balcony"): (
        ["Money Plant", "Spider Plant", "Mehendi", "Gandharaj", "Jasmine (Beli)", "Aparajita"],
        "East-facing balconies in Dhaka get ideal morning sun followed by afternoon shade — perfect for these species.",
        "Gandharaj and Jasmine bloom most intensely in spring (Mar–May) — this is the best time to take cuttings.",
        "Flowering balcony plants support urban pollinators — bees and butterflies — contributing to SDG 15 (Life on Land)."
    ),
    ("Medium", "Rooftop"): (
        ["Marigold", "Rose", "Kadam", "Curry Leaf", "Joba (Hibiscus)", "Duranta"],
        "Rooftops with partial shade from water tanks or neighbouring structures suit these moderate-sun lovers.",
        "Kadam blooms with the first monsoon rains (June) — a uniquely Bangladeshi experience. Ensure large containers.",
        "Marigold acts as a natural pesticide for neighbouring edible plants — reducing chemical use (SDG 2, Zero Hunger)."
    ),
    ("High", "Room"): (
        ["Aloe Vera", "Snake Plant", "Tulsi"],
        "A south-facing room window in Dhaka can provide 6+ hours of direct light — enough for these sun-lovers.",
        "Tulsi in a sunny windowsill repels mosquitoes naturally — valuable in monsoon season.",
        "Growing medicinal herbs like Tulsi and Aloe at home reduces pharmaceutical dependency (SDG 3)."
    ),
    ("High", "Balcony"): (
        ["Rose", "Spider Plant", "Aparajita", "Joba (Hibiscus)", "Jasmine (Beli)", "Mehendi", "Lemon Grass"],
        "South-facing Dhaka balconies receive 8+ hours of sun — ideal for these flowering and herbal species.",
        "Lemon Grass planted at balcony edges acts as a natural mosquito barrier — most effective June–October.",
        "Edible herbs and flowering plants on balconies contribute to urban food security (SDG 2) and biodiversity (SDG 15)."
    ),
    ("High", "Rooftop"): (
        ["Sunflower", "Marigold", "Krishnachura", "Neem", "Drumstick (Moringa)",
         "Shapla", "Joba (Hibiscus)", "Duranta"],
        "Open rooftops in Dhaka are ideal mini-farms. The combination of sun, breeze and space produces stunning results.",
        "Moringa grows up to 3 m in a single season in Bangladesh — harvest leaves weekly and pods when finger-length.",
        "Rooftop gardens in Dhaka can reduce indoor temperature by 4–6°C — critical climate adaptation (SDG 13)."
    ),
}

# Seasonal calendar for Bangladesh
SEASONAL_CALENDAR = {
    "Jan": ["Rose", "Marigold", "Sunflower"],
    "Feb": ["Rose", "Marigold", "Tulsi", "Mehendi"],
    "Mar": ["Jasmine (Beli)", "Aparajita", "Gandharaj", "Tulsi"],
    "Apr": ["Krishnachura", "Jasmine (Beli)", "Joba (Hibiscus)"],
    "May": ["Krishnachura", "Shapla", "Aparajita", "Jasmine (Beli)"],
    "Jun": ["Kadam", "Shapla", "Bamboo", "Drumstick (Moringa)"],
    "Jul": ["Kadam", "Shapla", "Curry Leaf"],
    "Aug": ["Shapla", "Drumstick (Moringa)", "Lemon Grass"],
    "Sep": ["Joba (Hibiscus)", "Lemon Grass", "Aparajita"],
    "Oct": ["Rose", "Marigold", "Joba (Hibiscus)"],
    "Nov": ["Sunflower", "Marigold", "Rose"],
    "Dec": ["Sunflower", "Rose", "Marigold"],
}

# Budget tiers
BUDGET_SUGGESTIONS = {
    "Under ৳500":  ["Tulsi", "Mint", "Marigold", "Aparajita", "Cactus"],
    "৳500–৳1000": ["Snake Plant", "Money Plant", "Aloe Vera", "Mehendi", "Lemon Grass"],
    "৳1000–৳2000":["Spider Plant", "Peace Lily", "ZZ Plant", "Rose", "Curry Leaf"],
    "৳2000+":     ["Areca Palm", "Krishnachura", "Bamboo", "Shapla", "Drumstick (Moringa)"],
}

# Purpose-based suggestions
PURPOSE_SUGGESTIONS = {
    "Air Purification":  ["Snake Plant", "Areca Palm", "Peace Lily", "Bamboo Palm", "Spider Plant", "Money Plant"],
    "Fragrance":        ["Jasmine (Beli)", "Gandharaj", "Tulsi", "Lemon Grass", "Rose", "Mehendi"],
    "Edible / Kitchen": ["Mint", "Tulsi", "Curry Leaf", "Aparajita", "Drumstick (Moringa)", "Shapla"],
    "Beginner Friendly":["Snake Plant", "Money Plant", "Cactus", "ZZ Plant", "Marigold", "Joba (Hibiscus)"],
    "Mosquito Repellent":["Tulsi", "Lemon Grass", "Marigold", "Neem", "Citronella"],
    "Privacy Screen":   ["Bamboo", "Areca Palm", "Duranta", "Bamboo Palm"],
    "Native to Bangladesh":["Krishnachura", "Shapla", "Kadam", "Tulsi", "Neem", "Gandharaj", "Joba (Hibiscus)"],
}

# Care difficulty guide
DIFFICULTY_TIPS = {
    "Beginner":     "Great starting point! These plants forgive occasional missed watering and tolerate variable light.",
    "Intermediate": "Needs regular attention — consistent watering, monthly feeding, and seasonal pruning. Worth the effort!",
    "Expert":       "For experienced gardeners. Precise watering schedules, specific soil mixes, and pest vigilance required.",
}


def get_recommendation(light: str, space: str) -> Tuple[str, str, str, str]:
    """
    Returns (plant_names_csv, care_tip, seasonal_tip, sdg_note).
    """
    key = (light.strip().capitalize(), space.strip().capitalize())
    if key in RECOMMENDATIONS:
        plants, care, seasonal, sdg = RECOMMENDATIONS[key]
        return ", ".join(plants), care, seasonal, sdg
    return ("Snake Plant, Money Plant",
            "These versatile plants work well in almost any condition.",
            "Water regularly and keep out of extreme temperatures.",
            "All plants contribute to SDG 15 — Life on Land.")


def get_seasonal_plants(month: str) -> list:
    """Return list of plant names best for the given month abbreviation."""
    return SEASONAL_CALENDAR.get(month, [])


def get_budget_suggestions(tier: str) -> list:
    return BUDGET_SUGGESTIONS.get(tier, [])


def get_purpose_suggestions(purpose: str) -> list:
    return PURPOSE_SUGGESTIONS.get(purpose, [])


def get_all_purposes() -> list:
    return list(PURPOSE_SUGGESTIONS.keys())


def get_all_budget_tiers() -> list:
    return list(BUDGET_SUGGESTIONS.keys())


def get_difficulty_tip(difficulty: str) -> str:
    return DIFFICULTY_TIPS.get(difficulty, "")
