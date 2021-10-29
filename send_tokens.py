#!/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from algosdk import account

# Connect to Algorand node maintained by PureStake
# Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
# algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
    "X-API-Key": algod_token,
}

acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000  # https://developer.algorand.org/docs/features/accounts/#minimum-balance

'''
Your function should create a transaction that sends “amount” microalgos 
to the account given by “receiver_pk” and submit the transaction to the Algorand Testnet.
Your function should return the address of the sender (“sender_pk”) as well as 
the id of the resulting transaction (“txid”) as it appears on the Testnet blockchain.
'''
def send_tokens(receiver_pk, tx_amount):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last

    # Your code here
    private_key_sender, sender_pk = account.generate_account()
    mnemonic_secret = "skirting trash phase buckets apology gags sedan coffee vinegar else " \
                      "fifteen pitched idled gorilla siren cucumber urban junk vastness laboratory " \
                      "rift rhino situated taxi"
    sk = mnemonic.to_private_key(mnemonic_secret)
    pk = mnemonic.to_public_key(mnemonic_secret)
    # passphrase = mnemonic.from_private_key(private_key_sender)
    # account_public_key = mnemonic.to_public_key(tx_amount)
    tx = transaction.PaymentTxn(sender_pk, tx_fee, first_valid_round,
                                last_valid_round, gen_hash, receiver_pk, tx_amount, flat_fee=True)
    stx = tx.sign(sk)
    txid = acl.send_transaction(stx)
    # txid = stx.transaction.get_txid()

    return sender_pk, txid


# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo
