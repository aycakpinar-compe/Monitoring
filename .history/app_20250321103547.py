from flask import Flask, render_template, url_for, jsonify, request, redirect
import mysql.connector

app = Flask(__name__)

dbconnection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Bitirme.proj.24',
    database='STAJDB')


@app.route('/main')
def apppage():
    return render_template('index.html')


@app.route('/')
def indexroute():
    return render_template('signin.html')


@app.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        useremail = data.get('useremail')
        userpass = data.get('userpass')

        cursor = dbconnection.cursor()
        query = "SELECT useremail, userpass FROM user WHERE useremail = %s AND userpass = %s"
        cursor.execute(query, (useremail, userpass))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Return success response instead of redirect
            return jsonify({"success": True, "message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        try:
            cursor = dbconnection.cursor()
            data = request.get_json()
            username = data.get('username')
            useremail = data.get('useremail')
            userpass = data.get('userpass')

            query = "INSERT INTO user (username, useremail, userpass) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, useremail, userpass))
            dbconnection.commit()
            cursor.close()

            # Return success response
            return jsonify({"success": True, "message": "User registered successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Bu kısım GET isteği için çalışacak
    return render_template("signup.html")



@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == "POST":
        try:
            cursor = dbconnection.cursor()
            data = request.get_json()
            user_id = data.get('userid')
            song = data.get('song')
            singer = data.get('singer')
            session_date = data.get('session_date')

            query = "INSERT INTO picked_items (userid, song, singer, session_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user_id, song, singer, session_date))
            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({"success": True, "message": "History updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # GET isteği için kullanıcı geçmişini getir
    try:
        cursor = dbconnection.cursor()
        data = request.get_json()
        cursor = curosr.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT song, singer, session_date 
            FROM picked_items 
            WHERE userid = %s
            ORDER BY session_date DESC
        """, (user_id,))
        
        data = cursor.fetchall()
        conn.close()

        return render_template("history.html", picked_items=data, len=len(data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":

    app.run(debug=True)
