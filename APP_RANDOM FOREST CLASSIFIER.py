from flask import Flask, request, jsonify
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import re
import base58
import hashlib
import bech32
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn import svm
import pickle

# Load the pickle model
model = pickle.load(open("model_Random.pkl", "rb"))
vectorizer=pickle.load(open("vectorizer_Random.pkl", "rb"))


app = Flask(__name__)

# Initialize the CountVectorizer

def is_valid_legacy_or_p2sh_address(address):
    try:
        decoded = base58.b58decode(address)
        payload, checksum = decoded[:-4], decoded[-4:]
        hash1 = hashlib.sha256(payload).digest()
        hash2 = hashlib.sha256(hash1).digest()
        return checksum == hash2[:4]
    except Exception as e:
        return False

def is_valid_bech32_address(address):
    try:
        hrp, data = bech32.bech32_decode(address)
        if hrp != 'bc' and hrp != 'tb':
            return True
        if data is None:
            return False
        return True
    except Exception as e:
        return False
'''
def is_valid_eth_address(address):
    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return False
    if address != address.lower() and address != address.upper():
        return check_eth_checksum(address)
    return True

def check_eth_checksum(address):
    address = address.replace('0x', '')
    address_hash = hashlib.sha3_256(address.lower().encode('utf-8')).hexdigest()
    for i in range(40):
        if (address_hash[i] >= '8' and address[i].upper() != address[i]) or (address_hash[i] < '8' and address[i].lower() != address[i]):
            return False
    return True
'''

def is_valid_eth_address(address):
    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return False
    return True

def validate_tron_address(address):
    if len(address) == 34:
        return True
    return False

def extract_features(address):
    features = {
        'length': len(address),
        'character_set': set(address),
        'prefix': address[:2],
        'is_valid': False,
        'type': 'unknown'
    }

    if address.startswith(('1', '3', 'bc1')):
        features['type'] = 'Bitcoin'
        if address.startswith('1') or address.startswith('3'):
            features['is_valid'] = is_valid_legacy_or_p2sh_address(address)
        elif address.startswith('bc1'):
            features['is_valid'] = is_valid_bech32_address(address)
    elif address.startswith('0x'):
        features['type'] = 'Ethereum'
        features['is_valid'] = is_valid_eth_address(address)
    elif validate_tron_address(address):
        features['type'] = 'TRON'
        features['is_valid'] = True

    return features

def validate_and_extract_address_features(address):
    features = extract_features(address)
    return features


    # Get JSON data from request
@app.route("/Cryptocurrency", methods=["POST"])
def predict_address():
    # Get JSON data from request
    json_data = request.get_json()

    # Extract address from JSON data
    address = json_data.get("address")
    print(address)
    print(type(address))
    print("HELLO")
    # vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 5))
    Z = vectorizer.transform([address])
   
    # Validate and extract features
    
    print("Hi")
    address_features = validate_and_extract_address_features(address)
    if(address_features['is_valid']==True):
        print("Hi")
        result=model.predict(Z)
        if(result==[1]):
            address_features['result']="ETH"
            print("ETH HELLO")
            if(address.startswith('0x')):
                return jsonify({"Prediction" : "ETH"})
            else:
                return jsonify({"Prediction" : "Can't Detected"})
        elif(result==[0]):
            address_features['result']="BTC"
            print("BTC HELLO")
            if(address.startswith(('1', '3', 'bc1'))):
                return jsonify({"Prediction" : "BTC" })
            else:
                return jsonify({"Prediction" : "Cant't Detected"})
        elif(result==[2]):
            address_features['result']="TRX"
            print("TRX HELLO")
            return jsonify({"Prediction" : "TRX" })
        # return jsonify({"address": address, "address_features": address_features})
    else:
        return jsonify({"error": "Invalid JSON format. Expected 'address' key."}), 400

if __name__ == "__main__":
    app.run(debug=True)