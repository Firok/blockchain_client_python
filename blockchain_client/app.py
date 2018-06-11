import binascii

import Crypto.Random
from Crypto.PublicKey import RSA
from flask import Flask, render_template, jsonify, request

from .models import Transaction

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('./home.html')


@app.route('/transactions/make')
def make_transaction():
    return render_template('./make_transaction.html')


@app.route('/transactions')
def view_transaction():
    return render_template('./view_transaction.html')


@app.route('/wallet/create_new', methods=['GET'])
def create_new_wallet():
    random_gen = Crypto.Random.new().read
    bits = 1024
    private_key = RSA.generate(bits, random_gen)
    public_key = private_key.publickey()
    response = {
        'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
        'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
    }

    return jsonify(response), 200


@app.route('/transactions/generate', methods=['POST'])
def generate_transaction():
    data = {'sender_address': request.form['sender_address'],
            'sender_private_key': request.form['sender_private_key'],
            'receiver_address': request.form['receiver_address'],
            'value': request.form['amount']}
    transaction = Transaction(data)
    response = {
        'transaction': transaction.to_dict(), 'signature': transaction.sign_transaction()
    }
    return jsonify(response), 200
