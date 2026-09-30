# AlgoCert

AlgoCert is a certificate registration and verification prototype that anchors a certificate's SHA-256 fingerprint to the Algorand TestNet. Certificate details and the transaction ID are stored in a local SQLite database; the certificate file itself is not written to the blockchain.

## Problem Statement

Paper and digital certificates can be altered or presented without a reliable way for a recipient to confirm their integrity and issuer-provided details. A verification process should make tampering detectable and provide an independently queryable record of the certificate fingerprint.

## Objectives

- Generate a certificate ID and record the student's name, course, file hash, and transaction ID locally.
- Anchor the file's SHA-256 hash in an Algorand TestNet transaction note.
- Verify a submitted file against both the local record and the on-chain hash.
- Provide a small browser interface for registration and verification.

## Current Features

- Flask endpoints for the web page, registration, and verification.
- SHA-256 hashing of uploaded certificate files.
- SQLite persistence for certificate metadata and transaction IDs.
- Zero-value Algorand self-payment transactions with the hash in the transaction note.
- Algorand Indexer lookup during verification.
- A sample text certificate in `database/sample_certificate.txt`.

## Technology Stack

- Python, Flask, and the Algorand Python SDK (`py-algorand-sdk`)
- SQLite
- Algorand TestNet via AlgoNode's public algod and Indexer endpoints
- HTML and JavaScript

## Project Structure

```text
AlgoCert/
|-- backend/       Flask app, database setup, hashing, registration, verification
|-- blockchain/    Algorand account, client, transaction, and lookup helpers
|-- database/      Sample certificate and runtime database/upload files
|-- docs/          Project documentation (currently empty)
|-- frontend/      Browser interface
|-- tests/         Verification smoke-test script
|-- .gitignore
`-- README.md
```

The SQLite database and uploaded certificate files are generated locally and are intentionally excluded from Git.

## Run Locally

From the repository root in PowerShell, create and activate a virtual environment, then install the application's dependencies:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install Flask py-algorand-sdk
```

Initialize the local SQLite schema and start the Flask development server:

```powershell
python -m backend.database
python -m backend.app
```

Open <http://127.0.0.1:5000/>. The development server is configured with Flask debug mode; use it only for local development, not as a public production server.

Registration requires an Algorand TestNet account with enough TestNet ALGO to cover transaction fees. On first use, `blockchain/account.py` generates a key pair and writes its private key to `blockchain/account.txt`. That file is ignored by Git. Fund the displayed address using an Algorand TestNet faucet before registering a certificate. Keep the private key local and never publish or share it. The application currently uses AlgoNode's public TestNet endpoints and an empty algod token; it does not load credentials from `.env`.

## Registration and Verification Workflow

1. Submit the student's name, course, and certificate file through the registration form.
2. The backend calculates the file's SHA-256 digest, creates a certificate ID, and submits a zero-value self-payment with the digest encoded in its note.
3. The certificate ID, student/course details, digest, and confirmed transaction ID are stored in `database/algocert.db`.
4. To verify, submit the certificate ID and the certificate file. The backend hashes the upload, checks it against the SQLite record, then retrieves the transaction note from the TestNet Indexer and compares that hash too.
5. A successful response includes the recorded student and course details and confirms blockchain verification.

## Tamper Detection

Any change to the uploaded file changes its SHA-256 digest. A mismatch with the local record is rejected as modified or invalid. If the database digest does not match the digest retrieved from the Algorand transaction, verification is also rejected. A missing certificate ID or an unavailable Indexer does not produce a successful verification.

The blockchain record is a hash anchor, not the certificate document or a digital signature proving the issuer's identity. The current implementation also depends on the local SQLite record to map a certificate ID to its transaction.

## Tests

`tests/test_certificate.py` is a manual verification smoke-test script, not an automatically discovered unit-test suite. It contains a fixed certificate ID and requires a matching local database record and accessible TestNet transaction to pass. For a basic end-to-end check, register `database/sample_certificate.txt` in the web form and verify the same file using the returned certificate ID.

## Algorand TestNet Integration

Transactions are submitted to `https://testnet-api.algonode.cloud`; verification queries `https://testnet-idx.algonode.cloud`. Both are public TestNet services, so transactions and their notes are visible on the network. The transaction note contains the certificate digest; do not put personal information or the certificate itself in it. TestNet ALGO has no mainnet value. This project does not deploy a smart contract.

## Future Enhancements

- Add automated unit and integration tests with mocked Algorand clients.
- Move account secrets to a dedicated secret manager and support configurable endpoints.
- Add issuer authentication, authorization, and signed issuance records.
- Improve upload validation, error handling, and production deployment security.
- Support richer certificate formats, revocation, and a public verification interface.
- Make the local persistence layer optional by resolving certificate records through a durable service or on-chain application.