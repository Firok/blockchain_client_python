import binascii
from collections import OrderedDict

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class Transaction:
    def __init__(self, data):
        self.sender_address = data.get('sender_address')
        self.sender_private_key = data.get('sender_private_key')
        self.receiver_address = data.get('receiver_address')
        self.value = data.get('value')

    def __getattr__(self, item):
        return self.data[item]

    def to_dict(self):
        return OrderedDict({'sender_address': self.sender_address,
                            'receiver_address': self.receiver_address,
                            'value': self.value})

    def sign_transaction(self):
        """
        Sign transaction with private key
        :return:
        """
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))  # rsa_key
        signer = PKCS1_v1_5.new(private_key)
        msg_hash = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(msg_hash)).decode('ascii')
