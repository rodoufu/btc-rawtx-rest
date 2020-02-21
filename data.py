import json


class TransactionInput(object):
	"""
	Transaction input for the service.
	"""
	def __init__(self, source_address: str, outputs: dict, fee_kb: int):
		self.source_address = source_address
		self.outputs = outputs
		self.fee_kb = fee_kb

	def __str__(self):
		return json.dumps(self, default=lambda o: o.__dict__)

	def __json__(self):
		return self.__dict__


class TransactionOutputItem(object):
	"""
	Item in the transaction output.
	"""
	def __init__(self, txid: str, vout: int, script_pub_key: str, amount: int):
		self.txid = txid
		self.vout = vout
		self.script_pub_key = script_pub_key
		self.amount = amount

	def __str__(self):
		return json.dumps(self, default=lambda o: o.__dict__)

	def __json__(self):
		return self.__dict__

	def __lt__(self, other):
		return self.amount < other.amount


class TransactionOutput(object):
	"""
	Transaction output for the service.
	"""
	def __init__(self, raw: str, inputs: list):
		self.raw = raw
		self.inputs = inputs

	def __str__(self):
		return json.dumps(self, default=lambda o: o.__dict__)

	def __json__(self):
		return self.__dict__
