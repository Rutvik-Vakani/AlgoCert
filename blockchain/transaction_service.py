from algosdk import transaction

from blockchain.account import get_account
from blockchain.algorand_client import get_algod_client


def send_certificate_hash(certificate_hash):

    private_key, sender_address = get_account()

    client = get_algod_client()

    params = client.suggested_params()

    txn = transaction.PaymentTxn(
        sender=sender_address,
        sp=params,
        receiver=sender_address,
        amt=0,
        note=certificate_hash.encode()
    )

    signed_txn = txn.sign(private_key)

    txid = client.send_transaction(signed_txn)

    confirmed_txn = transaction.wait_for_confirmation(
        client,
        txid,
        4
    )

    return {
        "txid": txid,
        "confirmed_round": confirmed_txn["confirmed-round"]
    }