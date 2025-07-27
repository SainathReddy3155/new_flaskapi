from flask import Flask,request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_pymongo import PyMongo
from pymongo import MongoClient
import os


app = Flask(__name__)

app.config['SECRET_KEY']="thisistodoappsecretkey"
app.config["JWT_SECRET_KEY"] = "thisistodoappjwtsuperkey"

##connecting mongodb client 
client=MongoClient("localhost:27017")

# =========REPALCE dbpassword WITH the original password================


##connecting database

db=client['Flaskapp']

jwt = JWTManager(app)

@app.route('/')
def index():
    return "Hello World...."

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    print("username",username)
    collection=db['usercredentials']
    print("collection:" ,collection)
    exists=collection.find_one({"username":username,"password":password})
    if exists:
        access_token = create_access_token(identity=username)
        return {"access_token": access_token}, 200
    else:
        return {"msg": "Invalid credentials"}, 401

@app.route("/createuser", methods=["POST"])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    if request.method=="POST":
        emp_id=request.form.get("emp_id")
        name=request.form.get("name")
        address=request.form.get("address")
        print(emp_id,name,address)
 
        collection=db['employeedetails']
       
        exists=collection.find_one({"emp_id":emp_id})
        if exists:
            print("Employee id already exists")
            errormessage="Employee id already exists"
            return {"message": "Employee id already exists"},404
        else:
            data={"emp_id":emp_id,"name":name,"address":address}
            collection.insert_one(data)
            print("data inserted successfully")
            successmessage="Employee Added successfully"
            return {"message":"Employee Added successfully"},200

    return {"message":"Invalid request"},400

@app.route("/updateuser", methods=["PUT"])
@jwt_required()
def updateuser():
    current_user = get_jwt_identity()
    if request.method=="PUT":
        emp_id=request.form.get("emp_id")
        name=request.form.get("name")
        address=request.form.get("address")
        print(emp_id,name,address)
 
        collection=db['employeedetails']
        exists=collection.find_one({"emp_id":emp_id})
        final_update_data={}
        if exists:
            if name:
                final_update_data["name"] = name
            if address:
                final_update_data["address"] = address
            collection.update_one({"emp_id": emp_id}, {"$set": final_update_data})
            print("Employee updated successfully")
            return {"message":"Employee updated successfully"}, 200

        else:
            return {"message":"Employee Details Not Found"},404
    return {"message":"Invalid request"},400

@app.route("/deleteuser", methods=["DELETE"])
@jwt_required()
def delete_user():
    current_user = get_jwt_identity()
    if request.method == "DELETE":
        emp_id = request.form.get("emp_id")
        collection = db["employeedetails"]
        exists = collection.find_one({"emp_id": emp_id})

        if exists:
            collection.delete_one({"emp_id": emp_id})
            print("Employee deleted successfully")
            return {"message":"Employee deleted successfully"}, 200
        else:
            print("Employee Details not found")
            return {"message":"Employee Details Not Found"},404
    return {"message":"Invalid request"},400

if __name__ == '__main__':  
    app.run(debug=True,port=5000)