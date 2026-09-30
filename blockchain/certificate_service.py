import uuid
import sqlite3

from backend.database import DATABASE
from backend.hash_utils import calculate_file_hash
from blockchain.transaction_service import send_certificate_hash


def register_certificate(file_path, student_name, course):
    """
    Register a certificate in the database
    and store its SHA-256 hash on Algorand TestNet.
    """

    certificate_hash = calculate_file_hash(file_path)

    certificate_id = "CERT-" + uuid.uuid4().hex[:8].upper()

    blockchain_result = send_certificate_hash(certificate_hash)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO certificates
        (certificate_id, student_name, course, certificate_hash)
        VALUES (?, ?, ?, ?)
    """, (
        certificate_id,
        student_name,
        course,
        certificate_hash
    ))

    connection.commit()
    connection.close()

    return (
        certificate_id,
        certificate_hash,
        blockchain_result["txid"]
    )