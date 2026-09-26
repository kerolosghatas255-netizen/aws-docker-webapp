from flask import Flask, jsonify, render_template_string
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


HOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS DevOps Deployment</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background:
                radial-gradient(circle at top left, #172554 0, transparent 35%),
                radial-gradient(circle at bottom right, #064e3b 0, transparent 30%),
                #090d16;
            color: #f8fafc;
            min-height: 100vh;
        }

        .container {
            width: min(1180px, 92%);
            margin: auto;
            padding: 64px 0;
        }

        .eyebrow {
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            color: #93c5fd;
            margin-bottom: 14px;
            font-weight: 700;
        }

        h1 {
            font-size: clamp(38px, 6vw, 68px);
            line-height: 1;
            margin: 0 0 20px;
            letter-spacing: -0.04em;
        }

        .lead {
            color: #b8c2d6;
            max-width: 780px;
            font-size: 18px;
            line-height: 1.7;
            margin-bottom: 42px;
        }

        .status-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 34px;
        }

        .card {
            background: rgba(15, 23, 42, 0.76);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 18px;
            padding: 22px;
            backdrop-filter: blur(10px);
        }

        .card-label {
            color: #94a3b8;
            font-size: 13px;
            margin-bottom: 10px;
        }

        .card-value {
            font-size: 21px;
            font-weight: 700;
        }

        .healthy {
            color: #4ade80;
        }

        .checking {
            color: #facc15;
        }

        .error {
            color: #fb7185;
        }

        .section {
            background: rgba(15, 23, 42, 0.62);
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 22px;
            padding: 28px;
            margin-top: 18px;
        }

        h2 {
            margin: 0 0 22px;
            font-size: 22px;
        }

        .flow {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }

        .flow-item {
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 12px;
            padding: 11px 15px;
            background: rgba(2, 6, 23, 0.55);
            font-weight: 600;
        }

        .arrow {
            color: #64748b;
            font-size: 20px;
        }

        .stack {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .tag {
            padding: 9px 13px;
            border-radius: 999px;
            background: rgba(59, 130, 246, 0.11);
            border: 1px solid rgba(96, 165, 250, 0.22);
            color: #bfdbfe;
            font-size: 14px;
        }

        .links {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 28px;
        }

        .button {
            text-decoration: none;
            color: #e2e8f0;
            border: 1px solid rgba(148, 163, 184, 0.22);
            background: rgba(15, 23, 42, 0.9);
            border-radius: 12px;
            padding: 11px 16px;
            font-size: 14px;
            transition: 0.2s ease;
        }

        .button:hover {
            border-color: #60a5fa;
            transform: translateY(-1px);
        }

        .footer {
            color: #64748b;
            margin-top: 30px;
            font-size: 13px;
        }

        code {
            color: #cbd5e1;
        }

        @media (max-width: 850px) {
            .status-row {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 520px) {
            .status-row {
                grid-template-columns: 1fr;
            }

            .container {
                padding: 38px 0;
            }
        }
    </style>
</head>

<body>
    <main class="container">
        <div class="eyebrow">DevOps Portfolio Project</div>

        <h1>AWS DevOps<br>Deployment</h1>

        <p class="lead">
            Containerized application running on AWS EC2 with Nginx,
            Flask/Gunicorn, PostgreSQL persistent storage, automated CI/CD,
            GitHub OIDC, AWS Systems Manager, and Terraform-managed infrastructure.
        </p>

        <div class="status-row">
            <div class="card">
                <div class="card-label">Application</div>
                <div id="app-status" class="card-value checking">Checking...</div>
            </div>

            <div class="card">
                <div class="card-label">Database</div>
                <div id="db-status" class="card-value checking">Checking...</div>
            </div>

            <div class="card">
                <div class="card-label">Reverse Proxy</div>
                <div class="card-value">Nginx</div>
            </div>

            <div class="card">
                <div class="card-label">Cloud Platform</div>
                <div class="card-value">AWS EC2</div>
            </div>
        </div>

        <section class="section">
            <h2>Application Flow</h2>

            <div class="flow">
                <div class="flow-item">Internet</div>
                <div class="arrow">?</div>
                <div class="flow-item">Nginx</div>
                <div class="arrow">?</div>
                <div class="flow-item">Gunicorn</div>
                <div class="arrow">?</div>
                <div class="flow-item">Flask</div>
                <div class="arrow">?</div>
                <div class="flow-item">PostgreSQL</div>
            </div>
        </section>

        <section class="section">
            <h2>Infrastructure & Delivery</h2>

            <div class="stack">
                <span class="tag">Docker</span>
                <span class="tag">Docker Compose</span>
                <span class="tag">Nginx</span>
                <span class="tag">Gunicorn</span>
                <span class="tag">PostgreSQL</span>
                <span class="tag">GitHub Actions</span>
                <span class="tag">GitHub OIDC</span>
                <span class="tag">AWS Systems Manager</span>
                <span class="tag">Terraform</span>
                <span class="tag">Ubuntu Linux</span>
            </div>

            <div class="links">
                <a class="button" href="/health">Application Health</a>
                <a class="button" href="/db-health">Database Health</a>
                <a class="button" href="/visits">Persistence Test</a>
            </div>
        </section>

        <div class="footer">
            Container hostname: <code>{{ hostname }}</code>
        </div>
    </main>

    <script>
        async function checkStatus(url, elementId, key) {
            const element = document.getElementById(elementId);

            try {
                const response = await fetch(url);
                const data = await response.json();

                if (response.ok) {
                    element.textContent = "Healthy";
                    element.className = "card-value healthy";
                } else {
                    element.textContent = "Unhealthy";
                    element.className = "card-value error";
                }
            } catch (error) {
                element.textContent = "Unavailable";
                element.className = "card-value error";
            }
        }

        checkStatus("/health", "app-status", "status");
        checkStatus("/db-health", "db-status", "database");
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HOME_PAGE,
        hostname=socket.gethostname()
    )


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
        return jsonify(
            database="unhealthy",
            error=str(exc)
        ), 500


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
