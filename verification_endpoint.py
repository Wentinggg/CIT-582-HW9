from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

'''
Create a REST endpoint that takes a (JSON) object and a signature, 
and verifies that the signatures is valid. 
Your endpoint should accept both signatures generated from Ethereum and Algorand keys.
'''


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    content = request.get_json(silent=True)

    content = json.dumps(content)
    sig = content['sig']
    message = content['payload']['message']
    pk = content['payload']['pk']
    platform = content['payload']['platform']
    # print('Sig: ' + str(sig) + '\nMessage: ' + str(message) + '\npk: ' + str(pk) + '\nplatform: ' + str(platform))

    result = True
    if platform == 'Ethereum':
        # eth_account.Account.enable_unaudited_hdwallet_features()
        # acct, mnemonic = eth_account.Account.create_with_mnemonic()

        # eth_pk = acct.address
        # eth_sk = acct.key

        # payload = "Sign this!"

        eth_encoded_msg = eth_account.messages.encode_defunct(text=message)
        # eth_sig_obj = eth_account.Account.sign_message(eth_encoded_msg, eth_sk)

        # print(eth_sig_obj.messageHash)
        if eth_account.Account.recover_message(eth_encoded_msg, signature=sig) == pk:
            # print("Eth sig verifies!")
            return jsonify(result)

    if platform == 'Algorand':
        # payload = "Sign this!"

        # algo_sk, algo_pk = algosdk.account.generate_account()
        # algo_sig_str = algosdk.util.sign_bytes(message.encode('utf-8'), algo_sk)

        if algosdk.util.verify_bytes(message.encode('utf-8'), sig, pk):
            # print("Algo sig verifies!")
            return jsonify(False)

    # Check if signature is valid
    result = False  # Should only be true if signature validates
    return jsonify(result)


if __name__ == '__main__':
    app.run(port='5002')


