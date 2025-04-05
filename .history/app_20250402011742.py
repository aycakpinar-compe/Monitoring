from flask import Flask, render_template, url_for, jsonify, request, redirect, session
import mysql.connector
import bcrypt
import os
from functools import wraps

app = Flask(__name__)
# Set a strong secret key for session encryption
app.secret_key = os.urandom(24)
# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

# Veritabanı bağlantısı
dbconnection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Bitirme.proj.24',
    database='STAJDB',
    autocommit=True
)

# Login required decorator


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session:
            return redirect(url_for('indexroute'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/main')
@login_required
def apppage():
    return render_template('index.html')


@app.route('/')
def indexroute():
    # If user is already logged in, redirect to main page
    if 'userid' in session:
        return redirect(url_for('apppage'))
    return render_template('signin.html')

# Kullanıcı Girişi


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('indexroute'))



@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    try:
        cursor = dbconnection.cursor(dictionary=True)
        if request.method == "POST":
            data = request.get_json()
            user_id = session.get('userid')  # Use session for user ID
            song = data.get('song')
            singer = data.get('singer')
            session_date = data.get('session_date')

            query = "INSERT INTO picked_items (userid, song, singer, session_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user_id, song, singer, session_date))
            dbconnection.commit()
            cursor.close()
            return jsonify({"success": True, "message": "History updated successfully"}), 200

        # GET isteği: Kullanıcının geçmişini getir
        user_id = session.get('userid')  # Use session for user ID
        query = """
            SELECT song, singer, session_date 
            FROM picked_items 
            WHERE userid = %s
            ORDER BY session_date DESC
        """
        cursor.execute(query, (user_id,))
        data = cursor.fetchall()
        cursor.close()
        return render_template("history.html", picked_items=data, len=len(data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a route to check login status for AJAX requests


@app.route('/check-auth')
def check_auth():
    if 'userid' in session:
        return jsonify({"authenticated": True}), 200
    else:
        return jsonify({"authenticated": False}), 401

# Ensure database connections are properly managed


@app.before_request
def before_request():
    if not dbconnection.is_connected():
        dbconnection.reconnect()


if __name__ == "__main__":
    app.run(debug=True)
