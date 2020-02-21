import os
from cryptos import Bitcoin, sha256, serialize
from data import TransactionInput, TransactionOutput, TransactionOutputItem
from select_utxo import BiggerFirst

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
	# TODO Add try / catch
	unspent = get_unspent_outputs(transaction_input.source_address)
	total_unspent = sum([u['value'] for u in unspent])
	total_outputs = sum([u for u in transaction_input.outputs.values()])

	if total_unspent < total_outputs:
		return None, "The output cannot be greater than the input"

	# TODO Change it to a interface so we can select between implementations
	selector = BiggerFirst()
	selected_utxo, total_selected = selector.select(unspent, total_outputs)

	while True:
		# TODO Add try / catch
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
	"""
	Calculate fee based in the transaction size and the price per KiB.
	:param estimated_size: Estimated size for the transaction.
	:param fee_kb: Price of the transaction by KiB.
	:return: The estimated fee.
	"""
	return int(estimated_size / 2 * fee_kb / 1024 + 0.5)


def create_change(outputs: dict, total_selected: int, address: str, total_outputs: int, fees: int):
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
		if address not in outputs:
			outputs[address] = 0
		outputs[address] += change
		return change
	return 0


def create_transaction(inputs: list, outputs: dict) -> (str, int):
	"""
	Create a Bitcoin transaction.
	It uses a simple wallet to sign the transaction and estimate the size of the final transaction.
	:param inputs: Inputs for the transaction.
	:param outputs: Outputs for the transaction.
	:return: The serialized not signed transaction and the estimated size.
	"""
	c = Bitcoin(testnet=bitcoin_is_testnet)
	priv = sha256('a big long brainwallet password')
	outs = []
	for outk, outv in outputs.items():
		outs += [{'value': outv, 'address': outk}]
	tx = c.mktx(inputs, outs)
	tx2 = c.sign(tx, 0, priv)
	return str(serialize(tx)), len(str(serialize(tx2)))
