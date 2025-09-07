from flask import Flask, request, jsonify

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

# GET all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# GET single student
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = students.get(id)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

# POST - add a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_id = max(students.keys()) + 1 if students else 1
    students[new_id] = data
    return jsonify({"id": new_id, "student": data})

# PUT - update student details
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    if id in students:
        students[id] = request.get_json()
        return jsonify(students[id])
    return jsonify({"error": "Student not found"}), 404

# DELETE - remove a student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    if id in students:
        return jsonify({"deleted": students.pop(id)})
    return jsonify({"error": "Student not found"}), 404

# Run app
if __name__ == '__main__':
    app.run(debug=True)
