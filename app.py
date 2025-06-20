from flask import Flask, render_template, request, redirect
import uuid
import time
import threading

app = Flask(__name__)
sessions = {}
messages_to_send = []

def auto_sender():
    while True:
        if messages_to_send:
            print(f"[Auto Send] Decrypted Message Sent: {messages_to_send.pop(0)}")
        time.sleep(60)  # Sends every 1 minute

# Start background sender
threading.Thread(target=auto_sender, daemon=True).start()

@app.route("/")
def index():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"status": "IDLE", "last": time.ctime()}
    return render_template("index.html", session_id=session_id)

@app.route("/send", methods=["POST"])
def send():
    recipient_id = request.form["recipient_id"]
    messages = request.form["messages"].splitlines()
    for msg in messages:
        decrypted = f"[Decrypted for {recipient_id}]: {msg}"  # Simulate decryption
        messages_to_send.append(decrypted)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
