import os
import razorpay
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret-key-prod")

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
PAID_DRIVE_LINK = os.getenv("DRIVE_LINK", "https://drive.google.com")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@app.route("/")
def home():
    return render_template("index.html", rzp_key=RAZORPAY_KEY_ID)

@app.route("/create-order", methods=["POST"])
def create_order():
    try:
        # ₹49 = 4900 paise
        order_data = {
            "amount": 4900,
            "currency": "INR",
            "receipt": "rcpt_masterfx_drive",
            "payment_capture": 1
        }
        order = client.order.create(data=order_data)
        return jsonify({"status": "success", "order": order})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/verify-payment", methods=["POST"])
def verify_payment():
    data = request.get_json()
    params_dict = {
        'razorpay_order_id': data.get('razorpay_order_id'),
        'razorpay_payment_id': data.get('razorpay_payment_id'),
        'razorpay_signature': data.get('razorpay_signature')
    }

    try:
        client.utility.verify_payment_signature(params_dict)
        session['is_paid'] = True
        session['payment_id'] = data.get('razorpay_payment_id')
        return jsonify({"status": "success"})
    except razorpay.errors.SignatureVerificationError:
        return jsonify({"status": "failed", "message": "Signature verification failed"}), 400

@app.route("/success")
def success():
    if not session.get('is_paid'):
        return redirect(url_for('home'))
    return render_template("success.html", download_url=PAID_DRIVE_LINK, payment_id=session.get('payment_id'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)