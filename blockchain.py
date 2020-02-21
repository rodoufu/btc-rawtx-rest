import os
from cryptos import Bitcoin, sha256, serialize
from data import TransactionInput, TransactionOutput, TransactionOutputItem
from select_utxo import BiggerFirst

min_for_change = int(os.environ['MIN_CHANGE']) if 'MIN_CHANGE' in os.environ else 5430
bitcoin_is_testnet = bool(os.environ['BITCOIN_TESTNET']) if 'BITCOIN_TESTNET' in os.environ else False


def get_unspent_outputs(address: str) -> list:
	c = Bitcoin(testnet=bitcoin_is_testnet)
	# I'm not worrying about using async methods cause, from what I've understood that's not the main point here.
	return c.unspent(address)


def select_utxo_and_create_tx(transaction_input: TransactionInput) -> (TransactionOutput, str):
	unspent = get_unspent_outputs(transaction_input.source_address)
	total_unspent = sum([u['value'] for u in unspent])
	total_outputs = sum([u for u in transaction_input.outputs.values()])

	if total_unspent < total_outputs:
		return None, "The output cannot be greater than the input"

	# TODO Change it to a interface so we can select between implementations
	selector = BiggerFirst()
	selected_utxo, total_selected = selector.select(unspent, total_outputs)

	while True:
		raw_transaction, estimated_size = create_transaction(selected_utxo, transaction_input.outputs)
		resp = TransactionOutput(raw_transaction, [])

		change = create_change(
			transaction_input.outputs, total_selected, transaction_input.source_address, total_outputs,
			calculate_fee(estimated_size, transaction_input.fee_kb)
		)
		if change == 0:
			break
		total_outputs += change

	for utxo in selected_utxo:
		txid, vout = utxo['output'].split(':')
		# TODO Check the txid and the script_pub_key
		resp.inputs += [TransactionOutputItem(txid, vout, "utxo.script_pub_key", utxo['value'])]

	return resp, None


def calculate_fee(estimated_size: int, fee_kb: int) -> int:
	return int(estimated_size / 2 * fee_kb / 1024 + 0.5)


def create_change(outputs: dict, total_selected: int, address: str, total_outputs: int, fees: int):
	change = total_selected - total_outputs - fees
	if change > min_for_change:
		if address not in outputs:
			outputs[address] = 0
		outputs[address] += change
		return change
	return 0


def create_transaction(inputs: list, outputs: dict) -> (str, int):
	c = Bitcoin(testnet=bitcoin_is_testnet)
	priv = sha256('a big long brainwallet password')
	# inputs = [
	# 	{'output': '3be10a0aaff108766371fd4f4efeabc5b848c61d4aac60db6001464879f07508:0', 'value': 180000000},
	# 	{'output': '51ce9804e1a4fd3067416eb5052b9930fed7fdd9857067b47d935d69f41faa38:0', 'value': 90000000}
	# ]
	# outs = [
	# 	{'value': 269845600, 'address': '2N8hwP1WmJrFF5QWABn38y63uYLhnJYJYTF'},
	# 	{'value': 100000, 'address': 'mrvHv6ggk5gFMatuJtBKAzktTU1N3MYdu2'}
	# ]
	outs = []
	for outk, outv in outputs.items():
		outs += [{'value': outv, 'address': outk}]
	tx = c.mktx(inputs, outs)
	tx2 = c.sign(tx, 0, priv)
	return str(serialize(tx)), len(str(serialize(tx2)))
