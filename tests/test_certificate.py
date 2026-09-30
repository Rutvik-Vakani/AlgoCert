from backend.verification_service import verify_certificate


file_path = "database/sample_certificate.txt"

certificate_id = "CERT-DF240AEC"

result = verify_certificate(
    file_path,
    certificate_id
)

print("\nVerification Result:")
print(result)