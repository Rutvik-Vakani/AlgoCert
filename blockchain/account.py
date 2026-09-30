from algosdk import account
import os


ACCOUNT_FILE = "blockchain/account.txt"


def get_account():

    if os.path.exists(ACCOUNT_FILE):

        with open(ACCOUNT_FILE, "r") as file:
            private_key = file.read().strip()

        address = account.address_from_private_key(private_key)

        return private_key, address

    private_key, address = account.generate_account()

    with open(ACCOUNT_FILE, "w") as file:
        file.write(private_key)

    return private_key, address


if __name__ == "__main__":

    private_key, address = get_account()

    print("Algorand TestNet Account")
    print("Address:", address)
    print("Account saved locally.")