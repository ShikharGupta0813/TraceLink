from hack import app, db

class CallLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50))
    number = db.Column(db.String(20))
    duration = db.Column(db.Integer)
    timestamp = db.Column(db.String(100))
    type =  db.Column(db.String(100))

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id= db.Column(db.String(50))
    device_type=db.Column(db.String(50))
    device_name=db.Column(db.String(50))

class SMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    sender = db.Column(db.String(100))
    message_body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    message_type = db.Column(db.String(10))

class AppInstalled(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    app_name = db.Column(db.String(25))
    app_package = db.Column(db.String(25))




with app.app_context():
    db.create_all()