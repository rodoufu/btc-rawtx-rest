from blockchain import select_utxo_and_create_tx
from data import TransactionInput
from flask import abort


def create(transaction: dict) -> (dict, int):
	"""
	This function creates a new transaction.
	:param transaction: The information for the transaction.
	:return: 201 on success, 400 if an error occurs.
	"""
	transaction_input = TransactionInput(transaction['source_address'], transaction['outputs'], transaction['fee_kb'])

	if len(transaction_input.source_address) == 0:
		abort(400, "The source address cannot be empty")
	if len(transaction_input.outputs) == 0:
		abort(400, "The outputs cannot be empty")

	resp, err = select_utxo_and_create_tx(transaction_input)

	if err:
		abort(500, err)

	for i in range(len(resp.inputs)):
		resp.inputs[i] = resp.inputs[i].__dict__
	resp = resp.__dict__

	return resp, 201
