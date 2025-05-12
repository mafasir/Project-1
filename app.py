from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wallet.db"
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    balance = db.Column(db.Float, default=0.0)
    
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
    
with app.app_context():
    db.create_all()
    
@app.route("/create-users")
def create_users():
    user1 = user(name="Sachindra", email="sachindra@example.com", balance=1000.0)
    user2 = user(name="Rabin", email="Rabin@example.com", balance=2000.0)
    db.session.add_all([user1, user2])
    db.session.commit()
    return "Users created successfully."

@app.route("/send", methods=["POST"])
def send_money():
    data = request.get_json()
    sender = user.query.filter_by(email=data["sender"]).first()
    receiver = user.query.filter_by(email=data["receiver"]).first()
    amount = float(data["amount"])
    
    if not sender or not receiver:
        return jsonify({"message": "User not found"}), 404
    
    if sender.balance < amount:
        return jsonify({"message": "Not enough balance"}), 400
    
    sender.balance -= amount
    receiver.balance += amount
    transaction = Transaction(sender_id=sender.id, receiver_id=receiver.id, amount=amount)
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({"message": "Money sent!"})

@app.route("/users")
def get_users():
    txns = Transaction.query.all()
    return jsonify([{ "sender_id": t.sender_id, "receiver_id": t.receiver_id, "amount": t.amount } for t in txns])

if __name__ == "__main__":
    app.run(debug=True)
    