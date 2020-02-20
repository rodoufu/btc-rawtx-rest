import requests

from data import TransactionInput, TransactionOutput, TransactionOutputItem


def get_unspent_outputs(address: str, confirmations: int = 6, limit: int = 250) -> list:
	url = f"https://blockchain.info/unspent?active={address}&limit={limit}&confirmations={confirmations}"
	unspent = requests.get(url)

	return [
		TransactionOutputItem(u['tx_hash'], u['tx_output_n'], u['script'], u['value'])
		for u in unspent.json()['unspent_outputs']
	]


def select_utxo_and_create_tx(transaction_input: TransactionInput) -> (TransactionOutput, str):
	unspent = get_unspent_outputs(transaction_input.source_address)
	total_unspent = sum([u.amount for u in unspent])
	total_outputs = sum([u for u in transaction_input.outputs.values()])

	if total_unspent < total_outputs:
		return None, "The output cannot be greater than the input"

	resp = TransactionOutput("1564sx", [])
	for utxo in unspent:
		resp.inputs += [TransactionOutputItem(utxo.txid, utxo.vout, utxo.script_pub_key, utxo.amount)]

	return resp, None
