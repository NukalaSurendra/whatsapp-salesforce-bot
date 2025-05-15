import sys
sys.stdout.reconfigure(line_buffering=True)

import os
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import requests
from dotenv import load_dotenv

load_dotenv()  # Load values from .env if running locally

app = Flask(__name__)

# Load environment variables for secure use
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

SF_INSTANCE = os.getenv("SF_INSTANCE")  # e.g., https://yourdomain.my.salesforce.com
SF_ACCESS_TOKEN = os.getenv("SF_ACCESS_TOKEN")  # Bearer token

print("webhook triggerd")
@app.route("/", methods=["GET"])
def home():
    return "Twilio WhatsApp Bot with Salesforce is Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '').replace('whatsapp:', '')

    print(f"Received message from {from_number}: {incoming_msg}")

    # Send message to Salesforce as a Case
    headers = {
        "Authorization": f"Bearer {SF_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    whatsapp_transaction = {
        "Message__c": incoming_msg,
        "Phone_No__c": from_number
    }
    r = requests.post(f"{SF_INSTANCE}/services/data/v60.0/sobjects/Whatsapp_Transaction__c/", headers=headers, json=whatsapp_transaction)
    print(f"Salesforce Case creation response: {r.status_code} - {r.text}")
    
    #case_data = {
    #    "Subject": f"WhatsApp from {from_number}",
    #    "Description": incoming_msg,
    #    "Origin": "WhatsApp",
    #    "Status": "New",
    #    "WhatsAppNumber__c": from_number
    #}

    #r = requests.post(f"{SF_INSTANCE}/services/data/v60.0/sobjects/Case/", headers=headers, json=case_data)
    #print(f"Salesforce Case creation response: {r.status_code} - {r.text}")

    # Respond to user immediately
    resp = MessagingResponse()
    msg = resp.message("Thanks for your message! We'll be in touch soon.")
    return str(resp)

@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()
    to = data.get('to')
    message = data.get('message')

    if not to or not message:
    	print("Missing 'to' or 'message'")
    	return jsonify({"error": "Missing 'to' or 'message'"}), 400

    if not to.startswith('+'):
        to = f'+{to}'

    print(f"[DEBUG] Sending message to whatsapp:{to}: {message}")
    print(f"Sending message to {to}: {message}")
    
    twilio_url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    payload = {
        "From": f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
        "To": f"whatsapp:{to}",
        "ContentSid" : "HX2fdd86cbee81cffcc28b70ff20e8cda5"
        #"ContentVariables": message
        #"Body": message
    }

    res = requests.post(twilio_url, data=payload, auth=(TWILIO_SID, TWILIO_AUTH_TOKEN))
    return jsonify({"status": "sent", "twilio_response": res.text}), res.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # For Render
    app.run(debug=True, host="0.0.0.0", port=port)


















