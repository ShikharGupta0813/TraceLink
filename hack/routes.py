from flask import request, jsonify
from hack import app, db
from hack.tables import Case, Device, CallLog, SMS, AppInstalled
from datetime import datetime
import subprocess
import pandas as pd
from hack.Models.model import (fetch_data_from_db, analyze_call_durations
        ,analyze_repeated_calls, analyze_unusual_timing, analyze_one_number_multiple_devices)
from hack.Models.modelsms import fetch_sms_logs ,find_frequent_communication ,detect_duplicate_messages,detect_excessive_activity,detect_unusual_timing,aggregate_sms_stats,preprocess_sms_data
def run_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

@app.route('/api/cases', methods=['POST'])
def create_case():
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        case = Case(name=name)
        with app.app_context():
            db.session.add(case)
            db.session.commit()
        return jsonify({"message": "Case created successfully"})

    else:
        return jsonify({"error" : "Request must be JSON"})


@app.route('/api/cases')
def show_cases():
    json_arr = []

    cases = Case.query.all()
    if not cases:
        return jsonify({"message": "Cases not created yet"})

    for log in cases:
        obj = {
            "id": log.id,
            "name": log.name,
            "created_at": log.created_at.strftime("%Y-%m-%d %H:%M:%S") if log.created_at else None,
        }
        json_arr.append(obj)

    return jsonify({'cases': json_arr})


@app.route('/api/devices', methods=['POST'])
def register_device():
    if request.is_json:
        data = request.get_json()

        case_id = data.get('caseId')
        device_type = data.get('deviceType')
        device_name = data.get('deviceName')
        device = Device(case_id=case_id, device_type=device_type,
                device_name=device_name)

        with app.app_context():
            db.session.add(device)
            db.session.commit()
        return jsonify({"message": "Device registered successfully"})

    else:
        return jsonify({"error" : "Request must be JSON"})


@app.route('/api/cases/<int:case_id>/devices')
def show_devices(case_id):
    json_arr = []

    devices = Device.query.filter_by(case_id=case_id)
    if not devices:
        return jsonify({"message": "Device not registered yet"})

    for log in devices:
        obj = {
            "id": log.id,
            "caseId": log.case_id,
            "type": log.device_type,
            "name": log.device_name
        }
        json_arr.append(obj)

    return jsonify({'devices': json_arr})


@app.route('/upload_call_logs/<int:device_id>', methods=['POST'])
def store_call_log(device_id):
    if request.is_json:
        json_data = request.get_json()
        data = json_data.get('logs')
        for entry in data:
            call_log = CallLog(
                device_id=device_id,
                phone_number=entry.get("number"),
                call_type=entry.get("type"),
                timestamp=datetime.fromisoformat(entry.get("date")),
                duration_seconds=entry.get("duration")
            )
            db.session.add(call_log)
            db.session.commit()

        return jsonify({"message": "CallLog stored successfully"})

    else:
        return jsonify({"error": "Request must be JSON"})


@app.route('/upload_sms_logs/<int:device_id>', methods=['POST'])
def store_sms(device_id):
    if request.is_json:
        json_data = request.get_json()
        data = json_data.get('logs')
        for entry in data:
            sms = SMS(
                device_id=device_id,
                sender=entry.get("address"),
                message_body=entry.get("body"),
                timestamp=datetime.fromisoformat(entry.get("date")),
                message_type=entry.get("type")
            )
            db.session.add(sms)
            db.session.commit()

        return jsonify({"message": "SMS stored successfully"})

    else:
        return jsonify({"error": "Request must be JSON"})

@app.route('/upload_installed_apps/<int:device_id>', methods=['POST'])
def store_installed_apps(device_id):
    if request.is_json:
        json_data = request.get_json()
        data = json_data.get('apps')
        for entry in data:
            installed = AppInstalled(
                device_id=device_id,
                app_name=entry.get("name"),
                app_package=entry.get("package")
            )
            db.session.add(installed)
            db.session.commit()

        return jsonify({"message": "App installed data stored successfully"})

    else:
        return jsonify({"error": "Request must be JSON"})


