import unittest
import blockchain
from select_utxo import BiggerFirst, SmallerFirst


class TestSelectUtxo(unittest.TestCase):
	def __init__(self, method_name: str = ...):
		super().__init__(method_name)
		self.unspent_10_20 = [{'output': 'oi10:0', 'value': 10}, {'output': 'oi20:1', 'value': 20}]
		self.unspent_10_20_30 = [
			{'output': 'oi10:0', 'value': 10}, {'output': 'oi20:1', 'value': 20},
			{'output': 'oi30:0', 'value': 30}
		]

	def test_bigger_first(self):
		selector = BiggerFirst()
		unspent = self.unspent_10_20
		selected, _ = selector.select(unspent, 12)
		self.assertEqual(len(selected), 1)
		self.assertEqual(selected[0]['value'], 20)

		unspent = self.unspent_10_20_30
		selected, _ = selector.select(unspent, 35)
		self.assertEqual(len(selected), 2)
		self.assertEqual(selected[0]['value'], 30)
		self.assertEqual(selected[1]['value'], 20)

	def test_smaller_first(self):
		selector = SmallerFirst()
		unspent = self.unspent_10_20
		selected, _ = selector.select(unspent, 12)
		self.assertEqual(len(selected), 2)
		self.assertEqual(selected[0]['value'], 10)
		self.assertEqual(selected[1]['value'], 20)

		unspent = self.unspent_10_20_30
		selected, _ = selector.select(unspent, 35)
		self.assertEqual(len(selected), 3)
		self.assertEqual(selected[0]['value'], 10)
		self.assertEqual(selected[1]['value'], 20)
		self.assertEqual(selected[2]['value'], 30)