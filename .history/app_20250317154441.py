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
        email = data.get('useremail')
        psw = data.get('userpass')

        cursor = dbconnection.cursor()
        # Veritabanında kullanıcıyı sorgulamak
        query = "SELECT useremail, userpass FROM user WHERE useremail = %s AND userpass = %s"
        cursor.execute(query, (email, psw))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Başarılı girişte yönlendirme yapılır
            return redirect('/main')
        else:
            # Hatalı girişte hata mesajı döndürülür
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        try:
            cursor = dbconnection.cursor()
            # queryilk = "SELECT useremail, userpass FROM user WHERE useremail = %s AND userpass = %s"
            data = request.get_json()
            username = data.get('user_name')
            useremail = data.get('useremail')
            userpass = data.get('userpass')
            # cursor.execute(queryilk, (username, useremail, userpass))
            user = cursor.fetchone()
            # if user:
            # return jsonify({"kullanici var": str(e)}), 505
            # else:

            query = "INSERT INTO user (username, useremail, userpass) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, useremail, userpass))
            dbconnection.commit()
            cursor.close()

            # Başarılıysa signin sayfasına yönlendir
            return jsonify({"kullanici giris yapti": str(e)}), 200
        except Exception as e:
            return jsonify({"kullanici olusturulamadi": str(e)}), 500
    return render_template("signup.html")


@app.route('/history', methods=['GET'])
def get_history(userid, session_date):
    try:
        cursor = dbconnection.cursor()
        cursor.execute("SELECT userid , session_date from picked_items ")
        data = cursor.fetchall()
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
        if data != 0:
            return jsonify(data)
        else:
            return '<h3>there is no a history so far</h3>'
    except Exception as e:
        return jsonify({"kullaniciya ait veri bulunamadi": str(e)}), 404


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
