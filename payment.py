from blockchain import select_utxo_and_create_tx
from data import TransactionInput
from flask import abort


def create(transaction: dict) -> (dict, int):
	"""
	This function creates a new transaction.
	:param transaction: The information for the transaction.
	:return: 201 on success, 400 if an error occurs.
	"""

	if 'source_address' not in transaction or \
		transaction['source_address'] is None or len(transaction['source_address']) == 0:
		abort(400, "The source address cannot be empty")
	if 'outputs' not in transaction or transaction['outputs'] is None or \
		len(transaction['outputs']) == 0:
		abort(400, "The outputs cannot be empty")
	if 'fee_kb' not in transaction or transaction['fee_kb'] is None:
		abort(400, "The fee per kb cannot be empty")

	transaction_input = TransactionInput(transaction['source_address'], transaction['outputs'], transaction['fee_kb'])

	resp, err = select_utxo_and_create_tx(transaction_input)

	if err:
		abort(500, err)

	for i in range(len(resp.inputs)):
		resp.inputs[i] = resp.inputs[i].__dict__
	resp = resp.__dict__

	return resp, 201
