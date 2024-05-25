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
import streamlit as st

import requests
import pandas as pd

st.title('Cryptocurrency Address Classification')

# Function to get Bitcoin addresses
@st.cache_data
def get_btc_addresses(limit=1250):
    btc_addresses = set()
    url = 'https://blockchain.info/latestblock'
    response = requests.get(url)
    latest_block = response.json()
    block_hash = latest_block['hash']

    while len(btc_addresses) < limit:
        block_url = f'https://blockchain.info/block/{block_hash}?format=json'
        response = requests.get(block_url)
        block_data = response.json()

        for tx in block_data['tx']:
            for out in tx['out']:
                if 'addr' in out:
                    btc_addresses.add(out['addr'])
                    if len(btc_addresses) >= limit:
                        break
            if len(btc_addresses) >= limit:
                break
        block_hash = block_data['prev_block']

    return list(btc_addresses)[:limit]

# Function to get Ethereum addresses
@st.cache_data
def get_eth_addresses(limit=1250):
    eth_addresses = set()
    url = 'https://api.etherscan.io/api?module=account&action=txlist&address=0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe&startblock=0&endblock=99999999&sort=asc&apikey=E1TRQRSFP237WHQG11I344FTW6WH1XG4WE'
    response = requests.get(url)
    transactions = response.json()['result']

    for tx in transactions:
        eth_addresses.add(tx['from'])
        eth_addresses.add(tx['to'])
        if len(eth_addresses) >= limit:
            break

    return list(eth_addresses)[:limit]

# Function to get TRON addresses
@st.cache_data
def get_trx_addresses(limit=1250):
    trx_addresses = set()
    url = 'https://api.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=100&start=0&apikey=7c31c3b5-939f-4d58-a66b-5e54bb970efd'
    response = requests.get(url)
    transactions = response.json()['data']

    for tx in transactions:
        trx_addresses.add(tx['ownerAddress'])
        trx_addresses.add(tx['toAddress'])
        if len(trx_addresses) >= limit:
            break

    return list(trx_addresses)[:limit]



# Main function to gather addresses and save to DataFrame
@st.cache_data
def create_crypto_address_dataset():
    btc_addresses = get_btc_addresses()
    eth_addresses = get_eth_addresses()
    trx_addresses = get_trx_addresses()
   

    data = {
        'address': btc_addresses + eth_addresses + trx_addresses,
        'type': ['BTC'] * len(btc_addresses) + ['ETH'] * len(eth_addresses) + ['TRX'] * len(trx_addresses)
    }

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = create_crypto_address_dataset()

    
    st.write(df)



import re
import base58
import hashlib
import bech32
import pandas as pd

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
            return False
        if data is None:
            return False
        return True
    except Exception as e:
        return False

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



# Add checksum validation feature
df['checksum_validation'] = df['address'].apply(lambda x: extract_features(x)['is_valid'])

# Display the updated DataFrame
st.write("After checksum validation")
st.write(df)


# Convert addresses into numerical features
vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 5))  # Example with character n-grams
X = vectorizer.fit_transform(df['address'],df['checksum_validation'])

# Encode target labels
label_encoder = LabelEncoder()
Y = label_encoder.fit_transform(df['type'])

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


model = RandomForestClassifier(n_estimators=100, criterion='entropy',random_state=42)
model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)

print(classification_report(Y_test, Y_pred))

accuracy = accuracy_score(Y_test, Y_pred)
print(f'Accuracy: {accuracy}')

import re
import base58
import hashlib
import bech32

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
            return False
        if data is None:
            return False
        return True
    except Exception as e:
        return False

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

# Get user input
#user_address = input("Please enter a cryptocurrency address: ")

# Validate and extract features


# Print the validation result
#print("Address is", "valid" if address_features['is_valid'] else "invalid")


add=st.text_input("Enter the address: ")
Z = vectorizer.transform([add])
result=model.predict(Z)
#print(result)

address_features = validate_and_extract_address_features(add)
if(address_features['is_valid']==True):
  if(result==[1]):
    st.write("ETH")
  elif(result==[0]):
    st.write("BTC")
  elif(result==[2]):
    st.write("TRX")
else:
  st.write("Invalid Address")