@app.route('/api/devices/<int:device_id>/call-logs')
def show_call_log(device_id):
    json_arr = []

    call_logs = CallLog.query.filter_by(device_id=device_id).order_by(CallLog.timestamp.desc())
    if not call_logs:
        return jsonify({"message": "Android app is not installed yet"})

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

    return jsonify({'call_log': json_arr})


@app.route('/api/devices/<int:device_id>/sms-logs')
def show_sms(device_id):
    json_arr = []

    sms_data = SMS.query.filter_by(device_id=device_id).order_by(SMS.timestamp.desc())
    if not sms_data:
        return jsonify({"message": "Android app is not installed yet"})

    for sms in sms_data:
        obj = {
            "id": sms.id,
            "device_id": sms.device_id,
            "sender": sms.sender,
            "message_body": sms.message_body,
            "timestamp": sms.timestamp.strftime("%Y-%m-%d %H:%M:%S") if sms.timestamp else None,
            "message_type": sms.message_type
        }
        json_arr.append(obj)

    return jsonify({'sms_data': json_arr})


@app.route('/api/devices/<int:device_id>/installed-apps')
def show_app_installed(device_id):
    json_arr = []

    app_data = AppInstalled.query.filter_by(device_id=device_id).order_by(AppInstalled.app_name.asc())
    if not app_data:
        return jsonify({"message": "Android app is not installed yet"})

    for a in app_data:
        obj = {
            "id": a.id,
            "device_id": a.device_id,
            "app_name": a.app_name,
            "app_package": a.app_package
        }
        json_arr.append(obj)

    return jsonify({'app_data': json_arr})


# Extracting Operating System Information
@app.route('/api/os-details')
def all_os_details():
    return jsonify({
        "os_version": run_command("uname -a"),
        "kernel_logs": run_command("dmesg"),
        "installed_apps": run_command("apt list --installed"),
        "last_logins": run_command("last"),
        "current_connections": run_command("netstat -tulnp"),
        "ip_config": run_command("ifconfig"),
        "routing_table": run_command("ip route"),
        "partition_info": run_command("lsblk")
    })


@app.route('/api/cases/<int:case_id>/evaluate/calllogs')
def call_log_insights(case_id):
    device_arr = Device.query.filter_by(case_id=case_id).all()

    if not device_arr:
        return jsonify({"message" : "No such device found"})

    arr = []
    for d in device_arr:
        arr.append(d.id)

    data = fetch_data_from_db(arr)
    print(data)
    call_df = pd.DataFrame([{
        'device_id': log['device_id'],
        'number': log['phone_number'],
        'duration': log['duration_seconds']
    } for log in data])

    df = analyze_repeated_calls(call_df,6)
    df1 = analyze_call_durations(call_df, 60)
    # df2 = analyze_unusual_timing(call_df)
    df3 = analyze_one_number_multiple_devices(call_df,2)

    result_json = df.to_dict(orient='records')
    result_json1 = df1.to_dict(orient='records')
    # result_json2 = df2.to_dict(orient='records')
    result_json3 = df3.to_dict(orient='records')

    return jsonify({"log": result_json, "log1": result_json1,
                     "log3" : result_json3})

@app.route('/api/cases/<int:case_id>/evaluate/sms')
def sms_log_insights(case_id):
    device_arr = Device.query.filter_by(case_id=case_id).all()

    if not device_arr:
        return jsonify({"message" : "No such device found"})

    arr = []
    for d in device_arr:
        arr.append(d.id)

    data = fetch_sms_logs(arr)
    print(data)
    call_df = pd.DataFrame([{
        'device_id': log['device_id'],
        'sender': log['sender'],
        'timestamp': log['timestamp'],
        'message_type':log['message_type'],
        'message_body':log['message_body']
    } for log in data])

    print(call_df)
    df=find_frequent_communication(call_df)
    df1 = detect_duplicate_messages(call_df)
    df9 = preprocess_sms_data(call_df)
    df0= aggregate_sms_stats(df9)
    df2 = detect_excessive_activity(df0)
    # df4 = detect_unusual_timing(call_df)

    result_json = df.to_dict(orient='records')
    result_json1 = df1.to_dict(orient='records')
    result_json3 = df2.to_dict(orient='records')
    # result_json4 = df4.to_dict(orient='records')

    return jsonify ({"log":result_json,"log2":result_json1,"log3":result_json3})