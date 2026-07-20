from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import time

app = Flask(__name__)
CORS(app)


# ----------------------------
# Database Connection
# ----------------------------
def get_connection():

    while True:
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "mysql"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "root"),
                database=os.getenv("DB_NAME", "student_feedback")
            )

            return connection

        except mysql.connector.Error:
            print("Waiting for MySQL...")
            time.sleep(5)


# ----------------------------
# Home Route
# ----------------------------
@app.route("/")
def home():

    return jsonify({
        "message": "Student Feedback Backend Running"
    })


# ----------------------------
# Health Check
# ----------------------------
@app.route("/health")
def health():

    return jsonify({
        "status": "Healthy"
    })


# ----------------------------
# Submit Feedback
# ----------------------------
@app.route("/feedback", methods=["POST"])
def submit_feedback():

    data = request.get_json()

    name = data["name"]
    email = data["email"]
    course = data["course"]
    rating = data["rating"]
    feedback = data["feedback"]

    connection = get_connection()

    cursor = connection.cursor()

    query = """
    INSERT INTO feedback
    (name,email,course,rating,feedback)
    VALUES(%s,%s,%s,%s,%s)
    """

    values = (
        name,
        email,
        course,
        rating,
        feedback
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Feedback Submitted Successfully"
    }), 201


# ----------------------------
# Get All Feedback
# ----------------------------
@app.route("/feedback", methods=["GET"])
def get_feedback():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
    id,
    name,
    email,
    course,
    rating,
    feedback,
    created_at
    FROM feedback
    ORDER BY id DESC
    """

    cursor.execute(query)

    feedback = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(feedback)


# ----------------------------
# Start Application
# ----------------------------
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
