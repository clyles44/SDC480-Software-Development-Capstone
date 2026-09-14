from flask import Flask, request, redirect, url_for, session, render_template_string
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "SDC480-Phase1-Fraud-Review-System"
DATABASE = "fraud_review.db"


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT NOT NULL,
            transaction_date TEXT NOT NULL,
            merchant TEXT NOT NULL,
            amount REAL NOT NULL,
            location TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            fraud_score INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER NOT NULL,
            reviewer_id INTEGER NOT NULL,
            decision TEXT NOT NULL,
            review_notes TEXT,
            reviewed_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
            FOREIGN KEY (reviewer_id) REFERENCES users(user_id)
        )
    """)

    # Create demonstration analyst account
    existing_user = cursor.execute(
        "SELECT * FROM users WHERE username = ?", ("analyst",)
    ).fetchone()

    if not existing_user:
        cursor.execute("""
            INSERT INTO users (username, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        """, (
            "analyst",
            generate_password_hash("Password1"),
            "Christopher Lyles",
            "Fraud Analyst"
        ))

    # Add sample fraud transactions
    count = cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    if count == 0:
        sample_transactions = [
            ("ACCT-1001", "2026-09-13 08:15", "Electronics World",
             1249.99, "New York, NY", "Online Purchase", 92, "Pending"),

            ("ACCT-1002", "2026-09-13 09:42", "Quick Fuel",
             175.50, "Baltimore, MD", "Card Purchase", 68, "Pending"),

            ("ACCT-1003", "2026-09-13 10:05", "Global Marketplace",
             899.00, "Miami, FL", "Online Purchase", 87, "Pending"),

            ("ACCT-1004", "2026-09-13 11:17", "Metro ATM",
             500.00, "Washington, DC", "ATM Withdrawal", 76, "Pending"),

            ("ACCT-1005", "2026-09-13 12:30", "Luxury Goods Store",
             2140.75, "Las Vegas, NV", "Card Purchase", 95, "Pending")
        ]

        cursor.executemany("""
            INSERT INTO transactions
            (account_id, transaction_date, merchant, amount, location,
             transaction_type, fraud_score, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_transactions)

    conn.commit()
    conn.close()


# ---------------- SECURITY ----------------

def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return decorated_function


# ---------------- COMMON PAGE DESIGN ----------------

def page(title, content):
    username = session.get("full_name", "User")

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ title }} | Fraud Transaction Review System</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Arial, Helvetica, sans-serif;
                background: #f4f6f8;
                color: #263238;
            }

            header {
                background: #17324d;
                color: white;
                padding: 20px 35px;
            }

            header h1 {
                margin: 0;
                font-size: 26px;
            }

            header p {
                margin: 5px 0 0;
                color: #d9e5ef;
            }

            nav {
                background: #244b6b;
                padding: 13px 35px;
            }

            nav a {
                color: white;
                text-decoration: none;
                margin-right: 25px;
                font-weight: bold;
            }

            nav a:hover {
                text-decoration: underline;
            }

            .container {
                max-width: 1150px;
                margin: 30px auto;
                padding: 0 25px;
            }

            .card {
                background: white;
                border-radius: 8px;
                padding: 24px;
                margin-bottom: 20px;
                box-shadow: 0 2px 7px rgba(0,0,0,.08);
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }

            th {
                background: #e8eef3;
                text-align: left;
            }

            th, td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }

            .button {
                display: inline-block;
                padding: 9px 15px;
                background: #1769aa;
                color: white;
                border: none;
                border-radius: 4px;
                text-decoration: none;
                cursor: pointer;
            }

            .danger {
                color: #b71c1c;
                font-weight: bold;
            }

            .medium {
                color: #e65100;
                font-weight: bold;
            }

            .low {
                color: #2e7d32;
                font-weight: bold;
            }

            .stat-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
            }

            .stat {
                background: white;
                padding: 25px;
                border-radius: 8px;
                box-shadow: 0 2px 7px rgba(0,0,0,.08);
            }

            .stat h2 {
                font-size: 34px;
                margin: 5px 0;
                color: #17324d;
            }

            textarea, select {
                width: 100%;
                padding: 10px;
                margin: 8px 0 16px;
            }

            footer {
                text-align: center;
                padding: 25px;
                color: #607d8b;
            }
        </style>
    </head>

    <body>

        <header>
            <h1>Fraud Transaction Review System</h1>
            <p>Phase #1 | SDC480 Software Development Capstone</p>
        </header>

        <nav>
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <a href="{{ url_for('transactions') }}">Transaction Queue</a>
            <a href="{{ url_for('review_history') }}">Review History</a>
            <a href="{{ url_for('logout') }}">Logout</a>
        </nav>

        <div class="container">
            <p>Signed in as <strong>{{ username }}</strong></p>
            """ + content + """
        </div>

        <footer>
            Fraud Transaction Review System | Phase #1
        </footer>

    </body>
    </html>
    """, title=title, username=username)


# ---------------- PAGE 1: LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["user_id"]
            session["full_name"] = user["full_name"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))

        error = "Invalid username or password."

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login | Fraud Transaction Review System</title>

        <style>
            body {
                font-family: Arial, Helvetica, sans-serif;
                background: #17324d;
                margin: 0;
            }

            .login-box {
                width: 420px;
                margin: 110px auto;
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,.25);
            }

            h1 {
                color: #17324d;
                margin-bottom: 5px;
            }

            input {
                width: 100%;
                padding: 12px;
                margin: 8px 0 18px;
                box-sizing: border-box;
            }

            button {
                width: 100%;
                padding: 12px;
                background: #1769aa;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                cursor: pointer;
            }

            .error {
                color: #b71c1c;
                font-weight: bold;
            }

            .demo {
                margin-top: 25px;
                padding: 15px;
                background: #eef4f8;
                border-radius: 5px;
            }
        </style>
    </head>

    <body>
        <div class="login-box">

            <h1>Fraud Transaction Review System</h1>
            <p>Secure Analyst Login</p>

            {% if error %}
                <p class="error">{{ error }}</p>
            {% endif %}

            <form method="POST">

                <label>Username</label>
                <input type="text"
                       name="username"
                       required>

                <label>Password</label>
                <input type="password"
                       name="password"
                       required>

                <button type="submit">Sign In</button>

            </form>

            <div class="demo">
                <strong>Phase #1 Demonstration Account</strong><br><br>
                Username: analyst<br>
                Password: Password1
            </div>

        </div>
    </body>
    </html>
    """, error=error)


