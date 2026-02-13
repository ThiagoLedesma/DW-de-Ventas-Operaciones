import json
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

NUM_ORDERS = 500
MAX_ITEMS_PER_ORDER = 4

CATEGORIES = ["Electronics", "electronics", "Home", "Sports", "Fashion"]
PAYMENT_METHODS = ["credit_card", "debit_card", "paypal", "transfer"]
SHIPPING_STATUS = ["pending", "shipped", "delivered", None]

BRANDS = ["LogiTech", "HyperType", "SportX", "HomePro", "UrbanStyle"]

def random_date_within_last_year():
    start_date = datetime.now() - timedelta(days=365)
    random_days = random.randint(0, 365)
    return (start_date + timedelta(days=random_days)).isoformat()

def generate_product():
    return {
        "product_id": f"P-{random.randint(100,999)}",
        "product_name": fake.word().capitalize() + " " + fake.word().capitalize(),
        "category": random.choice(CATEGORIES),
        "brand": random.choice(BRANDS),
        "quantity": random.randint(1, 3),
        "unit_price": random.choice([
            round(random.uniform(10, 200), 2),
            str(round(random.uniform(10, 200), 2))  # intencionalmente string
        ])
    }

def generate_customer():
    return {
        "customer_id": f"C-{random.randint(1000, 1999)}",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email().upper() if random.random() < 0.2 else fake.email(),
        "city": fake.city(),
        "country": "Argentina",
        "signup_date": fake.date_between(start_date="-2y", end_date="today").isoformat()
    }

def generate_order():
    return {
        "order_id": f"ORD-{uuid.uuid4().hex[:8]}",
        "order_date": random_date_within_last_year(),
        "customer": generate_customer(),
        "payment": {
            "method": random.choice(PAYMENT_METHODS),
            "installments": random.choice([1, 3, 6])
        },
        "shipping": {
            "status": random.choice(SHIPPING_STATUS),
            "shipping_cost": round(random.uniform(3, 15), 2)
        },
        "items": [generate_product() for _ in range(random.randint(1, MAX_ITEMS_PER_ORDER))]
    }

def main():
    orders = [generate_order() for _ in range(NUM_ORDERS)]

    with open("data/raw/orders.json", "w") as f:
        json.dump(orders, f, indent=2)

    print(f"Generated {NUM_ORDERS} orders successfully.")

if __name__ == "__main__":
    main()
