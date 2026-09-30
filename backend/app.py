from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory

from backend.certificate_service import register_certificate
from backend.verification_service import verify_certificate


app = Flask(__name__)
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/script.js")
def script():
    return send_from_directory(FRONTEND_DIR, "script.js")


@app.route("/register", methods=["POST"])
def register():

    file = request.files.get("certificate")
    student_name = request.form.get("student_name")
    course = request.form.get("course")

    if not file or not student_name or not course:
        return jsonify({
            "success": False,
            "message": "Certificate, student name, and course are required."
        }), 400

    file_path = "database/uploaded_certificate.txt"

    file.save(file_path)

    certificate_id, certificate_hash, transaction_id = register_certificate(
        file_path,
        student_name,
        course
    )

    return jsonify({
        "success": True,
        "certificate_id": certificate_id,
        "certificate_hash": certificate_hash,
        "transaction_id": transaction_id
    })


@app.route("/verify", methods=["POST"])
def verify():

    file = request.files.get("certificate")
    certificate_id = request.form.get("certificate_id")

    if not file or not certificate_id:
        return jsonify({
            "success": False,
            "message": "Certificate file and Certificate ID are required."
        }), 400

    file_path = "database/verify_certificate.txt"

    file.save(file_path)

    result = verify_certificate(
        file_path,
        certificate_id
    )

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)