# ---------------- PAGE 2: DASHBOARD ----------------

@app.route("/dashboard")
@login_required
def dashboard():

    conn = get_db()

    pending = conn.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE status = 'Pending'
    """).fetchone()[0]

    high_risk = conn.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE fraud_score >= 80
        AND status = 'Pending'
    """).fetchone()[0]

    reviewed = conn.execute("""
        SELECT COUNT(*) FROM reviews
    """).fetchone()[0]

    conn.close()

    content = f"""
        <div class="card">
            <h2>Fraud Operations Dashboard</h2>
            <p>
                This dashboard provides fraud analysts with an overview
                of transactions requiring investigation and completed
                transaction reviews.
            </p>
        </div>

        <div class="stat-grid">

            <div class="stat">
                <p>Pending Transactions</p>
                <h2>{pending}</h2>
            </div>

            <div class="stat">
                <p>High-Risk Transactions</p>
                <h2>{high_risk}</h2>
            </div>

            <div class="stat">
                <p>Completed Reviews</p>
                <h2>{reviewed}</h2>
            </div>

        </div>

        <div class="card" style="margin-top:20px;">
            <h3>Phase #1 Purpose</h3>

            <p>
                The Fraud Transaction Review System provides a centralized
                workflow for analysts to identify suspicious transactions,
                review transaction details, document decisions, and maintain
                an audit history of completed fraud investigations.
            </p>

            <a class="button" href="{url_for('transactions')}">
                Open Transaction Queue
            </a>
        </div>
    """

    return page("Dashboard", content)


# ---------------- PAGE 3: TRANSACTION QUEUE ----------------

@app.route("/transactions")
@login_required
def transactions():

    conn = get_db()

    rows = conn.execute("""
        SELECT * FROM transactions
        ORDER BY fraud_score DESC
    """).fetchall()

    conn.close()

    table_rows = ""

    for row in rows:

        if row["fraud_score"] >= 80:
            risk_class = "danger"
        elif row["fraud_score"] >= 60:
            risk_class = "medium"
        else:
            risk_class = "low"

        table_rows += f"""
            <tr>
                <td>{row['transaction_id']}</td>
                <td>{row['account_id']}</td>
                <td>{row['merchant']}</td>
                <td>${row['amount']:,.2f}</td>
                <td>{row['location']}</td>
                <td class="{risk_class}">
                    {row['fraud_score']}
                </td>
                <td>{row['status']}</td>
                <td>
                    <a class="button"
                       href="{url_for('transaction_details',
                                     transaction_id=row['transaction_id'])}">
                       Review
                    </a>
                </td>
            </tr>
        """

    content = f"""
        <div class="card">

            <h2>Transaction Review Queue</h2>

            <p>
                Transactions are prioritized by fraud risk score.
                Analysts can select a transaction to view detailed
                information and record a review decision.
            </p>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Account</th>
                    <th>Merchant</th>
                    <th>Amount</th>
                    <th>Location</th>
                    <th>Fraud Score</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>

                {table_rows}

            </table>

        </div>
    """

    return page("Transaction Queue", content)


