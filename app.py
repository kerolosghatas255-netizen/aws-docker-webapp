from flask import Flask, jsonify
import os
import socket
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

@app.route("/")
def home():
    return f"""
    <h1>DevOps Portfolio Project</h1>
    <p>Application successfully deployed with Docker.</p>
    <p>Hostname: {socket.gethostname()}</p>
    <p>Try <a href="/health">/health</a> or <a href="/visits">/visits</a></p>
    """

@app.route("/health")
def health():
    return jsonify(status="healthy"), 200

@app.route("/db-health")
def db_health():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        return jsonify(database="healthy"), 200
    except Exception as exc:
        return jsonify(database="unhealthy", error=str(exc)), 500

@app.route("/visits")
def visits():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)

    cur.execute("INSERT INTO visits DEFAULT VALUES;")
    cur.execute("SELECT COUNT(*) FROM visits;")
    count = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify(
        message="Visit stored successfully",
        total_visits=count
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
