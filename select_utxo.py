class SelectUtxo(object):
	"""
	Generic class for selecting UTXO before creating a transaction.
	Given a list of transactions and a value, use some criteria to choose the UTXO.
	"""
	def select(self, unspent: list, value: int) -> (list, int):
		raise NotImplementedError("Implement select")


class BiggerFirst(SelectUtxo):
	"""
	Select the bigger UTXO first.
	"""

	def __init__(self):
		self.should_sort = True
		self.reverse = True

	def select(self, unspent: list, value: int) -> (list, int):
		unspent = sorted(unspent, key=lambda k: k['value'], reverse=self.reverse) if self.should_sort else unspent
		total = 0
		resp = []
		for utxo in unspent:
			if total > value:
				break
			resp += [utxo]
			total += utxo['value']
		return resp, total


class SmallerFirst(BiggerFirst):
	"""
	Select the smaller UTXO first.
	"""

	def __init__(self):
		super().__init__()
		self.reverse = False


class FirstFit(BiggerFirst):
	"""
	Select the first elements until it fulfills the transaction.
	"""

	def __init__(self):
		super().__init__()
		self.should_sort = False


class BestFit(SelectUtxo):
	"""
	Knapsack problem inspired version.
	"""

	def select(self, unspent: list, value: int) -> (list, int):
		bag = dict()

		total = 0
		resp = []
		for utxo in unspent:
			bag_keys = list(bag.keys())
			for bagk in bag_keys:
				new_value = bagk + utxo['value']
				if new_value not in bag or len(bag[new_value]) > len(bag[bagk]):
					bag[new_value] = bag[bagk] + [utxo]
			# It's going to override when it's possible to find it using only one UTXO
			bag[utxo['value']] = [utxo]

		# Only the cases where the value found is bigger thant the value required for the outputs are filtered
		keys = sorted([v for v in bag.keys() if v > value])

		# Select the option that selects less inputs
		used = len(unspent)
		for k in keys:
			v = bag[k]
			if len(v) < used:
				used = len(v)
				resp = v
				total = sum([x['value'] for x in resp])

		return resp, total