# ---------------- PAGE 4: TRANSACTION DETAILS ----------------

@app.route("/transaction/<int:transaction_id>",
           methods=["GET", "POST"])
@login_required
def transaction_details(transaction_id):

    conn = get_db()

    transaction = conn.execute("""
        SELECT * FROM transactions
        WHERE transaction_id = ?
    """, (transaction_id,)).fetchone()

    if not transaction:
        conn.close()
        return "Transaction not found.", 404

    if request.method == "POST":

        decision = request.form["decision"]
        notes = request.form["notes"]

        conn.execute("""
            INSERT INTO reviews
            (transaction_id, reviewer_id, decision, review_notes)
            VALUES (?, ?, ?, ?)
        """, (
            transaction_id,
            session["user_id"],
            decision,
            notes
        ))

        conn.execute("""
            UPDATE transactions
            SET status = ?
            WHERE transaction_id = ?
        """, (
            decision,
            transaction_id
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("review_history"))

    conn.close()

    content = f"""
        <div class="card">

            <h2>Transaction Details</h2>

            <table>
                <tr>
                    <th>Transaction ID</th>
                    <td>{transaction['transaction_id']}</td>
                </tr>

                <tr>
                    <th>Account ID</th>
                    <td>{transaction['account_id']}</td>
                </tr>

                <tr>
                    <th>Date/Time</th>
                    <td>{transaction['transaction_date']}</td>
                </tr>

                <tr>
                    <th>Merchant</th>
                    <td>{transaction['merchant']}</td>
                </tr>

                <tr>
                    <th>Amount</th>
                    <td>${transaction['amount']:,.2f}</td>
                </tr>

                <tr>
                    <th>Location</th>
                    <td>{transaction['location']}</td>
                </tr>

                <tr>
                    <th>Transaction Type</th>
                    <td>{transaction['transaction_type']}</td>
                </tr>

                <tr>
                    <th>Fraud Risk Score</th>
                    <td><strong>{transaction['fraud_score']}</strong></td>
                </tr>

                <tr>
                    <th>Status</th>
                    <td>{transaction['status']}</td>
                </tr>
            </table>

        </div>

        <div class="card">

            <h2>Analyst Review</h2>

            <form method="POST">

                <label>
                    <strong>Review Decision</strong>
                </label>

                <select name="decision" required>
                    <option value="">Select Decision</option>
                    <option value="Approved">
                        Approve - Legitimate Transaction
                    </option>
                    <option value="Fraud Confirmed">
                        Fraud Confirmed
                    </option>
                    <option value="Escalated">
                        Escalate for Additional Investigation
                    </option>
                </select>

                <label>
                    <strong>Analyst Notes</strong>
                </label>

                <textarea
                    name="notes"
                    rows="5"
                    placeholder="Document the reason for the review decision..."
                    required></textarea>

                <button class="button" type="submit">
                    Submit Review
                </button>

            </form>

        </div>
    """

    return page("Transaction Details", content)


# ---------------- PAGE 5: REVIEW HISTORY ----------------

@app.route("/history")
@login_required
def review_history():

    conn = get_db()

    reviews = conn.execute("""
        SELECT
            r.review_id,
            r.decision,
            r.review_notes,
            r.reviewed_at,
            t.transaction_id,
            t.account_id,
            t.merchant,
            t.amount,
            u.full_name
        FROM reviews r
        JOIN transactions t
            ON r.transaction_id = t.transaction_id
        JOIN users u
            ON r.reviewer_id = u.user_id
        ORDER BY r.reviewed_at DESC
    """).fetchall()

    conn.close()

    if reviews:

        rows = ""

        for review in reviews:
            rows += f"""
                <tr>
                    <td>{review['review_id']}</td>
                    <td>{review['transaction_id']}</td>
                    <td>{review['account_id']}</td>
                    <td>{review['merchant']}</td>
                    <td>${review['amount']:,.2f}</td>
                    <td>{review['decision']}</td>
                    <td>{review['full_name']}</td>
                    <td>{review['reviewed_at']}</td>
                </tr>
            """

        history = f"""
            <table>
                <tr>
                    <th>Review</th>
                    <th>Transaction</th>
                    <th>Account</th>
                    <th>Merchant</th>
                    <th>Amount</th>
                    <th>Decision</th>
                    <th>Analyst</th>
                    <th>Reviewed</th>
                </tr>

                {rows}
            </table>
        """

    else:
        history = """
            <p>
                No completed transaction reviews are currently available.
                Select a transaction from the Transaction Queue to complete
                the first review.
            </p>
        """

    content = f"""
        <div class="card">

            <h2>Fraud Review History</h2>

            <p>
                This page maintains an audit history of completed
                transaction reviews and analyst decisions.
            </p>

            {history}

        </div>
    """

    return page("Review History", content)


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- START APPLICATION ----------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)