from flask import Flask, render_template, url_for, jsonify, request, redirect
import mysql.connector
import bcrypt  # Şifre hashleme için

app = Flask(__name__)

# Veritabanı bağlantısı
dbconnection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Bitirme.proj.24',
    database='STAJDB',
    autocommit=True  # Veri kaybını önler
)


@app.route('/main')
def apppage():
    return render_template('index.html')


@app.route('/')
def indexroute():
    return render_template('signin.html')

# Kullanıcı Girişi


@app.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        useremail = data.get('useremail')
        userpass = data.get('userpass')

        cursor = dbconnection.cursor(dictionary=True)
        query = "SELECT userpass FROM user WHERE useremail = %s"
        cursor.execute(query, (useremail,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.checkpw(userpass.encode('utf-8'), user['userpass'].encode('utf-8')):
            return jsonify({"success": True, "message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Kullanıcı Kaydı


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        try:
            data = request.get_json()
            username = data.get('username')
            useremail = data.get('useremail')
            userpass = data.get('userpass')

            # Şifreyi hashle
            hashed_password = bcrypt.hashpw(
                userpass.encode('utf-8'), bcrypt.gensalt())

            cursor = dbconnection.cursor()
            query = "INSERT INTO user (username, useremail, userpass) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, useremail,
                           hashed_password.decode('utf-8')))
            dbconnection.commit()
            cursor.close()

            return jsonify({"success": True, "message": "User registered successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return render_template("signup.html")

# Kullanıcı Geçmişi


@app.route('/history', methods=['GET', 'POST'])
def history():
    try:
        cursor = dbconnection.cursor(dictionary=True)

        if request.method == "POST":
            data = request.get_json()
            user_id = data.get('userid')
            song = data.get('song')
            singer = data.get('singer')
            session_date = data.get('session_date')

            query = "INSERT INTO picked_items (userid, song, singer, session_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user_id, song, singer, session_date))
            dbconnection.commit()
            cursor.close()

            return jsonify({"success": True, "message": "History updated successfully"}), 200

        # GET isteği: Kullanıcının geçmişini getir
        user_id = request.args.get('userid')
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


if __name__ == "__main__":
    app.run(debug=True)
