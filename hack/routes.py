from hack import app, db
from hack.tables import CallLog
from datetime import datetime, timedelta
import random

# Sample device IDs and common phone numbers
device_ids = ['123', '456', '789']
common_numbers = [f"9{random.randint(100000000, 999999999)}" for _ in range(3)]  # 3 common numbers


@app.route('/')
def add_data():
    with app.app_context():
        for i in range(50):
            # Randomly pick device_id
            device_id = random.choice(device_ids)

            # Add logic for generating calls between different devices and common numbers
            if random.random() < 0.5:  # 50% chance to have a common number between two devices
                number = random.choice(common_numbers)
            else:
                number = f"9{random.randint(100000000, 999999999)}"  # Random number for other cases

            # Ensure the same device calls the same number continuously 6 to 7 times
            if random.random() < 0.3:  # 30% chance to have a continuous call sequence
                number = random.choice(common_numbers)
                call_count = random.randint(6, 7)  # Call count between 6 and 7 times
                for _ in range(call_count):
                    new_log = CallLog(
                        device_id=device_id,
                        number=number,
                        duration=random.randint(30, 300),
                        timestamp=(datetime.now() - timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S"),
                        type=random.choice(["incoming", "outgoing", "missed"])
                    )
                    db.session.add(new_log)
            else:
                new_log = CallLog(
                    device_id=device_id,
                    number=number,
                    duration=random.randint(30, 300),
                    timestamp=(datetime.now() - timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S"),
                    type=random.choice(["incoming", "outgoing", "missed"])
                )
                db.session.add(new_log)

        db.session.commit()

    return "✅ Added 50 call logs!"







