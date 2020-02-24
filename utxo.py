import requests

from data import TransactionOutputItem


class Utxo(object):
	"""
	Encapsulates the API logic to get the blockchain information.
	This way if we need to add use another provider we only need to implement a subclass with the logic.
	"""

	@staticmethod
	def get_unspent_outputs(address: str, confirmations: int = 6, limit: int = 250) -> list:
		"""
		Get unspent outputs for the address.
		:param address: The address to look for.
		:param confirmations: Minimum number of confirmations.
		:param limit: Maximum of outputs to return.
		:return: The unspent outputs.
		"""
		url = f"https://blockchain.info/unspent?active={address}&limit={limit}&confirmations={confirmations}"
		# I'm not worrying about using async methods cause, from what I've understood that's not the main point here.
		unspent = requests.get(url)

		return [
			{
				"output": f"{o['tx_hash_big_endian']}:{o['tx_output_n']}",
				"value": o['value'],
				'script': o['script']
			}
			for o in unspent.json()['unspent_outputs']
		]

	@staticmethod
	def to_tx_output_item(utxo: dict) -> TransactionOutputItem:
		"""
		Generates a TransactionOutputItem from the UTXO information.
		:param utxo: The UTXO.
		:return: TransactionOutputItem.
		"""
		txid, vout = utxo['output'].split(':')
		return TransactionOutputItem(txid, vout, utxo['script'], utxo['value'])
