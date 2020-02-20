import requests
import os

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

	# TODO Change it to a interface so we can select between implementations
	selected_utxo, total_selected = select_utxo(unspent, total_outputs)

	# TODO Create the transaction
	resp = TransactionOutput("1564sx", [])

	create_change(
		transaction_input.outputs, total_selected, transaction_input.source_address, total_outputs,
		calculate_fee(resp.raw, transaction_input.fee_kb)
	)

	for utxo in selected_utxo:
		resp.inputs += [TransactionOutputItem(utxo.txid, utxo.vout, utxo.script_pub_key, utxo.amount)]

	return resp, None


def select_utxo(unspent: list, value: int) -> (list, int):
	unspent = sorted(unspent, reverse=True)
	total = 0
	resp = []
	for utxo in unspent:
		if total > value:
			break
		resp += [utxo]
		total += utxo.amount
	return resp, total


def calculate_fee(raw: str, fee_kb: int) -> int:
	return int(len(raw) / 2 * fee_kb / 1024 + 0.5)


def create_change(outputs: dict, total_selected: int, address: str, total_outputs: int, fees: int):
	# This could be moved to a configuration object to be loaded once
	min_for_change = int(os.environ['MIN_CHANGE']) if 'MIN_CHANGE' in os.environ else 5430

	change = total_selected - total_outputs - fees
	if change > min_for_change:
		if address not in outputs:
			outputs[address] = 0
		outputs[address] += change
		return change
	return 0
