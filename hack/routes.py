from flask import request, jsonify
from hack import app, db
from hack.tables import Case, Device, CallLog, SMS
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


@app.route('/upload_sms/<int:device_id>', methods=['POST'])
def store_sms(device_id):
    if request.is_json:
        data = request.get_json()
        for entry in data:
            sms = SMS(
                device_id=device_id,
                sender=entry.get("sender"),
                receiver=entry.get("receiver"),
                message_body=entry.get("message_body"),
                timestamp=datetime.fromisoformat(entry.get("timestamp")),
                message_type=entry.get("message_type")
            )
            db.session.add(sms)
            db.session.commit()

        return jsonify({"message": "SMS stored successfully"})

    else:
        return jsonify({"error": "Request must be JSON"})
