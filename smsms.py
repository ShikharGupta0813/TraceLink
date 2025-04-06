from hack import app, db
from hack.tables import SMS
from datetime import datetime, timedelta
import random

def add_dummy_sms_data():
    with app.app_context():
        for i in range(50):
            new_sms = SMS(
                device_id=random.randint(100, 999),  # Replace with actual logic if needed
                sender=f"9{random.randint(100000000, 999999999)}",
                message_body=f"This is a dummy message {i + 1}",
                timestamp=(datetime.now() - timedelta(minutes=i)),  # Use datetime object directly
                message_type=random.choice(["incoming", "outgoing", "missed"])  # Example types
            )
            db.session.add(new_sms)

        db.session.commit()
    print("✅ Added 50 SMS entries!")

# Call this function wherever needed
add_dummy_sms_data()
