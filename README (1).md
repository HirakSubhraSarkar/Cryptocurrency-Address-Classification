
# Cryptocurrency Address Classification

Objective: The objective of this internship assignment is to develop a machine learning model that can accurately classify cryptocurrency
addresses into different types, such as BTC (Bitcoin), ETH (Ethereum), TRX (Tron).


## Demo

https://github.com/HirakSubhraSarkar/Cryptocurrency-Address-Classification/assets/159253204/0b0bd180-e890-4e49-9191-6bee92a10a1f


## Screenshots


![RFC](https://github.com/HirakSubhraSarkar/Cryptocurrency-Address-Classification/assets/159253204/af67e380-ad79-4ab2-bd74-b1fcbafbc108)


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

To deploy this project

```bash
  pip install bech32 base58
```
```bash
pip install flask
```
In Postman(POST METHOD) 
```bash
localhost:5000/Cryptocurrency
```
## Documentation

[Documentation](https://linktodocumentation)

