from flask import Flask, request, jsonify, make_response
from collections import OrderedDict

app = Flask(__name__)

# Simple in-memory database for students
students = {
    1: {
        "name": "Arun",
        "rollno": 101,
        "marks": {
            "science": 85,
            "english": 78,
            "math": 92,
            "history": 74,
            "geography": 80
        }
    },
    2: {
        "name": "Bala",
        "rollno": 102,
        "marks": {
            "science": 88,
            "english": 82,
            "math": 76,
            "history": 69,
            "geography": 85
        }
    },
    3: {
        "name": "Sriram",
        "rollno": 103,
        "marks": {
            "science": 72,
            "english": 90,
            "math": 81,
            "history": 65,
            "geography": 78
        }
    },
    4: {
        "name": "Kiran",
        "rollno": 104,
        "marks": {
            "science": 91,
            "english": 87,
            "math": 95,
            "history": 80,
            "geography": 89
        }
    },
    5: {
        "name": "Divya",
        "rollno": 105,
        "marks": {
            "science": 84,
            "english": 88,
            "math": 79,
            "history": 90,
            "geography": 92
        }
    }
}

# Helper function to reorder fields
def format_student(student):
    return OrderedDict([
        ("name", student["name"]),
        ("rollno", student["rollno"]),
        ("marks", OrderedDict([
            ("science", student["marks"]["science"]),
            ("english", student["marks"]["english"]),
            ("math", student["marks"]["math"]),
            ("history", student["marks"]["history"]),
            ("geography", student["marks"]["geography"])
        ]))
    ])

# GET all students
@app.route('/students', methods=['GET'])
def get_students():
    formatted_students = OrderedDict((id, format_student(stu)) for id, stu in students.items())
    return jsonify(formatted_students)

# GET single student
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = students.get(id)
    if student:
        return jsonify(format_student(student))
    return jsonify({"error": "Student not found"}), 404

# POST - add a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_id = max(students.keys()) + 1 if students else 1
    students[new_id] = data
    return jsonify({"id": new_id, "student": format_student(data)})

# PUT - update student details fully
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    if id in students:
        students[id] = request.get_json()
        return jsonify(format_student(students[id]))
    return jsonify({"error": "Student not found"}), 404

# PATCH - update student partially
@app.route('/students/<int:id>', methods=['PATCH'])
def patch_student(id):
    if id in students:
        data = request.get_json()
        student = students[id]
        # Update fields if present
        if "name" in data:
            student["name"] = data["name"]
        if "rollno" in data:
            student["rollno"] = data["rollno"]
        if "marks" in data:
            for subject, mark in data["marks"].items():
                student["marks"][subject] = mark
        return jsonify(format_student(student))
    return jsonify({"error": "Student not found"}), 404

# DELETE - remove a student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    if id in students:
        deleted = students.pop(id)
        return jsonify({"deleted": format_student(deleted)})
    return jsonify({"error": "Student not found"}), 404

# HEAD - get only headers (example)
@app.route('/students', methods=['HEAD'])
def head_students():
    response = make_response()
    response.headers["X-Total-Students"] = str(len(students))
    return response

# OPTIONS - allowed methods
@app.route('/students', methods=['OPTIONS'])
def options_students():
    response = make_response()
    response.headers["Allow"] = "GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS"
    return response

# Run app
if __name__ == '__main__':
    app.run(debug=True)
