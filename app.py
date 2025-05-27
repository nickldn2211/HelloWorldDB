import mysql.connector
from flask import Flask, jsonify
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# MySQL database connection details from environment
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

@app.route('/')
def hello():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        conn.close()
        return "Hello, World! ✅ Database Connected Successfully"
    except Exception as e:
        return f"❌ Database connection failed: {str(e)}"

@app.route('/users')
def get_users():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(users), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

