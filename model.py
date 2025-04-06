import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Connect to DB
conn = sqlite3.connect("instance/database.db")

# Set your target case_id
target_case_id = 1  # 🔁 Change this as needed

# Step 2: Manually input device IDs linked to the case (for now)
device_ids = ['device_123', 'device_427', 'device_376']  # Replace with your actual device IDs

# Step 3: Fetch all call logs for those devices
query = f"""
SELECT * FROM call_log
WHERE device_id IN ({','.join(['?'] * len(device_ids))})
"""
call_logs = pd.read_sql_query(query, conn, params=device_ids)

conn.close()

# Step 4: Check for missing values in 'duration' and 'number' columns
if call_logs.empty:
    print("No call logs found for the specified devices.")
else:
    # Check for missing values in 'duration' and 'number' columns
    if call_logs['duration'].isnull().sum() > 0:
        print(f"Warning: There are {call_logs['duration'].isnull().sum()} missing values in the 'duration' column.")

    if call_logs['number'].isnull().sum() > 0:
        print(f"Warning: There are {call_logs['number'].isnull().sum()} missing values in the 'number' column.")

    # Step 5: Convert timestamp to datetime
    call_logs['timestamp'] = pd.to_datetime(call_logs['timestamp'])

    # --- Excessive Call Duration --- #

    # Step 6: Identify devices with excessive call duration (e.g., 60 minutes or more)
    threshold_duration = 60  # 60 minutes (1 hour) considered 'too long'
    excessive_calls = call_logs.groupby(['device_id', 'number']).agg(
        total_duration=('duration', 'sum')).reset_index()

    long_duration_calls = excessive_calls[excessive_calls['total_duration'] > threshold_duration]
    if not long_duration_calls.empty:
        print(f"\nDevices making excessive calls (over {threshold_duration} minutes):")
        print(long_duration_calls)

        # Written Insight for Excessive Call Duration
        print(f"\nInsight: The following devices have excessive call durations (over {threshold_duration} minutes):")
        print(long_duration_calls)

    # --- Repeated Calls to the Same Number --- #

    # Step 7: Identify devices calling the same number repeatedly
    call_counts = call_logs.groupby(['device_id', 'number']).size().reset_index(name='call_count')

    threshold_calls = 6  # Threshold for repeated calls (e.g., 6 times)
    repeated_calls = call_counts[call_counts['call_count'] >= threshold_calls]

    if not repeated_calls.empty:
        print(f"\nDevices calling the same number {threshold_calls} or more times:")
        print(repeated_calls)

        # Written Insight for Repeated Calls
        print(f"\nInsight: The following devices have made repeated calls to the same number {threshold_calls} or more times:")
        print(repeated_calls)

    # --- Frequent Communication --- #

    # Step 8: Identify devices with frequent communication patterns (many calls to various numbers)
    communication_threshold = 10  # Devices with more than 10 calls to different numbers
    frequent_communicators = call_logs.groupby('device_id')['number'].nunique().reset_index(name='unique_contacts')
    frequent_communicators = frequent_communicators[frequent_communicators['unique_contacts'] >= communication_threshold]

    if not frequent_communicators.empty:
        print(f"\nDevices with frequent communication (more than {communication_threshold} unique contacts):")
        print(frequent_communicators)

        # Written Insight for Frequent Communication
        print(f"\nInsight: The following devices are engaged in frequent communication (more than {communication_threshold} unique contacts):")
        print(frequent_communicators)

    # --- Unusual Call Timing --- #

    # Step 9: Identify calls made during unusual hours (e.g., late night or early morning)
    # Define 'unusual' as calls made between 10 PM and 6 AM
    call_logs['hour'] = call_logs['timestamp'].dt.hour
    unusual_timing = call_logs[(call_logs['hour'] >= 22) | (call_logs['hour'] < 6)]

    if not unusual_timing.empty:
        print(f"\nCalls made during unusual hours (10 PM - 6 AM):")
        print(unusual_timing)

        # Written Insight for Unusual Call Timing
        print(f"\nInsight: The following calls were made during unusual hours (10 PM - 6 AM), which could indicate suspicious activity:")
        print(unusual_timing)

    # --- High Frequency of Calls Between Two Numbers --- #

    # Step 10: Identify devices with high frequency of calls between two numbers
    high_frequency_calls = call_logs.groupby(['device_id', 'number']).size().reset_index(name='call_count')
    high_call_threshold = 10  # Threshold for high-frequency calls (e.g., 10 or more calls)
    high_frequency_calls = high_frequency_calls[high_frequency_calls['call_count'] >= high_call_threshold]

    if not high_frequency_calls.empty:
        print(f"\nHigh Frequency of Calls Between Two Numbers (10 or more calls):")
        print(high_frequency_calls)

        # Written Insight for High Frequency of Calls Between Two Numbers
        print(f"\nInsight: The following devices have made high-frequency calls (more than {high_call_threshold} calls) to the same number:")
        print(high_frequency_calls)

    # --- One Number Calling Different Devices --- #

    # Step 11: Identify if one number is calling multiple devices
    number_to_devices = call_logs.groupby(['number', 'device_id']).size().reset_index(name='call_count')
    threshold_devices = 3  # Threshold for a number calling multiple devices (e.g., 3 or more devices)
    number_to_devices = number_to_devices[number_to_devices['call_count'] >= threshold_devices]

    if not number_to_devices.empty:
        print(f"\nOne Number Calling Multiple Devices (3 or more devices):")
        print(number_to_devices)

        # Written Insight for One Number Calling Different Devices
        print(f"\nInsight: The following numbers have called multiple devices (more than {threshold_devices} devices):")
        print(number_to_devices)

    # --- Visualization --- #

    # Plot excessive call duration (for devices with long calls)
    if not long_duration_calls.empty:
        plt.figure(figsize=(12, 6))
        sns.barplot(x='device_id', y='total_duration', hue='number', data=long_duration_calls, palette='viridis')
        plt.title(f"Devices with Excessive Call Durations (Case ID: {target_case_id})")
        plt.xlabel('Device ID')
        plt.ylabel('Total Duration (Minutes)')
        plt.xticks(rotation=45)
        plt.show()

        # Written Insight for Graph
        print(f"\nInsight (Graph): The bar chart displays devices with excessive call durations (over {threshold_duration} minutes). Look for any unusual spikes in the graph.")

    # Plot repeated calls (for devices calling the same number many times)
    if not repeated_calls.empty:
        plt.figure(figsize=(12, 6))
        sns.barplot(x='device_id', y='call_count', hue='number', data=repeated_calls, palette='viridis')
        plt.title(f"Devices Repeatedly Calling the Same Number (Case ID: {target_case_id})")
        plt.xlabel('Device ID')
        plt.ylabel('Number of Calls')
        plt.xticks(rotation=45)
        plt.show()

        # Written Insight for Graph
        print(f"\nInsight (Graph): The bar chart shows devices making repeated calls to the same number. Devices with higher call counts could indicate suspicious activity.")

    # Plot frequent communication (for devices with many unique contacts)
    if not frequent_communicators.empty:
        plt.figure(figsize=(12, 6))
        sns.barplot(x='device_id', y='unique_contacts', data=frequent_communicators, palette='viridis')
        plt.title(f"Devices with Frequent Communication (Case ID: {target_case_id})")
        plt.xlabel('Device ID')
        plt.ylabel('Unique Contacts')
        plt.xticks(rotation=45)
        plt.show()

        # Written Insight for Graph
        print(f"\nInsight (Graph): The bar chart illustrates devices that communicated with many unique contacts. High values could indicate mass communication activities, requiring further investigation.")

    # Plot calls during unusual hours
    if not unusual_timing.empty:
        plt.figure(figsize=(12, 6))
        sns.countplot(x='device_id', data=unusual_timing, palette='viridis')
        plt.title(f"Calls Made During Unusual Hours (10 PM - 6 AM) (Case ID: {target_case_id})")
        plt.xlabel('Device ID')
        plt.ylabel('Number of Calls')
        plt.xticks(rotation=45)
        plt.show()

        # Written Insight for Graph
        print(f"\nInsight (Graph): The count plot displays devices making calls during unusual hours (10 PM - 6 AM). A high number of calls during this time could indicate irregular activity.")

    # Plot high-frequency calls (for devices making high-frequency calls between two numbers)
    if not high_frequency_calls.empty:
        plt.figure(figsize=(12, 6))
        sns.barplot(x='device_id', y='call_count', hue='number', data=high_frequency_calls, palette='viridis')
        plt.title(f"High Frequency of Calls Between Two Numbers (Case ID: {target_case_id})")
        plt.xlabel('Device ID')
        plt.ylabel('Call Count')
        plt.xticks(rotation=45)
        plt.show()

        # Written Insight for Graph
        print(f"\nInsight (Graph): The bar chart visualizes high-frequency calls between two numbers. This may help identify frequent communication between particular devices.")
