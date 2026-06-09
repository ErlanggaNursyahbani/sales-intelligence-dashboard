import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# Config
N = 500
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)

PRODUCTS = {
    "Sepatu Lari Nike": {"category": "Footwear", "base_price": 850000},
    "Kaos Polos Uniqlo": {"category": "Apparel", "base_price": 299000},
    "Tas Ransel Eiger": {"category": "Bags", "base_price": 650000},
    "Jaket Fleece": {"category": "Apparel", "base_price": 450000},
    "Sandal Jepit Havaianas": {"category": "Footwear", "base_price": 180000},
    "Celana Jogger": {"category": "Apparel", "base_price": 320000},
    "Topi Baseball": {"category": "Accessories", "base_price": 150000},
    "Kacamata Sunglasses": {"category": "Accessories", "base_price": 520000},
    "Sepatu Formal Bata": {"category": "Footwear", "base_price": 720000},
    "Tas Selempang": {"category": "Bags", "base_price": 380000},
}

CITIES = ["Jakarta", "Surabaya", "Bandung", "Medan", "Makassar", "Semarang", "Yogyakarta", "Palembang"]
CHANNELS = ["Tokopedia", "Shopee", "Website", "Instagram Shop"]

# Seasonal multipliers per month (simulate trend)
MONTHLY_MULTIPLIER = {
    1: 0.8, 2: 0.75, 3: 0.9, 4: 0.85,
    5: 1.0, 6: 1.3,   # Lebaran spike
    7: 0.9, 8: 0.95, 9: 1.0, 10: 1.1,
    11: 1.4, 12: 1.5  # Harbolnas + Nataru
}

rows = []
for i in range(N):
    date = START_DATE + timedelta(days=random.randint(0, 364))
    product_name = random.choice(list(PRODUCTS.keys()))
    product = PRODUCTS[product_name]

    multiplier = MONTHLY_MULTIPLIER[date.month]
    qty = max(1, int(np.random.poisson(2) * multiplier))
    discount_pct = random.choice([0, 0, 0, 5, 10, 15, 20, 25])
    base_price = product["base_price"]
    final_price = base_price * (1 - discount_pct / 100)
    revenue = round(final_price * qty)

    rows.append({
        "order_id": f"ORD-{10000 + i}",
        "date": date.strftime("%Y-%m-%d"),
        "month": date.strftime("%B"),
        "month_num": date.month,
        "product": product_name,
        "category": product["category"],
        "qty": qty,
        "unit_price": base_price,
        "discount_pct": discount_pct,
        "revenue": revenue,
        "city": random.choice(CITIES),
        "channel": random.choices(
            CHANNELS,
            weights=[0.35, 0.35, 0.2, 0.1]  # Tokped & Shopee dominant
        )[0],
        "rating": round(random.uniform(3.5, 5.0), 1),
    })

df = pd.DataFrame(rows)
df = df.sort_values("date").reset_index(drop=True)
df.to_csv("data/sales_data.csv", index=False)

print(f"✓ Dataset generated: {len(df)} rows")
print(f"✓ Date range: {df['date'].min()} → {df['date'].max()}")
print(f"✓ Total revenue: Rp {df['revenue'].sum():,.0f}")
print(f"\nSample:\n{df.head(3).to_string()}")
