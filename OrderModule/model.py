from db import orders_database
from datetime import datetime


def create_order_for_user(user_id: str):
    orders_database[f"client.{user_id}"].insert_one({
        "date": datetime.now(),
        "items": [],
        "status": "Initialized"
    })
