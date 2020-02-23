import os
from cryptos import Bitcoin, sha256, serialize
from data import TransactionInput, TransactionOutput, TransactionOutputItem, SelectedInfo
from select_utxo import BiggerFirst, FirstFit, BestFit, SmallerFirst, SelectUtxo
from utxo import Utxo

min_for_change = int(os.environ['MIN_CHANGE']) if 'MIN_CHANGE' in os.environ else 5430
bitcoin_is_testnet = bool(os.environ['BITCOIN_TESTNET']) if 'BITCOIN_TESTNET' in os.environ else False


def select_utxo_and_create_tx(transaction_input: TransactionInput) -> (TransactionOutput, str):
	"""
	Selects the UTXO and creates the transaction.
	It also estimates the fees and add the change, when it is necessary.
	:param transaction_input: Service input.
	:return: Service output or error message.
	"""
	try:
		unspent = Utxo.get_unspent_outputs(transaction_input.source_address)
	except Exception as e:
		# It should be logging using the default log
		print(f"There was a problem trying to get unspent outputs: {e}")
		return None, "There was a problem trying to get unspent outputs"

	total_unspent = sum([u['value'] for u in unspent])

	best_selected = SelectedInfo(total_unspent, "", list(unspent), dict(transaction_input.outputs))
	# It checks which selector gives the best results in terms of lower fees
	for selector in [BiggerFirst(), SmallerFirst(), FirstFit(), BestFit()]:
		outputs = dict(transaction_input.outputs)
		total_outputs = sum([u for u in outputs.values()])

		selected, err = create_transaction_with_change(
			selector, outputs, total_outputs, unspent, total_unspent,
			transaction_input.source_address, transaction_input.fee_kb)

		if err is not None:
			return None, err

		# Case it's found a smaller fee or less UTXO are used or less no change is necessary
		best_selected = min(best_selected, selected)

	if len(best_selected.selected) == 0:
		return None, "It was unable the select the UTXO for creating the transaction"

	resp = TransactionOutput(best_selected.raw, [])
	for utxo in best_selected.selected:
		resp.inputs += [Utxo.to_tx_output_item(utxo)]

	return resp, None


def create_transaction_with_change(
		selector: SelectUtxo, outputs: dict, total_outputs: int, unspent: list, total_unspent: int,
		source_address: str, fee_kb: int) -> (SelectedInfo, str):
	"""
	Create a transaction adding the change if necessary.
	:param selector: The selector used to choose the UTXO.
	:param outputs: The outputs for the transaction.
	:param total_outputs: Sum of the values for the outputs.
	:param unspent: The UTXO used for the transaction.
	:param total_unspent: Sum of the values from the UTXO.
	:param source_address: The source address.
	:param fee_kb: The fee by kb.
	:return: The transaction, the selected UTXO and the used fee.
	"""
	# Selecting UTXO without fee just to estimate the transaction size
	selected_utxo, _ = selector.select(unspent, total_outputs)
	estimated_size = guess_transaction_size(selected_utxo, outputs)
	estimated_fee = estimate_fee(estimated_size, fee_kb)

	if total_unspent < total_outputs + estimated_fee:
		return None, "The output cannot be greater than the input"

	selected_utxo, total_selected = selector.select(unspent, total_outputs + estimated_fee)
	# Create transaction and calculate the fee
	(raw_transaction, estimated_size), err = create_transaction(selected_utxo, outputs)
	if err is not None:
		return None, err
	estimated_fee = estimate_fee(estimated_size, fee_kb)

	outputs, change = create_change(
		outputs, total_selected, source_address, total_outputs, estimated_fee
	)
	total_outputs += change
	# If a change was added then it needs to create the transaction again
	if change != 0:
		(raw_transaction, _), err = create_transaction(selected_utxo, outputs)
		if err is not None:
			return None, err

	fee_value = total_selected - total_outputs
	return SelectedInfo(fee_value, raw_transaction, selected_utxo, outputs), None


def estimate_fee(estimated_size: int, fee_kb: int) -> int:
	"""
	Calculate fee based in the transaction size and the price per KiB.
	:param estimated_size: Estimated size for the transaction.
	:param fee_kb: Price of the transaction by KiB.
	:return: The estimated fee.
	"""
	return int(estimated_size * fee_kb / 1024.0 + 0.5)


def create_change(outputs: dict, total_selected: int, address: str, total_outputs: int, fees: int) -> (dict, int):
	"""
	Identify the change and create if necessary.
	Change the outputs adding the change.
	:param outputs: Dict with the outputs.
	:param total_selected: Sum of the selected UTXO.
	:param address: Address to add the change.
	:param total_outputs: Total to send in the transaction.
	:param fees: Value for fees.
	:return: The outputs and value of the change.
	"""
	change = total_selected - total_outputs - fees
	if change > min_for_change:
		outputs = dict(outputs)
		if address not in outputs:
			outputs[address] = 0
		outputs[address] += change
		return outputs, change
	return outputs, 0


def create_transaction(inputs: list, outputs: dict) -> ((str, int), str):
	"""
	Create a Bitcoin transaction.
	It uses a simple wallet to sign the transaction and estimates the size of the final transaction.
	:param inputs: Inputs for the transaction.
	:param outputs: Outputs for the transaction.
	:return: The serialized not signed transaction and the estimated size in bytes.
	"""
	try:
		c = Bitcoin(testnet=bitcoin_is_testnet)
		outs = []
		for outk, outv in outputs.items():
			outs += [{'value': outv, 'address': outk}]
		tx = c.mktx(inputs, outs)
		tx_serialize = serialize(tx)

		# Signing each input to predict the transaction size
		priv = sha256('a big long brainwallet password')
		tx_signed = tx.copy()
		for i in range(len(inputs)):
			tx_signed = c.sign(tx_signed, i, priv)

		# The serialization uses one char per nibble so in order the get the number of bytes it's necessary to
		# divide the size of the string serialization by 2
		return (str(tx_serialize), len(str(serialize(tx_signed))) // 2), None
	except Exception as e:
		# It should be logging using the default log
		print(f"There was a problem trying to create the transaction: {e}")
		return (None, None), "There was a problem trying to create the transaction"


def guess_transaction_size(inputs: list, outputs: dict) -> (str, int):
	"""
	Guess the transaction size based in the number of inputs and outputs.
	https://en.bitcoin.it/wiki/Protocol_documentation#tx
	Usually the transaction is composed of:
	- 180 bytes for each "pay to address" input;
	- 34 bytes (32 + maybe 2 more bytes) for each output;
	- 11 fixed bytes (10 + maybe 1 more).
	:param inputs: List of inputs.
	:param outputs: List of outputs.
	:return: A guess for the expected size of the transaction in bytes.
	"""
	return 11 + 180 * len(inputs) + 34 * len(outputs)
