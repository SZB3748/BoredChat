from . import messaging
from .messaging import Connection, Message
from flask import abort, Flask, redirect, render_template, request, session, url_for
from flask_sock import Sock, Server
import json
import os
import traceback
from uuid import uuid4

DIR = os.getcwd()

sock = Sock()
app = Flask(__name__)
app.url_map.strict_slashes = False

connections:dict[int, Connection] = {}

def enqueue_msg(message:Message):
    for conn in connections.values():
        conn.enqueue_msg(message)

def create():
    "Create flask app."
    TEMPLATES = os.path.join(DIR, "templates")
    STATIC = os.path.join(DIR, "static")

    app.template_folder = TEMPLATES
    app.static_folder = STATIC


    sock.init_app(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "name" not in request.form:
            abort(400, "Missing name.")
        if "id" not in session:
            session["id"] = uuid4().int
        session["name"] = request.form["name"]
        return redirect(url_for("chat"))
    else:
        return render_template("index.html")
    

@app.route("/chat")
def chat():
    if "id" not in session:
        return redirect(url_for("index"))
    return render_template("chat.html", name=session["name"])

@app.route("/tips")
def tips():
    return render_template("tips.html")

@sock.route("/ws")
def web_socket(ws:Server):
    conn = Connection(session["id"])
    connections[conn.id] = conn
    enqueue_msg(Message(0, "<span style=\"color: #820a0a;\">[SERVER]</span>", f"{session['name']} has joined."))
    try:
        while ws.connected:
            try:
                msg = ws.receive(0)
                if msg:
                    enqueue_msg(Message(session["id"], session["name"], msg))
                m = conn.dequeue_msg()
                while m:    
                    ws.send(json.dumps({"name":m.sender_name, "content":m.content})+"\n")
                    m = conn.dequeue_msg()
            except Exception as e:
                traceback.print_exception(e)
    finally:
        connections.pop(conn.id, None)
        enqueue_msg(Message(0, "<span style=\"color: #820a0a;\">[SERVER]</span>", f"{session['name']} has left."))
