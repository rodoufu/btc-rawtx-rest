import unittest
from data import TransactionInput, TransactionOutput, TransactionOutputItem


class TestData(unittest.TestCase):
	def test_transaction_input_str(self):
		self.assertEqual(str(TransactionInput("oi", {}, 1)), '{"source_address": "oi", "outputs": {}, "fee_kb": 1}')

	def test_transaction_output_str(self):
		self.assertEqual(str(TransactionOutput("oi", [])), '{"raw": "oi", "inputs": []}')

	def test_transaction_output_item_str(self):
		self.assertEqual(
			str(TransactionOutputItem("oi", 1, "oi2", 1)),
			'{"txid": "oi", "vout": 1, "script_pub_key": "oi2", "amount": 1}'
		)


if __name__ == '__main__':
	unittest.main()
