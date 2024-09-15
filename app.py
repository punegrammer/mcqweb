from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
import re

app = Flask(__name__)

# Database connection configuration
DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'database': 'sql12731483',
    'user': 'sql12731483',
    'password': 'VsHQsDTI5L'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    roll_no = request.form['roll_no']
    date = request.form['date']
    questions = request.form.getlist('questions[]')
    options = request.form.getlist('options[]')
    correct_options = request.form.getlist('correct_options[]')

    if not roll_no or not date:
        return jsonify({'status': 'error', 'message': 'Please enter Roll No and a date'})

    if not validate_date(date):
        return jsonify({'status': 'error', 'message': 'Date must be in the format dd-mm-yyyy'})

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            cursor = conn.cursor()
            for i in range(len(questions)):
                question = questions[i]
                option_a, option_b, option_c, option_d = options[i*4:i*4+4]
                correct_opt_index = int(correct_options[i])
                correct_opt = chr(65 + correct_opt_index)

                cursor.execute('''
                    INSERT INTO questions (roll_no, date, question, option_a, option_b, option_c, option_d, correct_option)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (roll_no, date, question, option_a, option_b, option_c, option_d, correct_opt))

            conn.commit()
            return jsonify({'status': 'success', 'message': 'Questions Submitted Successfully!'})

    except Error as e:
        return jsonify({'status': 'error', 'message': f'Error: {e}'})
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def validate_date(date):
    date_regex = r'^\d{2}-\d{2}-\d{4}$'
    return re.match(date_regex, date) is not None

if __name__ == "__main__":
    app.run(debug=True)
