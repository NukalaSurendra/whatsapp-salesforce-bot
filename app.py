# app.py
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Twilio WhatsApp Bot is Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')

    print(f"Received message from {from_number}: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    # Simple logic
    if 'hello' in incoming_msg:
        msg.body("Hi! How can I help you today?")
    elif 'help' in incoming_msg:
        msg.body("This is a test bot connected to Twilio and Salesforce.")
    else:
        msg.body(f"You said: {incoming_msg}")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Important for Render
    app.run(debug=True, host='0.0.0.0', port=port)



















