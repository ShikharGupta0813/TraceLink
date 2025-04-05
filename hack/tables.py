from datetime import datetime
from hack import db, app

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    device_type = db.Column(db.String(50))
    device_name = db.Column(db.String(100))


class CallLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    phone_number = db.Column(db.String(20))
    call_type = db.Column(db.String(10))  # Incoming, Outgoing, Missed
    timestamp = db.Column(db.DateTime)
    duration_seconds = db.Column(db.Integer)

class SMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    sender = db.Column(db.String(100))
    message_body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    message_type = db.Column(db.String(10))


with app.app_context():
    db.create_all()