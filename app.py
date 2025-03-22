from flask import Flask, request, jsonify, render_template
import mysql.connector

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'fallback-secret')

# Database Configuration
db_config = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json  # Expecting JSON payload with 'Id' and 'pwd'
    user_id = data.get('Id')
    password = data.get('pwd')

    if not user_id or not password:
        return jsonify({'Authenticated': False, 'Type': None, 'Error': 'Missing credentials'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM auth WHERE ID = %s AND pwd = %s"
        cursor.execute(query, (user_id, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return jsonify({'Authenticated': True, 'Type': user['type']})
        else:
            return jsonify({'Authenticated': False, 'Type': None})

    except mysql.connector.Error as err:
        return jsonify({'Authenticated': False, 'Type': None, 'Error': str(err)}), 500

@app.route('/get_student_by_id', methods=['POST'])
def get_student_by_id():
    data = request.json
    student_id = data.get('S_ID')

    if not student_id:
        return jsonify({'error': 'Missing student ID'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Student WHERE S_ID = %s"
        cursor.execute(query, (student_id,))
        student = cursor.fetchone()

        cursor.close()
        conn.close()

        if student:
            return jsonify(student)
        else:
            return jsonify({'error': 'Student not found'}), 404

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

@app.route('/get_employee_by_id', methods=['POST'])
def get_employee_by_id():
    data = request.json
    employee_id = data.get('Employee_ID')

    if not employee_id:
        return jsonify({'error': 'Missing Employee ID'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Employees WHERE Employee_ID = %s"
        cursor.execute(query, (employee_id,))
        employee = cursor.fetchone()

        cursor.close()
        conn.close()

        if employee:
            return jsonify(employee)
        else:
            return jsonify({'error': 'Employee not found'}), 404

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

