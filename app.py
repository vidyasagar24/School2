from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# ---------------- Database Setup ----------------
def get_db():
 #   client = MongoClient(
 #       os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
 #   )
 #   db = client[os.environ.get("MONGO_DB", "school")]
    client = MongoClient("mongodb+srv://vidyasagar24_db_user:Sankeerth29@cluster0.mongodb.net/school")
    db = client["school"]

    return db

db = get_db()
students_collection = db["students"]

# ---------------- Routes ----------------
@app.route("/")
def index():
    students = list(students_collection.find())
    return render_template("index.html", students=students)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student = {
            "name": request.form["name"],
            "class": request.form["class"],
            "address": request.form["address"],
            "phone": request.form["phone"],
            "fee": float(request.form["fee"]),
            "dob": request.form["dob"]
        }
        students_collection.insert_one(student)
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_student(id):
    student = students_collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        updated_student = {
            "name": request.form["name"],
            "class": request.form["class"],
            "address": request.form["address"],
            "phone": request.form["phone"],
            "fee": float(request.form["fee"]),
            "dob": request.form["dob"]
        }
        students_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": updated_student}
        )
        return redirect(url_for("index"))

    return render_template("edit.html", student=student)

@app.route("/delete/<id>")
def delete_student(id):
    students_collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("index"))

@app.route("/search", methods=["GET", "POST"])
def search_student():
    students = []
    if request.method == "POST":
        keyword = request.form["keyword"]
        students = list(students_collection.find({
            "$or": [
                {"name": {"$regex": keyword, "$options": "i"}},
                {"class": {"$regex": keyword, "$options": "i"}}
            ]
        }))
    return render_template("search.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)


