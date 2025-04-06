import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Connect to DB and fetch installed apps data
conn = sqlite3.connect("../instance/database.db")

# Query to fetch installed apps
query = """
SELECT ai.device_id, ai.app_name, ai.app_package 
FROM app_installed ai
"""
app_data = pd.read_sql_query(query, conn)
conn.close()

# Step 2: Feature Engineering

# Count the number of apps installed per device
device_app_count = app_data.groupby('device_id').size().reset_index(name='app_count')

# Extract app categories (you can expand this list or map manually)
app_categories = {
    'Communication': ['WhatsApp', 'Telegram', 'Messenger', 'Signal', 'Skype'],
    'Social Media': ['Facebook', 'Instagram', 'Twitter', 'Snapchat'],
    'Security': ['VPN', 'Tor', 'Signal'],
    'Finance': ['Paytm', 'Google Pay', 'Amazon Pay'],
    # Add other categories as needed
}

# Create a feature for each category (binary: 1 if app is in category, else 0)
for category, apps in app_categories.items():
    app_data[category] = app_data['app_name'].apply(lambda x: 1 if x in apps else 0)

# Aggregate the data by device to get counts for each category
device_features = app_data.groupby('device_id')[list(app_categories.keys())].sum().reset_index()

# Add app count (total number of apps installed per device)
device_features['app_count'] = device_app_count['app_count']

# Step 3: Anomaly Detection using Isolation Forest

# Prepare features for the model
X = device_features.drop(columns='device_id')

# Normalize or scale the features if needed
# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# Apply Isolation Forest
model = IsolationForest(contamination=0.1)  # 10% outliers (adjust as needed)
outliers = model.fit_predict(X)

# Add the outlier predictions to the dataset (1 means normal, -1 means anomaly)
device_features['outlier'] = outliers

# Step 4: Visualize and Analyze

# Plot the number of apps per device (normal vs anomalies)
plt.figure(figsize=(10, 6))
sns.countplot(x='app_count', hue='outlier', data=device_features)
plt.title("Normal vs Anomalous Devices Based on Number of Apps Installed")
plt.xlabel("Number of Apps Installed")
plt.ylabel("Device Count")
plt.show()

# Plot distribution of communication and security apps among devices
plt.figure(figsize=(12, 6))
sns.barplot(x='device_id', y='Communication', data=device_features, color='blue', label="Communication Apps")
sns.barplot(x='device_id', y='Security', data=device_features, color='red', label="Security Apps")
plt.title("Communication and Security Apps per Device")
plt.xticks(rotation=90)
plt.xlabel("Device ID")
plt.ylabel("Number of Apps")
plt.legend()
plt.show()

# Step 5: Identify Suspicious Devices
# These devices could be flagged as having unusual behavior (e.g., high number of security/privacy apps, unusual combinations)
suspicious_devices = device_features[device_features['outlier'] == -1]
print("Suspicious Devices Based on App Installations:")
print(suspicious_devices)

