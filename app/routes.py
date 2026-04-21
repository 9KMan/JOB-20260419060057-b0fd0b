from flask import Blueprint, request, jsonify
from app import Session
from app.models import Customer, Visit, Reward
from app.services.loyalty_service import LoyaltyService
from app.services.whatsapp_service import WhatsAppService

api_bp = Blueprint("api", __name__)
loyalty_service = LoyaltyService()
whatsapp_service = WhatsAppService()

@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@api_bp.route("/customers", methods=["POST"])
def create_customer():
    data = request.get_json()
    phone = data.get("phone")
    name = data.get("name", "")

    if not phone:
        return jsonify({"error": "phone is required"}), 400

    db = Session()
    try:
        customer = db.query(Customer).filter_by(phone=phone).first()
        if customer:
            return jsonify(customer.to_dict()), 200

        customer = Customer(phone=phone, name=name)
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return jsonify(customer.to_dict()), 201
    finally:
        db.close()

@api_bp.route("/customers/<phone>", methods=["GET"])
def get_customer(phone):
    db = Session()
    try:
        customer = db.query(Customer).filter_by(phone=phone).first()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify(customer.to_dict())
    finally:
        db.close()

@api_bp.route("/customers/<phone>/visits", methods=["GET"])
def get_customer_visits(phone):
    db = Session()
    try:
        customer = db.query(Customer).filter_by(phone=phone).first()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        visits = [v.to_dict() for v in customer.visits]
        return jsonify({"customer": customer.to_dict(), "visits": visits})
    finally:
        db.close()

@api_bp.route("/visits", methods=["POST"])
def record_visit():
    data = request.get_json()
    phone = data.get("phone")
    notes = data.get("notes", "")

    if not phone:
        return jsonify({"error": "phone is required"}), 400

    db = Session()
    try:
        customer = db.query(Customer).filter_by(phone=phone).first()
        if not customer:
            customer = Customer(phone=phone)
            db.add(customer)
            db.commit()
            db.refresh(customer)

        visit, reward_granted = loyalty_service.record_visit(db, customer)

        if reward_granted:
            whatsapp_service.send_reward_message(phone, customer.name)

        return jsonify({
            "visit": visit.to_dict(),
            "reward_granted": reward_granted,
            "customer": customer.to_dict()
        }), 201
    finally:
        db.close()

@api_bp.route("/rewards/<phone>", methods=["GET"])
def get_rewards(phone):
    db = Session()
    try:
        customer = db.query(Customer).filter_by(phone=phone).first()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        rewards = db.query(Reward).filter_by(customer_id=customer.id, redeemed=False).all()
        return jsonify({
            "customer": customer.to_dict(),
            "available_rewards": [r.to_dict() for r in rewards]
        })
    finally:
        db.close()

@api_bp.route("/rewards/<int:reward_id>/redeem", methods=["POST"])
def redeem_reward(reward_id):
    db = Session()
    try:
        reward = db.query(Reward).filter_by(id=reward_id).first()
        if not reward:
            return jsonify({"error": "Reward not found"}), 404
        if reward.redeemed:
            return jsonify({"error": "Reward already redeemed"}), 400

        reward.redeemed = True
        reward.redeemed_at = datetime.utcnow()
        customer = db.query(Customer).filter_by(id=reward.customer_id).first()
        if customer:
            customer.total_rewards += 1
        db.commit()

        if customer:
            whatsapp_service.send_redeem_confirmation(customer.phone, customer.name)

        return jsonify(reward.to_dict())
    finally:
        db.close()

from datetime import datetime