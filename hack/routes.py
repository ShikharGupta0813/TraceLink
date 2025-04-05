from flask import request, jsonify
from hack import app, db
from hack.tables import Case, Device, CallLog, SMS, AppInstalled
from datetime import datetime

@app.route('/case', methods=['POST'])
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

@app.route('/device/<int:case_id>', methods=['POST'])
def register_device(case_id):
    if request.is_json:
        data = request.get_json()

        device_type = data.get('device_type')
        device_name = data.get('device_name')
        device = Device(case_id=case_id, device_type=device_type,
                device_name=device_name)

        with app.app_context():
            db.session.add(device)
            db.session.commit()
        return jsonify({"message": "Device registered successfully"})

    else:
        return jsonify({"error" : "Request must be JSON"})


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


@app.route('/show_call_log/<int:device_id>')
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


@app.route('/show_sms/<int:device_id>')
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


@app.route('/show_app_installed/<int:device_id>')
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