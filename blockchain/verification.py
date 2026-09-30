import base64
import json
from urllib.request import urlopen


INDEXER_URL = "https://testnet-idx.algonode.cloud"


def get_transaction_hash(txid):

    url = f"{INDEXER_URL}/v2/transactions/{txid}"

    with urlopen(url) as response:
        data = json.loads(response.read().decode())

    note = data["transaction"].get("note")

    if note:
        return base64.b64decode(note).decode()

    return None


if __name__ == "__main__":

    txid = "EYLGL54KYO7H24ECX4MJASTZPNRMSMQOWHQLYXZPPQ5PJBVHR2UA"

    certificate_hash = get_transaction_hash(txid)

    print("Certificate hash from Algorand:")
    print(certificate_hash)