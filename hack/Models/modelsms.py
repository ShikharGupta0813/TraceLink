import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from hack.tables import SMS
import io
import base64

# Function to fetch SMS logs from DB
def fetch_sms_logs(device_ids):
    call_logs = SMS.query.filter(SMS.device_id.in_(device_ids)).all()

    json_arr = []
    for log in call_logs:
        obj = {
            "id": log.id,
            "device_id": log.device_id,
            "sender": log.sender,
            "message_type": log.message_type,
            "message_body":log.message_body,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S") if log.timestamp else None
        }
        json_arr.append(obj)

    return json_arr


# Function to preprocess SMS data
def preprocess_sms_data(sms_logs):
    sms_logs['timestamp'] = pd.to_datetime(sms_logs['timestamp'])
    sms_logs['hour'] = sms_logs['timestamp'].dt.hour
    sms_logs['day'] = sms_logs['timestamp'].dt.dayofweek
    sms_logs['month'] = sms_logs['timestamp'].dt.month
    sms_logs['message_length'] = sms_logs['message_body'].apply(lambda x: len(str(x)))
    sms_logs['message_type'] = sms_logs['message_type'].astype('category')
    return sms_logs


# Function to aggregate SMS statistics per device
def aggregate_sms_stats(sms_logs):
    device_sms_summary = sms_logs.groupby(['device_id', 'sender']).agg(
        total_sms=('message_body', 'count'),
        avg_message_length=('message_length', 'mean'),
        sms_per_hour=('hour', 'count'),
        sms_per_day=('day', 'count'),
        sms_per_month=('month', 'count')
    ).reset_index()
    return device_sms_summary


# Function to detect excessive messaging activity
def detect_excessive_activity(device_sms_summary):
    threshold = device_sms_summary['total_sms'].mean() + 3 * device_sms_summary['total_sms'].std()
    suspicious_activity = device_sms_summary[device_sms_summary['total_sms'] > threshold]
    return suspicious_activity


# Function to detect message pattern similarities
def detect_duplicate_messages(sms_logs):
    message_pairs = sms_logs.groupby(['sender', 'device_id'])['message_body'].apply(lambda x: ' '.join(x)).reset_index()
    duplicate_messages = message_pairs[message_pairs.duplicated(subset=['message_body'], keep=False)]
    return duplicate_messages


# Function to find frequent communication between senders
def find_frequent_communication(sms_logs):
    communication_count = sms_logs.groupby(['sender', 'device_id']).size().reset_index(name='communication_count')
    top_communication_pairs = communication_count.nlargest(10, 'communication_count')
    return top_communication_pairs


# Function to detect unusual timing patterns
def detect_unusual_timing(sms_logs):
    unusual_hours = sms_logs[sms_logs['hour'] < 6]
    unusual_activity = unusual_hours.groupby(['sender', 'device_id']).size().reset_index(name='unusual_hour_sms_count')
    return unusual_activity




def generate_sms_plot(df, feature, threshold=None):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='device_id', y=feature, data=df)
    if threshold:
        plt.axhline(y=threshold, color='red', linestyle='--', label='Threshold')
    plt.title(f'{feature} per Device')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return image_base64


# Function to print insights and results for each analysis
def print_insights_and_plots(data, analysis_type, threshold=None):
    if not data.empty:
        print(f"\n{analysis_type} (Threshold: {threshold if threshold else 'N/A'}):")
        print(data[['sender', 'device_id', analysis_type]])

        # Plotting the data
        plt.figure(figsize=(12, 6))
        sns.barplot(x='device_id', y=analysis_type, hue='sender', data=data, palette='viridis')
        plt.title(f"{analysis_type} Analysis")
        plt.xlabel('Device ID')
        plt.ylabel('Value')
        plt.xticks(rotation=45)
        plt.show()


# Main function to run the analysis
def main():
    # Fetch and preprocess data
    sms_logs = fetch_sms_logs()
    sms_logs = preprocess_sms_data(sms_logs)

    # Aggregate SMS statistics per device
    device_sms_summary = aggregate_sms_stats(sms_logs)

    # 1. Detect excessive messaging activity
    suspicious_activity = detect_excessive_activity(device_sms_summary)
    print_insights_and_plots(suspicious_activity, 'total_sms', threshold=suspicious_activity['total_sms'].mean())

    # 2. Detect message pattern similarities
    duplicate_messages = detect_duplicate_messages(sms_logs)
    print_insights_and_plots(duplicate_messages, 'message_body')

    # 3. Find frequent communication between senders
    top_communication_pairs = find_frequent_communication(sms_logs)
    print_insights_and_plots(top_communication_pairs, 'communication_count')

    # 4. Detect unusual timing patterns
    unusual_activity = detect_unusual_timing(sms_logs)
    print_insights_and_plots(unusual_activity, 'unusual_hour_sms_count')


if __name__ == "__main__":
    main()
