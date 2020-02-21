import unittest
import blockchain
from data import TransactionInput


class TestBlockchain(unittest.TestCase):
	def test_get_unspent_outputs(self):
		# unspent = blockchain.get_unspent_outputs("1MUz4VMYui5qY1mxUiG8BQ1Luv6tqkvaiL")
		unspent = blockchain.get_unspent_outputs("1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr")
		self.assertIsNotNone(unspent)
		self.assertTrue(len(unspent) > 0)
		print(f"unspent({len(unspent)}): {unspent}")
		for utxo in unspent:
			print(f"utxo: {utxo}")

	def test_calculate_fee(self):
		self.assertEqual(blockchain.estimate_fee(len("2a" * 2024), 1), 2)
		self.assertEqual(blockchain.estimate_fee(len("2a" * 2024), 2), 4)
		self.assertEqual(blockchain.estimate_fee(len("2a" * 2024), 0), 0)
		self.assertEqual(blockchain.estimate_fee(len("2a" * 2624), 1), 3)

	def test_create_transaction(self):
		inputs = [
			{'output': '3be10a0aaff108766371fd4f4efeabc5b848c61d4aac60db6001464879f07508:0', 'value': 180000000},
			{'output': '51ce9804e1a4fd3067416eb5052b9930fed7fdd9857067b47d935d69f41faa38:0', 'value': 90000000}
		]
		outs = {
			'2N8hwP1WmJrFF5QWABn38y63uYLhnJYJYTF': 269845600,
			'mrvHv6ggk5gFMatuJtBKAzktTU1N3MYdu2': 100000
		}
		raw_tx, _ = blockchain.create_transaction(inputs, outs)
		raw_tx_resp = "\
01000000020875f07948460160db60ac4a1dc648b8c5abfe4e4ffd71637608f\
1af0a0ae13b000000008b483045022100afab8c54817ef534d6134fe8796f09\
2d8b5ae479a3e7b8409b657ede443ea0f102206231206ae2ebb322db8c48f6f\
89b1f75205c309edc5aed47f572398f28b988ed0141041f763d81010db8ba30\
26fef4ac3dc1ad7ccc2543148041c61a29e883ee4499dc724ab2737afd66e4a\
acdc0e4f48550cd783c1a73edb3dbd0750e1bd0cb03764fffffffff38aa1ff4\
695d937db4677085d9fdd7fe30992b05b56e416730fda4e10498ce510000000\
08a473044022003dca553f79a391a56550d124e4a60a5bd03f4780ccd00a5d2\
a4ad49c57d933602201e7e04de6f8f6ffeb0fd14476918537a57f67548105b7\
d611c15c95d04e4fe2f0141041f763d81010db8ba3026fef4ac3dc1ad7ccc25\
43148041c61a29e883ee4499dc724ab2737afd66e4aacdc0e4f48550cd783c1\
a73edb3dbd0750e1bd0cb03764fffffffff02608415100000000017a914a997\
4100aeee974a20cda9a2f545704a0ab54fdc87a08601000000000017a9147d1\
3547544ecc1f28eda0c0766ef4eb214de10458700000000"
		self.assertEqual(raw_tx, raw_tx_resp)

	def test_select_utxo_and_create_transaction_wrong_source(self):
		transaction_input = TransactionInput('1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cA2', {}, 0)
		transaction_output, err = blockchain.select_utxo_and_create_tx(transaction_input)
		self.assertIsNone(transaction_output)
		self.assertEqual(err, "There was a problem trying to get unspent outputs")

	def test_select_utxo_and_create_transaction_wrong_output(self):
		transaction_input = TransactionInput(
			'1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr', {'1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cA2': 2}, 0
		)
		transaction_output, err = blockchain.select_utxo_and_create_tx(transaction_input)
		self.assertIsNone(transaction_output)
		self.assertEqual(err, "There was a problem trying to create the transaction")


if __name__ == '__main__':
	unittest.main()
