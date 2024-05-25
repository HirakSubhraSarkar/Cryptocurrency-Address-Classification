
# Cryptocurrency Address Classification

Objective: The objective of this internship assignment is to develop a machine learning model that can accurately classify cryptocurrency
addresses into different types, such as BTC (Bitcoin), ETH (Ethereum), TRX (Tron).


## Demo

Insert gif or link to demo


## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## API Reference

#### I Use 3 APIs
##### 1st for BTC (Bitcoin)

```http
  'https://blockchain.info/block/{block_hash}?format=json'

```

##### 2nd for ETH (Ethereum)
```http
  'https://api.etherscan.io/api?module=account&action=txlist&address=0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe&startblock=0&endblock=99999999&sort=asc&apikey=Your_api_key'
```


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Your_api_key` | `string` | **Required**. Your API key |

##### 3rd for TRX (Tron)
```http
  ''https://api.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=100&start=0&apikey=Your_api_key'
```


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Your_api_key` | `string` | **Required**. Your API key |


## Deployment

To deploy this project run

```bash
  pip install bech32 base58
```
```bash
pip install streamlit
```
```bash
!npm install localtunnel
```
#### For app.py
```bash
!streamlit run app.py &>/content/logs.txt & npx localtunnel --port 8501 & ipv4.icanhazip.com
```

#### For app2.py
```bash
!streamlit run app2.py &>/content/logs.txt & npx localtunnel --port 8501 & ipv4.icanhazip.com!streamlit run app2.py &>/content/logs.txt & npx localtunnel --port 8501 & ipv4.icanhazip.com
```
## Documentation

[Documentation](https://linktodocumentation)

