import sqlite3

from backend.database import DATABASE
from backend.hash_utils import calculate_file_hash
from blockchain.verification import get_transaction_hash


def verify_certificate(file_path, certificate_id):
    """
    Verify a certificate using:
    1. Local SHA-256 hash
    2. Hash stored in SQLite
    3. Hash stored on Algorand TestNet
    """

    certificate_hash = calculate_file_hash(file_path)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT student_name, course, certificate_hash, transaction_id
        FROM certificates
        WHERE certificate_id = ?
    """, (certificate_id,))

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return {
            "valid": False,
            "message": "Certificate ID not found."
        }

    student_name, course, stored_hash, transaction_id = result

    # Check local certificate against database
    if certificate_hash != stored_hash:
        return {
            "valid": False,
            "message": "Certificate has been modified or is invalid."
        }

    # Check database hash against Algorand
    try:
        blockchain_hash = get_transaction_hash(transaction_id)
    except Exception:
        return {
            "valid": False,
            "message": "Unable to verify certificate on Algorand."
        }

    if blockchain_hash != stored_hash:
        return {
            "valid": False,
            "message": "Blockchain hash mismatch."
        }

    return {
        "valid": True,
        "message": "Certificate is valid.",
        "student_name": student_name,
        "course": course,
        "transaction_id": transaction_id,
        "blockchain_verified": True
    }