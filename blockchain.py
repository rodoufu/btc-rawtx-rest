import os
from cryptos import Bitcoin, sha256, serialize
from data import TransactionInput, TransactionOutput, TransactionOutputItem
from select_utxo import BiggerFirst, FirstFit, BestFit, SmallerFirst

min_for_change = int(os.environ['MIN_CHANGE']) if 'MIN_CHANGE' in os.environ else 5430
bitcoin_is_testnet = bool(os.environ['BITCOIN_TESTNET']) if 'BITCOIN_TESTNET' in os.environ else False


def get_unspent_outputs(address: str) -> list:
	"""
	Get unspent outputs for the address.
	:param address: The address to look for.
	:return: The unspent outputs.
	"""
	c = Bitcoin(testnet=bitcoin_is_testnet)
	# I'm not worrying about using async methods cause, from what I've understood that's not the main point here.
	return c.unspent(address)


def select_utxo_and_create_tx(transaction_input: TransactionInput) -> (TransactionOutput, str):
	"""
	Selects the UTXO and creates the transaction.
	It also estimates the fees and add the change, when it is necessary.
	:param transaction_input: Service input.
	:return: Service output or error message.
	"""
	try:
		unspent = get_unspent_outputs(transaction_input.source_address)
	except Exception as e:
		print(f"There was a problem trying to get unspent outputs: {e}")
		return None, "There was a problem trying to get unspent outputs"

	total_unspent = sum([u['value'] for u in unspent])

	fee_value = total_unspent
	best_resp = None
	num_selected = len(unspent)
	num_outputs = len(transaction_input.outputs)
	for selector in [BiggerFirst(), SmallerFirst(), FirstFit(), BestFit()]:
		outputs = dict(transaction_input.outputs)
		total_outputs = sum([u for u in outputs.values()])

		if total_unspent < total_outputs:
			return None, "The output cannot be greater than the input"

		selected_utxo, total_selected = selector.select(unspent, total_outputs)
		if len(selected_utxo) == 0:
			selected_utxo, total_selected = selector.select(unspent, total_outputs)

		while True:
			try:
				raw_transaction, estimated_size = create_transaction(selected_utxo, outputs)
			except Exception as e:
				print(f"There was a problem trying to create the transaction: {e}")
				return None, "There was a problem trying to create the transaction"

			resp = TransactionOutput(raw_transaction, [])

			outputs, change = create_change(
				outputs, total_selected, transaction_input.source_address, total_outputs,
				estimate_fee(estimated_size, transaction_input.fee_kb)
			)
			if change == 0:
				break
			total_outputs += change

		# Case it's find a smaller fee or less UTXO are used or less no change is necessary
		if total_selected - total_outputs < fee_value or\
					len(selected_utxo) < num_selected or\
					len(outputs) < num_outputs:
			print(f"Using selector: {selector.__class__.__name__}")
			fee_value = total_selected - total_outputs
			best_resp = resp
			num_selected = len(selected_utxo)
			num_outputs = len(outputs)
	resp = best_resp

	for utxo in selected_utxo:
		txid, vout = utxo['output'].split(':')
		# TODO Check the txid and the script_pub_key
		resp.inputs += [TransactionOutputItem(txid, vout, "utxo.script_pub_key", utxo['value'])]

	return resp, None


def estimate_fee(estimated_size: int, fee_kb: int) -> int:
	"""
	Calculate fee based in the transaction size and the price per KiB.
	:param estimated_size: Estimated size for the transaction.
	:param fee_kb: Price of the transaction by KiB.
	:return: The estimated fee.
	"""
	return int(estimated_size / 2 * fee_kb / 1024 + 0.5)


def create_change(outputs: dict, total_selected: int, address: str, total_outputs: int, fees: int) -> (dict, int):
	"""
	Identify the change and create if if necessary.
	Change the outputs adding the change.
	:param outputs: Dict with the outputs.
	:param total_selected: Sum of the selected UTXO.
	:param address: Address to add the change.
	:param total_outputs: Total to send in the transaction.
	:param fees: Value for fees.
	:return: The value of the change.
	"""
	change = total_selected - total_outputs - fees
	if change > min_for_change:
		outputs = dict(outputs)
		if address not in outputs:
			outputs[address] = 0
		outputs[address] += change
		return outputs, change
	return outputs, 0


def create_transaction(inputs: list, outputs: dict) -> (str, int):
	"""
	Create a Bitcoin transaction.
	It uses a simple wallet to sign the transaction and estimate the size of the final transaction.
	:param inputs: Inputs for the transaction.
	:param outputs: Outputs for the transaction.
	:return: The serialized not signed transaction and the estimated size.
	"""
	c = Bitcoin(testnet=bitcoin_is_testnet)
	outs = []
	for outk, outv in outputs.items():
		outs += [{'value': outv, 'address': outk}]
	tx = c.mktx(inputs, outs)
	priv = sha256('a big long brainwallet password')
	tx2 = c.sign(tx, 0, priv)
	return str(serialize(tx)), len(str(serialize(tx2)))
