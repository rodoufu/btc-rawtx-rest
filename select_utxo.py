class SelectUtxo(object):
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
	Select the first elements that can fulfill the transaction.
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
			for bagk in bag.keys():
				bag[bagk + utxo['value']] += [utxo]
			# It's going to override when it's possible to find it using only one UTXO
			bag[utxo['value']] = [utxo]
		keys = sorted([v for v in bag.keys() if v > value])

		return resp, total