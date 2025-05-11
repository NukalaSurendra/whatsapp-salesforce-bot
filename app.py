# app.py

from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "WhatsApp-Salesforce Bot is Running!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return request.args.get("hub.challenge")
    if request.method == 'POST':
        print(request.json)  # this is where you process incoming WhatsApp messages
        return "OK", 200

PORT = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=PORT)
