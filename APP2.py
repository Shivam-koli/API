from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple in-memory database
salaries = {
    1: {"name": "Arun", "salary": 50000},
    2: {"name": "Bala", "salary": 60000},
    3: {"name": "Sriram", "salary": 30000},
}

# GET all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(salaries)

# GET single employee
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = salaries.get(id)
    if employee:
        return jsonify(employee)
    return jsonify({"error": "Employee not found"}), 404

# POST - add a new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    new_id = max(salaries.keys()) + 1 if salaries else 1
    salaries[new_id] = data
    return jsonify({"id": new_id, "employee": data})

# PUT - update salary or name
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    if id in salaries:
        salaries[id] = request.get_json()
        return jsonify(salaries[id])
    return jsonify({"error": "Employee not found"}), 404

# DELETE - remove an employee
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    if id in salaries:
        return jsonify({"deleted": salaries.pop(id)})
    return jsonify({"error": "Employee not found"}), 404

# Run app
if __name__ == '__main__':
    app.run(debug=True)