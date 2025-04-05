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
    host='localhost',  # hata:host.docker.internal bunu dockerla calistircaksan kesin degistir
    user='root',
    password='Bitirme.proj.24',
    database='stajdb',
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
# Kullanıcı Girişi


@app.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        useremail = data.get('useremail')
        userpass = data.get('userpass')

        cursor = dbconnection.cursor(dictionary=True)
        query = "SELECT userid, username, userpass FROM user WHERE useremail = %s "
        cursor.execute(query, (useremail,))
        user = cursor.fetchone()
        cursor.close()

        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        # Try standard bcrypt check first
        try:
            stored_hash = user['userpass'].encode('utf-8')
            is_valid = bcrypt.checkpw(userpass.encode('utf-8'), stored_hash)
            if is_valid:
                session['userid'] = user['userid']
                session['username'] = user['username']
                session['email'] = useremail
                return jsonify({"success": True, "message": "Login successful"}), 200
        except Exception as password_error:
            # If bcrypt check fails, try direct comparison (for non-hashed passwords)
            if user['userpass'] == userpass:
                # Store user data in session
                session['userid'] = user['userid']
                session['username'] = user['username']
                session['email'] = useremail

                # Optionally update to hashed password if column size allows
                try:
                    cursor = dbconnection.cursor()
                    hashed = bcrypt.hashpw(
                        userpass.encode('utf-8'), bcrypt.gensalt())
                    update_query = "UPDATE user SET userpass = %s WHERE userid = %s"
                    cursor.execute(
                        update_query, (hashed.decode('utf-8'), user['userid']))
                    dbconnection.commit()
                    cursor.close()
                except Exception:
                    # Silently fail if update doesn't work
                    pass

                return jsonify({"success": True, "message": "Login successful"}), 200

        # If we get here, password was invalid
        return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Kullanıcı Kaydı


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user is already logged in, redirect to main page
    if 'userid' in session:
        return redirect(url_for('apppage'))

    if request.method == "POST":
        try:
            data = request.get_json()
            username = data.get('username')
            useremail = data.get('useremail')
            userpass = data.get('userpass')

            # Check if user already exists
            cursor = dbconnection.cursor(dictionary=True)
            check_query = "SELECT userid FROM user WHERE useremail = %s"
            cursor.execute(check_query, (useremail,))
            existing_user = cursor.fetchone()

            if existing_user:
                return jsonify({"error": "Email already registered"}), 409

            # First try to hash the password
            try:
                # Şifreyi hashle
                hashed_password = bcrypt.hashpw(userpass.encode(
                    'utf-8'), bcrypt.gensalt()).decode('utf-8')

                # Check if hashed password would be too long for column
                cursor.execute(
                    "SELECT CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'user' AND COLUMN_NAME = 'userpass'")
                max_length = cursor.fetchone()['CHARACTER_MAXIMUM_LENGTH']

                # If hash is too long, store plain password temporarily and notify
                if max_length and len(hashed_password) > max_length:
                    print(
                        f"WARNING: userpass column is too small ({max_length}) for bcrypt hash ({len(hashed_password)})")
                    password_to_store = userpass  # Store plain password as fallback
                else:
                    password_to_store = hashed_password  # Store the hash
            except Exception as hash_error:
                # If hashing fails for any reason, store plain password temporarily
                print(f"WARNING: Failed to hash password: {str(hash_error)}")
                password_to_store = userpass

            # Insert the user
            insert_query = "INSERT INTO user (username, useremail, userpass) VALUES (%s, %s, %s)"
            cursor.execute(
                insert_query, (username, useremail, password_to_store))
            dbconnection.commit()

            # Get the new user's ID
            cursor.execute("SELECT LAST_INSERT_ID() as userid")
            user_id = cursor.fetchone()['userid']
            cursor.close()

            # Log the user in
            session['userid'] = user_id
            session['username'] = username
            session['email'] = useremail

            return jsonify({"success": True, "message": "User registered successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template("signup.html")


@app.route('/history', methods=['GET', 'POST'])
def history():
    try:
        # POST isteği işleniyor
        if request.method == "POST":
            cursor = dbconnection.cursor(dictionary=True)
            data = request.get_json()  # JSON verisini alıyoruz
            # Kullanıcı ID'sini session'dan alıyoruz
            user_id = session.get('userid')
            picked_song = data.get('pickedsong')  # Seçilen şarkı
            session_date = data.get('session_date')  # Seçilen zaman
            print(user_id, picked_song, session_date)
            # Veritabanına kaydediyoruz
            query = "INSERT INTO picked_items (picked_song, session_date, userid) VALUES (%s, %s, %s)"
            cursor.execute(query, (picked_song, session_date, user_id))
            dbconnection.commit()  # Değişiklikleri kaydediyoruz
            cursor.close()
            return jsonify({"success": True, "message": "History updated successfully"}), 200

        cursor = dbconnection.cursor(dictionary=True)
        # Kullanıcı ID'sini session'dan alıyoruz
        user_id = session.get('userid')

        query = """
            SELECT p.picked_song, p.session_date, s.SingerName
            FROM picked_items p
            JOIN songs song ON p.picked_song = song.Songid
            JOIN singer s ON song.SingerID = s.SingerID
            WHERE p.userid = %s
ORDER BY p.session_date DESC;

         """

        cursor.execute(query, (user_id,))
        data = cursor.fetchall()  # Sonuçları alıyoruz
        cursor.close()
        return render_template("history.html", picked_items=data, len=len(data))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
