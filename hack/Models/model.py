from hack.tables import CallLog
import seaborn as sns
import matplotlib.pyplot as plt


def fetch_data_from_db(device_ids):
    call_logs = CallLog.query.filter(CallLog.device_id.in_(device_ids)).all()

    json_arr = []
    for log in call_logs:
        obj = {
            "id": log.id,
            "device_id": log.device_id,
            "phone_number": log.phone_number,
            "call_type": log.call_type,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S") if log.timestamp else None,
            "duration_seconds": log.duration_seconds
        }
        json_arr.append(obj)

    return json_arr


def check_missing_values(call_logs):
    """Check for missing values in the call logs."""
    missing_values = {
        "duration": call_logs['duration'].isnull().sum(),
        "number": call_logs['number'].isnull().sum()
    }
    return missing_values


def analyze_call_durations(call_logs, threshold=60):
    """Analyze call durations and identify excessive calls."""
    excessive_calls = call_logs.groupby(['device_id', 'number']).agg(
        total_duration=('duration', 'sum')).reset_index()
    long_duration_calls = excessive_calls[excessive_calls['total_duration'] > threshold]
    return long_duration_calls


def analyze_repeated_calls(call_logs, threshold=6):
    """Identify repeated calls to the same number."""
    call_counts = call_logs.groupby(['device_id', 'number']).size().reset_index(name='call_count')
    repeated_calls = call_counts[call_counts['call_count'] >= threshold]
    return repeated_calls


def analyze_frequent_communication(call_logs, threshold=10):
    """Identify devices with frequent communication."""
    frequent_communicators = call_logs.groupby('device_id')['number'].nunique().reset_index(name='unique_contacts')
    frequent_communicators = frequent_communicators[frequent_communicators['unique_contacts'] >= threshold]
    return frequent_communicators


def analyze_unusual_timing(call_logs):
    """Identify calls made during unusual hours."""
    call_logs['hour'] = call_logs['timestamp'].dt.DateTime
    unusual_timing = call_logs[(call_logs['hour'] >= 22) | (call_logs['hour'] < 6)]
    return unusual_timing


def analyze_one_number_multiple_devices(call_logs, threshold=3):
    """Identify if one number is calling multiple devices."""
    number_to_devices = call_logs.groupby(['number', 'device_id']).size().reset_index(name='call_count')
    number_to_devices = number_to_devices[number_to_devices['call_count'] >= threshold]
    return number_to_devices


def generate_insight_and_plot(data, title, insight_type, threshold):
    """Generate insights and plot for analysis."""
    if not data.empty:
        print(f"\nDevices with {insight_type} (Threshold: {threshold}):")
        print(data)

        # Plotting the data
        plt.figure(figsize=(12, 6))
        sns.barplot(x='device_id', y='total_duration', hue='number', data=data, palette='viridis')
        plt.title(f"{title}")
        plt.xlabel('Device ID')
        plt.ylabel('Value')
        plt.xticks(rotation=45)
        plt.show()

        print(f"\nInsight (Graph): {insight_type} analysis. Devices with higher values could indicate suspicious activity.")


def main(device_ids):
    """Main function to run all analyses and print insights."""
    call_logs = fetch_data_from_db(device_ids)

    if call_logs.empty:
        print("No call logs found for the specified devices.")
        return

    # Step 1: Check for missing values
    missing_values = check_missing_values(call_logs)
    for column, count in missing_values.items():
        if count > 0:
            print(f"Warning: There are {count} missing values in the '{column}' column.")

    # Step 2: Perform analysis and generate insights
    long_duration_calls = analyze_call_durations(call_logs)
    repeated_calls = analyze_repeated_calls(call_logs)
    frequent_communicators = analyze_frequent_communication(call_logs)
    unusual_timing = analyze_unusual_timing(call_logs)
    number_to_devices = analyze_one_number_multiple_devices(call_logs)

    # Generate insights and plots for each analysis
    generate_insight_and_plot(long_duration_calls, "Devices with Excessive Call Durations", "Excessive Call Duration", 60)
    generate_insight_and_plot(repeated_calls, "Devices Repeatedly Calling the Same Number", "Repeated Calls", 6)
    generate_insight_and_plot(frequent_communicators, "Devices with Frequent Communication", "Frequent Communication", 10)
    generate_insight_and_plot(unusual_timing, "Calls Made During Unusual Hours", "Unusual Call Timing", 0)
    generate_insight_and_plot(number_to_devices, "One Number Calling Multiple Devices", "Multiple Devices Called", 3)


if __name__ == "__main__":
    # Example device IDs (Replace with actual IDs)
    device_ids = ['device_123', 'device_427', 'device_376']
    main(device_ids)
