from flask import Flask, jsonify, session, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)



class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    # timestamp = db.Column(db.DateTime, server_default=datetime.now)

    def __init__(self, username, message):
        self.username = username
        self.message = message

    def getLine(self):
        return f"[+] {self.username}: {self.message}"
    
    def getJson(self):
        return { "username": self.username, "message": self.message}


@app.route("/")
def hello_world():
    return jsonify(
            message="Bad request.",
            category="error",
            status=404
            )

@app.route("/getChat")
def getChat():
    messages = db.session.query(Message).all()
    JsonArray = []
    
    for message in messages:
        JsonArray.append(message.getJson())
        print(message.getJson())

    return jsonify(JsonArray)

@app.route("/sendMessage", methods=["POST"])
def sendMessage():
    username = request.args.get("username")
    message = request.args.get("message")
    message = Message(username, message)
    db.session.add(message)
    db.session.commit()
    return jsonify(success=True)