from flask import Flask, request, jsonify
from flask_cors import CORS
import main

app = Flask(__name__)
CORS(app)

@app.route("/HUFS", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    bot_response = main.chatting(user_message)
    return jsonify({ "response": bot_response })

if __name__ == "__main__":
    app.run(port=1954)