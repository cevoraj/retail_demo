SKUS = {
    "Product": {},
    "General cleaning":{
    "SKU":{},
    "P&G-CLN-001": {
        "brand": "Procter & Gamble",
        "name": "Dish Soap – Lemon Fresh",
        "description": "A citrus-scented liquid soap designed to cut through grease.",
        "price_gbp": 2.50,
        "packaging": "500ml bottle",
        "competitor_price_gbp": 2.30,
        "units_sold_last_week": 480,
        "margin_per_unit_gbp": 0.80,
        "price_elasticity_slope": -0.5  # Inelastic staple
    },
    "P&G-CLN-002": {
        "brand": "Procter & Gamble",
        "name": "Laundry Detergent – Regular",
        "description": "Powerful detergent for tough stains and fresh clothes.",
        "price_gbp": 6.99,
        "packaging": "2L bottle",
        "competitor_price_gbp": 7.49,
        "units_sold_last_week": 220,
        "margin_per_unit_gbp": 1.50,
        "price_elasticity_slope": -0.6
    },
    "P&G-CLN-003": {
        "brand": "Procter & Gamble",
        "name": "Fabric Softener – Fresh Linen",
        "description": "Softens fabrics and leaves a fresh linen scent.",
        "price_gbp": 3.25,
        "packaging": "1L bottle",
        "competitor_price_gbp": 3.10,
        "units_sold_last_week": 310,
        "margin_per_unit_gbp": 1.10,
        "price_elasticity_slope": -1.1
    },
    "P&G-CLN-004": {
        "brand": "Procter & Gamble",
        "name": "Disinfectant Spray – Antibacterial",
        "description": "Kills 99.9% of germs on hard surfaces.",
        "price_gbp": 4.50,
        "packaging": "750ml spray",
        "competitor_price_gbp": 4.80,
        "units_sold_last_week": 190,
        "margin_per_unit_gbp": 1.60,
        "price_elasticity_slope": -1.3
    },
    "P&G-CLN-005": {
        "brand": "Procter & Gamble",
        "name": "Floor Cleaner – Pine Scent",
        "description": "Multi-surface cleaner with a refreshing pine scent.",
        "price_gbp": 3.75,
        "packaging": "1L bottle",
        "competitor_price_gbp": 3.50,
        "units_sold_last_week": 280,
        "margin_per_unit_gbp": 0.90,
        "price_elasticity_slope": -1.4
    },
    "UNL-CLN-006": {
        "brand": "Unilever",
        "name": "Dish Soap – Unscented",
        "description": "Gentle and effective grease removal, fragrance-free.",
        "price_gbp": 2.30,
        "packaging": "500ml bottle",
        "competitor_price_gbp": 2.50,
        "units_sold_last_week": 410,
        "margin_per_unit_gbp": 0.70,
        "price_elasticity_slope": -0.7
    },
    "UNL-CLN-007": {
        "brand": "Unilever",
        "name": "Multi-Surface Spray – Citrus",
        "description": "Removes dirt and grease, leaving a citrus aroma.",
        "price_gbp": 3.90,
        "packaging": "750ml spray",
        "competitor_price_gbp": 3.80,
        "units_sold_last_week": 260,
        "margin_per_unit_gbp": 1.20,
        "price_elasticity_slope": -1.2
    },
    "UNL-CLN-008": {
        "brand": "Unilever",
        "name": "Toilet Bowl Cleaner – Bleach",
        "description": "Thick bleach formula removes limescale and kills germs.",
        "price_gbp": 2.99,
        "packaging": "750ml bottle",
        "competitor_price_gbp": 2.79,
        "units_sold_last_week": 370,
        "margin_per_unit_gbp": 0.95,
        "price_elasticity_slope": -0.8
    },
    "UNL-CLN-009": {
        "brand": "Unilever",
        "name": "Bathroom Mold Remover",
        "description": "Quickly removes black mold from tiles and grout.",
        "price_gbp": 4.10,
        "packaging": "500ml spray",
        "competitor_price_gbp": 4.30,
        "units_sold_last_week": 150,
        "margin_per_unit_gbp": 1.40,
        "price_elasticity_slope": -1.8
    },
    "UNL-CLN-010": {
        "brand": "Unilever",
        "name": "Carpet Stain Remover",
        "description": "Removes stubborn carpet stains, safe for most fabrics.",
        "price_gbp": 5.25,
        "packaging": "500ml spray",
        "competitor_price_gbp": 5.50,
        "units_sold_last_week": 130,
        "margin_per_unit_gbp": 1.80,
        "price_elasticity_slope": -2.0
    },
    "RBK-CLN-011": {
        "brand": "Reckitt Benckiser",
        "name": "Glass Cleaner – Streak-Free",
        "description": "Shiny, streak-free finish for windows and mirrors.",
        "price_gbp": 3.10,
        "packaging": "750ml spray",
        "competitor_price_gbp": 3.25,
        "units_sold_last_week": 290,
        "margin_per_unit_gbp": 1.00,
        "price_elasticity_slope": -1.3
    },
    "RBK-CLN-012": {
        "brand": "Reckitt Benckiser",
        "name": "Kitchen Degreaser – Heavy Duty",
        "description": "Removes stubborn kitchen grease and residue.",
        "price_gbp": 4.60,
        "packaging": "500ml spray",
        "competitor_price_gbp": 4.40,
        "units_sold_last_week": 210,
        "margin_per_unit_gbp": 1.55,
        "price_elasticity_slope": -1.5
    },
    "RBK-CLN-013": {
        "brand": "Reckitt Benckiser",
        "name": "Oven Cleaner – Heavy Duty",
        "description": "Foaming cleaner for tough baked-on grease.",
        "price_gbp": 5.90,
        "packaging": "500ml spray",
        "competitor_price_gbp": 6.10,
        "units_sold_last_week": 170,
        "margin_per_unit_gbp": 2.00,
        "price_elasticity_slope": -1.6
    },
    "RBK-CLN-014": {
        "brand": "Reckitt Benckiser",
        "name": "Disinfectant Wipes – 50 Pack",
        "description": "Quick-clean wipes for high-touch surfaces.",
        "price_gbp": 3.50,
        "packaging": "50 wipes pack",
        "competitor_price_gbp": 3.60,
        "units_sold_last_week": 320,
        "margin_per_unit_gbp": 1.10,
        "price_elasticity_slope": -1.1
    },
    "CLN-CLN-015": {
        "brand": "Clorox",
        "name": "Toilet Bowl Cleaner – Eco-Friendly",
        "description": "Plant-based formula cleans and deodorizes toilets.",
        "price_gbp": 3.20,
        "packaging": "750ml bottle",
        "competitor_price_gbp": 3.40,
        "units_sold_last_week": 200,
        "margin_per_unit_gbp": 1.00,
        "price_elasticity_slope": -0.9
    },
    "CLN-CLN-016": {
        "brand": "Clorox",
        "name": "Drain Cleaner – Gel Formula",
        "description": "Thick gel dissolves clogs and removes odors.",
        "price_gbp": 4.75,
        "packaging": "1L bottle",
        "competitor_price_gbp": 4.50,
        "units_sold_last_week": 180,
        "margin_per_unit_gbp": 1.70,
        "price_elasticity_slope": -1.4
    },
    "CLN-CLN-017": {
        "brand": "Clorox",
        "name": "Stainless Steel Polish",
        "description": "Polishes stainless steel surfaces to a streak-free shine.",
        "price_gbp": 5.10,
        "packaging": "500ml spray",
        "competitor_price_gbp": 5.20,
        "units_sold_last_week": 160,
        "margin_per_unit_gbp": 1.90,
        "price_elasticity_slope": -2.1
    },
    "CLN-CLN-018": {
        "brand": "Clorox",
        "name": "Air Freshener – Ocean Breeze",
        "description": "Long-lasting ocean-inspired room fragrance.",
        "price_gbp": 2.90,
        "packaging": "300ml spray",
        "competitor_price_gbp": 3.00,
        "units_sold_last_week": 410,
        "margin_per_unit_gbp": 0.85,
        "price_elasticity_slope": -1.2
    },
    "CLN-CLN-019": {
        "brand": "Clorox",
        "name": "Air Freshener – Lavender",
        "description": "Soothing lavender scent, lasting up to 30 days.",
        "price_gbp": 2.95,
        "packaging": "300ml spray",
        "competitor_price_gbp": 2.85,
        "units_sold_last_week": 390,
        "margin_per_unit_gbp": 0.90,
        "price_elasticity_slope": -1.3
    },
    "SCJ-CLN-020": {
        "brand": "SC Johnson",
        "name": "Disinfectant Spray – Citrus Fresh",
        "description": "Cleans and disinfects with a citrus aroma.",
        "price_gbp": 4.20,
        "packaging": "750ml spray",
        "competitor_price_gbp": 4.00,
        "units_sold_last_week": 230,
        "margin_per_unit_gbp": 1.50,
        "price_elasticity_slope": -1.4
    }
}
}