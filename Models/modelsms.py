import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from datetime import datetime

# Step 1: Connect to DB
conn = sqlite3.connect("../instance/database.db")

# Step 2: Fetch SMS logs for all devices
query = """
SELECT * FROM SMS
"""
sms_logs = pd.read_sql_query(query, conn)

conn.close()

# Step 3: Preprocess the data
sms_logs['timestamp'] = pd.to_datetime(sms_logs['timestamp'])
sms_logs['hour'] = sms_logs['timestamp'].dt.hour
sms_logs['day'] = sms_logs['timestamp'].dt.dayofweek
sms_logs['month'] = sms_logs['timestamp'].dt.month
sms_logs['message_length'] = sms_logs['message_body'].apply(lambda x: len(str(x)))
sms_logs['message_type'] = sms_logs['message_type'].astype('category')

# Step 4: Aggregate SMS statistics per device
device_sms_summary = sms_logs.groupby(['device_id', 'sender']).agg(
    total_sms=('message_body', 'count'),
    avg_message_length=('message_length', 'mean'),
    sms_per_hour=('hour', 'count'),
    sms_per_day=('day', 'count'),
    sms_per_month=('month', 'count')
).reset_index()

# 1. **Excessive Messaging Activity**
# Identify senders or devices with unusually high SMS volume
threshold = device_sms_summary['total_sms'].mean() + 3 * device_sms_summary['total_sms'].std()
suspicious_activity = device_sms_summary[device_sms_summary['total_sms'] > threshold]
print("\nSuspicious Devices/Senders with Excessive Messages:")
print(suspicious_activity[['device_id', 'sender', 'total_sms']])

# Written Insight: Excessive Messaging Activity
print("\nWritten Insight: Excessive Messaging Activity")
for index, row in suspicious_activity.iterrows():
    print(f"Device ID: {row['device_id']}, Sender: {row['sender']} has sent {row['total_sms']} messages, which is suspicious.")

# 2. **Message Pattern Similarities**
# Find similar messages between two devices (repeat messages)
# We will consider exact same message content sent between two devices or senders

# Group messages by sender and receiver (sender, recipient pairs)
message_pairs = sms_logs.groupby(['sender', 'device_id'])['message_body'].apply(lambda x: ' '.join(x)).reset_index()
# Check for duplicate message content
duplicate_messages = message_pairs[message_pairs.duplicated(subset=['message_body'], keep=False)]

print("\nDevices/Senders Sending the Same Messages to Each Other:")
print(duplicate_messages[['sender', 'device_id', 'message_body']])

# Written Insight: Message Pattern Similarities
print("\nWritten Insight: Message Pattern Similarities")
for index, row in duplicate_messages.iterrows():
    print(f"Sender {row['sender']} and Device {row['device_id']} sent the same message: '{row['message_body']}'")

# 3. **Frequent Communication Between Specific Senders**
# Find senders that communicate frequently with each other
communication_count = sms_logs.groupby(['sender', 'device_id']).size().reset_index(name='communication_count')

# Find the top communication pairs (senders and receivers)
top_communication_pairs = communication_count.nlargest(10, 'communication_count')

print("\nTop 10 Communication Pairs (Frequent Communication Between Senders and Devices):")
print(top_communication_pairs[['sender', 'device_id', 'communication_count']])

# Written Insight: Frequent Communication Between Specific Senders
print("\nWritten Insight: Frequent Communication Between Specific Senders")
for index, row in top_communication_pairs.iterrows():
    print(f"Sender {row['sender']} communicated with Device {row['device_id']} {row['communication_count']} times.")

# 4. **Unusual Timing Patterns**
# Find senders who send messages at unusual hours (e.g., late at night or early morning)
# Defining "unusual" as messages sent between 12am and 6am
unusual_hours = sms_logs[sms_logs['hour'] < 6]

# Count of messages sent during unusual hours
unusual_activity = unusual_hours.groupby(['sender', 'device_id']).size().reset_index(name='unusual_hour_sms_count')

print("\nSenders with High Activity During Unusual Hours (12 AM - 6 AM):")
print(unusual_activity[['sender', 'device_id', 'unusual_hour_sms_count']])

# Written Insight: Unusual Timing Patterns
print("\nWritten Insight: Unusual Timing Patterns")
for index, row in unusual_activity.iterrows():
    print(f"Sender {row['sender']} communicated with Device {row['device_id']} during unusual hours ({row['unusual_hour_sms_count']} messages).")

# Optional - You can also add PCA and clustering, but I won't repeat that part since it's already covered in your code.
