# -*- coding: utf-8 -*-
import datetime  # DateTime
import hashlib  # To Cryptoghraphy
import json
from urllib import response
from flask import Flask, jsonify
from numpy import block  # To Handle http Request in Postman
import sqlite3


# Create Database And Connect
db = sqlite3.connect(
    r"C:\Users\khatib\Desktop\BlockchainsA-Z\BlockChainCode\1- CreateBlockChain\BlockChain.db")
# Setting Up The Cursor
cr = db.cursor()


# 1-  building a BlockChain
class Blockchain:
    def __init__(self):
        # self.chain = []                                 # chain contains blocks
        # if statment if records in db null create Genisis block
        records = cr.execute("select * from records")
        if (records is None):
            self.create_block(proof=1, pervious_hash='0')  # Genisis Block


# function To Create Block and Add To Chian Array


    def create_block(self, proof, pervious_hash):

        # get last BlockNumber in db
        records = "SELECT BlockNumber FROM records ORDER BY BlockNumber DESC LIMIT 1"
    # Assumes conn is a database connection.
        cursor = cr
        cursor.execute(records)
        rows = [x for x in cursor]
        cols = [x[0] for x in cursor.description]
        Blocks = []
        for row in rows:
            Block = {}
            for prop, val in zip(cols, row):
                Block[prop] = val
            Blocks.append(Block)
    # Create a string representation of your array of songs.
        BlocksJSON = Blocks

    # printing original list
        print("The original list is : " + str(BlocksJSON))

# Using list comprehension
# Get values of particular key in list of dictionaries
        result = [sub['BlockNumber'] for sub in BlocksJSON]

# printing result
        print("The values corresponding to key : " + str(result))
        BlockNumber = int(result[0])  # accessing the zeroth element
        print(BlockNumber)

        block = {
            # To Get Length Chain To Add New Block
            'index':          BlockNumber + 1,
            # DateTime Create Block
            'timestamp':     str(datetime.datetime.now()),
            # Get Hash Pervious Block
            'pervious_hash': pervious_hash,
            # Get From Mining function
            'proof':         proof,

        }
    # Add Block To Chain
        # self.chain.append(block)
        # insert the new Blocks in db
        cr.execute(
            f"""INSERT INTO records (BlockNumber , timestamp2 , pervious_hash , proof) VALUES ('{block['index']}', '{block['timestamp']}', '{block['pervious_hash']}', '{block['proof']}');"""
        )
        db.commit()
        return block


# function To get pervious block in Chain Array

    def get_pervious_block(self):

        # get last BlockNumber in db
        records = "SELECT * FROM records ORDER BY BlockNumber DESC LIMIT 1"
        # Assumes conn is a database connection.
        cursor = cr
        cursor.execute(records)
        rows = [x for x in cursor]
        cols = [x[0] for x in cursor.description]
        Blocks = []
        for row in rows:
            Block = {}
            for prop, val in zip(cols, row):
                Block[prop] = val
            Blocks.append(Block)
    # Create a string representation of your array of songs.
        BlocksJSON = Blocks

        print(BlocksJSON)
        return BlocksJSON


# # function To get current block in Chain Array
#     def get_current_block(self):
#         for idx, val in enumerate(self.chain):
#             print(idx, val)

# function to proof of work
# Pervious Prood // is an element of the problem that miners will need to control to find the new proof
# this will check is that the proof of the proof of each block is valid according to our proof of work problem that we defines in this proof of work function


    def proof_of_work(self, pervious_proof):
        new_proof = 1  # to solve the problem we need to increment variable by one each iteration of while loop until we get the right proof
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - pervious_proof**2).encode()).hexdigest()    # **2 To more Complex
            # .encode  b'5'  Without '5'
            if hash_operation[:4] == '0000':  # [:4] git first 4 numbers
                check_proof = True  # miners wins
            else:
                new_proof += 1  # Still increment until codition true

        return new_proof    # return the new proof and block was mined
        #

# Hash Blocks function
# this function take a block as input and going to return sha256 cryptographic hash
# in json library  Domp func // to make dictinory with four key in Block(index, pervoius_hash .. ) as A string
# json.dumps() // takes object and return as string
# sort_key // its aparameter in dumps if true they Will Sort blocks
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

# this function will checks if the chain is valid
# it iterate on each of blocks of the chain and make two checks for each of these blocks.
# the first check // the pervious hash is equal to the hash of the pervious block
# the second check // check th proof of work is valid

    def is_valid_chain(self, chain):
        pervious_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['pervious_hash'] != self.hash(pervious_block):
                return False
            pervious_proof = pervious_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - pervious_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            pervious_block = block
            block_index += 1
        return True


# 2-  Mining our BlockChain
# Mine Block function will simply get the proof of work that we will need to solve
# Create A Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# Creating a Blockchain
blockchain = Blockchain()
# 2-  Mining our BlockChain


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_pervious_block()
# printing original list
    print("The original list is : " + str(previous_block))
# Using list comprehension
# Get values of particular key in list of dictionaries
    result = [sub['proof'] for sub in previous_block]
# printing result
    print("The values corresponding to key : " + str(result))
    proof = int(result[0])  # accessing the zeroth element
    print(proof)

    previous_proof = proof
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'Congratulations, you just mined a block!',
                'BlockNumber': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'pervious_hash': block['pervious_hash'],

                }
    return jsonify(response), 200

# Getting the Full BlockChain


@app.route('/get_chain', methods=['GET'])
def getchain():

    # Assumes conn is a database connection.
    qry = "Select BlockNumber, timestamp2, pervious_hash, proof From records Order By BlockNumber"

    # Assumes conn is a database connection.
    cursor = cr
    cursor.execute(qry)
    rows = [x for x in cursor]
    cols = [x[0] for x in cursor.description]
    Blocks = []
    for row in rows:
        Block = {}
        for prop, val in zip(cols, row):
            Block[prop] = val
        Blocks.append(Block)
    # Create a string representation of your array of songs.
    BlocksJSON = Blocks

    response = {
        'chain': BlocksJSON,
        'length': len(BlocksJSON)
    }
    return jsonify(response), 200
# Check if blockchain is valid or not


@app.route('/is_blockchain_valid', methods=['GET'])
def is_blockchain_valid():
    is_blockchain_valid = blockchain.is_valid_chain(blockchain.chain)
    if is_blockchain_valid:
        response = {'message ': 'The Block Chain Is Valid'}
    else:
        response = {'message ': 'The Block Chain Is Not Valid'}
    return jsonify(response), 200


# Running The Web App
app.run(host='0.0.0.0', port=5000)
