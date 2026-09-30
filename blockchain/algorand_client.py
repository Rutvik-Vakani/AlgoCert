from algosdk.v2client import algod

from blockchain.algorand_config import ALGOD_ADDRESS, ALGOD_TOKEN


def get_algod_client():
    return algod.AlgodClient(
        ALGOD_TOKEN,
        ALGOD_ADDRESS
    )


if __name__ == "__main__":
    client = get_algod_client()

    status = client.status()
    
    
    print("Connected to Algorand TestNet")
    print("Last round:", status["last-round"])