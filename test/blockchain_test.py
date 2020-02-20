import unittest
import blockchain
from data import TransactionOutputItem


class TestBlockchain(unittest.TestCase):
	def test_get_unspent_outputs(self):
		# unspent = blockchain.get_unspent_outputs("1MUz4VMYui5qY1mxUiG8BQ1Luv6tqkvaiL")
		unspent = blockchain.get_unspent_outputs("1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr")
		self.assertIsNotNone(unspent)
		self.assertTrue(len(unspent) > 0)
		print(f"unspent({len(unspent)}): {unspent}")
		for utxo in unspent:
			print(f"utxo: {utxo}")

	def test_select_utxo(self):
		unspent = [TransactionOutputItem("oi10", 0, "s10", 10), TransactionOutputItem("oi20", 1, "s20", 20)]
		selected, _ = blockchain.select_utxo(unspent, 12)
		self.assertEqual(len(selected), 1)
		self.assertEqual(selected[0].amount, 20)

		unspent = [
			TransactionOutputItem("oi10", 0, "s10", 10), TransactionOutputItem("oi20", 1, "s20", 20),
			TransactionOutputItem("oi30", 0, "s30", 30)
		]
		selected, _ = blockchain.select_utxo(unspent, 35)
		self.assertEqual(len(selected), 2)
		self.assertEqual(selected[0].amount, 30)
		self.assertEqual(selected[1].amount, 20)

	def test_calculate_fee(self):
		self.assertEqual(blockchain.calculate_fee("2a" * 2024, 1), 2)
		self.assertEqual(blockchain.calculate_fee("2a" * 2024, 2), 4)
		self.assertEqual(blockchain.calculate_fee("2a" * 2024, 0), 0)
		self.assertEqual(blockchain.calculate_fee("2a" * 2624, 1), 3)

	def test_create_transaction(self):
		self.assertEqual(blockchain.create_transaction(), "oi")


if __name__ == '__main__':
	unittest.main()
