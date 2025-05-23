import pymssql
from flask import Flask, jsonify

app = Flask(__name__)

# Database connection details
DB_SERVER = "NGUYEN-ASUS-LAPTOP\\MSSQLSERVER04"  # Your SQL Server instance
DB_NAME = "HelloWorldDB"

@app.route('/')
def hello():
    return "Hello, World! Database Connected Successfully"

@app.route('/users')
def get_users():
    try:
        # Establish a fresh connection per request
        conn = pymssql.connect(server=DB_SERVER, database=DB_NAME)
        cursor = conn.cursor()

        # Fetch users from the database
        cursor.execute("SELECT * FROM HelloWorldDB.dbo.Users")
        column_names = [col[0] for col in cursor.description]  # Get column headers
        users = [dict(zip(column_names, row)) for row in cursor.fetchall()]  # Format data properly
        
        conn.close()  # Close connection after retrieving data
        return jsonify(users), 200  # Return structured JSON response

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error if query fails

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
