    from flask import Flask,request,jsonify,redirect,session
    from flask_cors import CORS
    from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
    import os
    import mysql.connector
    from flask_cors import CORS
    from werkzeug.security import generate_password_hash, check_password_hash
    from email_utils import send_registration_email
    from flask_mail import Mail, Message
    import random

    def dbconnect():
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sainath@1322",
        database="inventory_db"
        ) 
        return mydb




    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)


    app.config['SECRET_KEY']="thisistodoappsecretkey"
    app.config["JWT_SECRET_KEY"] = "thisistodoappjwtsuperkey"

    app.config["MAIL_SERVER"]='smtp.gmail.com'
    app.config["MAIL_PORT"]=465
    app.config['MAIL_USERNAME'] = 'sainathreddy.unf12@gmail.com'
    app.config['MAIL_PASSWORD'] = 'wew hdfd her ead'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)

    jwt = JWTManager(app)

    @app.route('/')
    def index():
        return "Hello World...."

    @app.route('/register', methods=['POST'])
    def register():
        if request.method=="POST":
            data=request.get_json()
            # print("data ",data)
            username = data['username']
            email = data['email']
            password = data['password']
            mydb = dbconnect()
            cursor=mydb.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s ",(username,))
            username_exists=cursor.fetchone()
            cursor.close()
            #checking email id exists or not
            mydb = dbconnect()
            cursor=mydb.cursor()
            cursor.execute("SELECT * FROM users WHERE email=%s ",(email,))
            email_exists=cursor.fetchone()
            cursor.close()

            if username_exists:
                return {"message":"Username already taken"},409
            elif email_exists:
                return {"message":"Email already taken"},409
            else:
                random_number=random.randint(100000,900000)
                mydb = dbconnect()
                mycursor1=mydb.cursor()
                sql="INSERT INTO users(username,email,password,role,otp) VALUES (%s,%s,%s,%s,%s)"
                # hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
                # print("hashed_password",hashed_password)
                # val= (username,email,hashed_password,"user")
                val= (username,email,password,"user",random_number)
                try:
                    mycursor1.execute(sql,val)
                    mydb.commit()
                    mycursor1.close()
                    msg = Message(subject='Welcome To Inventory Management', sender='sainathreddy.unf12@gmail.com', recipients=[email])
                    msg.html = f"""
                            <!DOCTYPE html>
                            <html>
                            <head>
                            <meta charset="UTF-8">
                            <title>Welcome</title>
                            </head>
                            <body style="margin: 0; padding: 0; background-image: url('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?fit=crop&w=1400&q=80'); background-size: cover; background-position: center; font-family: Arial, sans-serif;">
                            <div style="background-color: rgba(255, 255, 255, 0.85); max-width: 600px; margin: 60px auto; padding: 40px; border-radius: 10px; text-align: center;">
                                <h1 style="color: #333;">Welcome to Inventory Management!</h1>
                                <p style="font-size: 16px; color: #555;">Hi <strong>{val[0]}</strong>,</p>
                                <p style="font-size: 16px; color: #555;">
                                We're excited to have you onboard! Your account has been successfully created.
                                You can now start managing your inventory efficiently and seamlessly.
                                </p>
                                <p style="font-size: 16px; color: #555;">
                                If you have any questions, feel free to reply to this email. We're here to help!
                                </p>
                                <p style="margin-top: 30px; font-size: 14px; color: #aaa;">– The Inventory Management Team</p>
                            </div>
                            </body>
                            </html>
                            """
                    mail.send(msg)
                    print("Email sent!")
                except Exception as e:
                    mydb.rollback()  
                    raise e

            return {"message":"Created"},201
        else:
            return {"message":"Invalid request"},400

    @app.route('/login',methods=['POST'])
    def login():
        if request.method=='POST':
            print("In post")
            data=request.get_json()
            username=data['username']
            password=data['password']
            mydb = dbconnect()
            cursor=mydb.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s and password=%s",(username,password))
            exists=cursor.fetchone()
            cursor.close()
            if exists:
                role=exists[4]
                session['email'] = exists[2]
                random_number=random.randint(100000,900000)
                mydb = dbconnect()
                cursor=mydb.cursor()
                cursor.execute("UPDATE users SET otp=%s WHERE email=%s ",(random_number,session['email']))
                mydb.commit()
                cursor.close()
                msg = Message(subject='OTP to Login to your account', sender='sainathreddy.unf12@gmail.com', recipients=[session['email']])
                msg.html = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                        <meta charset="UTF-8">
                        <title>Welcome</title>
                        </head>
                        <body style="margin: 0; padding: 0; background-image: url('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?fit=crop&w=1400&q=80'); background-size: cover; background-position: center; font-family: Arial, sans-serif;">
                        <div style="background-color: rgba(255, 255, 255, 0.85); max-width: 600px; margin: 60px auto; padding: 40px; border-radius: 10px; text-align: center;">
                            <h1 style="color: #333;">Here is you OTP</h1>
                            <p style="font-size: 16px; color: #555;">Hi <strong>{exists[1]}</strong>,</p>
                            <p style="font-size: 16px; color: #555;">
                            Here is OTP to login into your account : {random_number}
                            </p>
                            <p style="font-size: 16px; color: #555;">
                            If you have any questions, feel free to reply to this email. We're here to help!
                            </p>
                            <p style="margin-top: 30px; font-size: 14px; color: #aaa;">– The Inventory Management Team</p>
                        </div>
                        </body>
                        </html>
                        """
                mail.send(msg)
                print("Email sent!")

                # return redirect('/otpvalidation')
                return {"message":"opt sent","role":role},200
            else:
                return {"message":"Invalid credentials"},409

        else:
            return {"message":"Invalid request"},400

    @app.route('/otpvalidation',methods=['POST'])
    def otpvalidation():
        if request.method=='POST':
            data=request.get_json()
            otp=data['otp']
            email = session.get('email')
            if not email:
                return {"message": "Session expired or email missing"}, 401
            mydb = dbconnect()
            cursor=mydb.cursor()
            cursor.execute("SELECT * FROM users WHERE email=%s AND otp=%s", (email, otp))
            exists=cursor.fetchone()
            cursor.close()
            if exists:
                return {"message": "OTP validated successfully"}, 200
            else:
                return {"message": "Invalid OTP"}, 401




    if __name__ == '__main__':  
        app.run(debug=True,port=5000)
