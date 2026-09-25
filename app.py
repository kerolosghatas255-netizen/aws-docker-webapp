from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return f"""
    <h1>DevOps Portfolio Project</h1>
    <p>Application successfully deployed with Docker.</p>
    <p>Hostname: {socket.gethostname()}</p>
    """

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)