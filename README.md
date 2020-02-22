# btc-rawtx-rest

Rest webservice to create raw transactions selecting UTXO

## Endpoints

### Create transaction

This endpoint will be used to create a raw transaction that spends from a P2PKH address and that supports
paying to mulitple addresses (either P2PKH or P2SH). The endpoint should return a transaction that
spends from the source address and that pays to the output addresse

- URL: /payment_transactions
- Method: POST
- Request body (dictionary):
    - source_address (string): The address to spend from
    - outputs (dictionary): A dictionary that maps addresses to amounts (in SAT)
    - fee_kb (int): The fee per kb in SAT
- Response body (dictionary):
    - raw (string): The unsigned raw transaction
    - inputs (array of dicts): The inputs used
    - txid (string): The transaction id
    - vout (int): The output number
    - script_pub_key (string): The script pub key
    - amount (int): The amount in SAT

## Assumptions

- A public service should be used to retrieve unspent transaction ouputs (For example
https://blockchain.info/unspent?active=address).
- Any UTXO selecting logic will work as long as the transaction is valid.
- Its ok to use any library as long as you implement the code to select the utxos and estimate the
transaction size.