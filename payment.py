from blockchain import select_utxo_and_create_tx
from data import TransactionInput
from flask import abort


def create(transaction: dict) -> (dict, int):
	"""
	This function creates a new transaction.
	:param transaction: The information for the transaction.
	:return: 201 on success, 400 if an error occurs.
	"""
	for dict_attrib in ['source_address', 'outputs']:
		if dict_attrib not in transaction or transaction[dict_attrib] is None or len(transaction[dict_attrib]) == 0:
			msg = f"The {dict_attrib} cannot be empty"
			# It should be logging using the default log
			print(msg)
			abort(400, msg)
	if 'fee_kb' not in transaction or transaction['fee_kb'] is None:
		msg = "The fee per kb cannot be empty"
		# It should be logging using the default log
		print(msg)
		abort(400, msg)
	transaction_input = TransactionInput(transaction['source_address'], transaction['outputs'], transaction['fee_kb'])

	resp, err = select_utxo_and_create_tx(transaction_input)
	if err:
		abort(500, err)

	# Converting the response
	for i in range(len(resp.inputs)):
		resp.inputs[i] = resp.inputs[i].__dict__
	resp = resp.__dict__

	return resp, 201
