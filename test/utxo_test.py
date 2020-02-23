import unittest
from utxo import Utxo


class TestUtxo(unittest.TestCase):
	def test_get_unspent_outputs(self):
		unspent = Utxo.get_unspent_outputs("1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr")
		self.assertIsNotNone(unspent)
		self.assertTrue(len(unspent) > 0)

		unspent = Utxo.get_unspent_outputs("1MUz4VMYui5qY1mxUiG8BQ1Luv6tqkvaiL")
		self.assertIsNotNone(unspent)
		self.assertTrue(len(unspent) > 0)

	def test_to_tx_output_item(self):
		utxo_dict = {
			'output': '3be10a0aaff108766371fd4f4efeabc5b848c61d4aac60db6001464879f07508:0',
			'script': 'batata',
			'value': 180000000
		}
		utxo = Utxo.to_tx_output_item(utxo_dict)
		utxo_dict_tx, utxo_dict_vout = utxo_dict['output'].split(':')
		self.assertEqual(utxo.amount, utxo_dict['value'])
		self.assertEqual(utxo.txid, utxo_dict_tx)
		self.assertEqual(utxo.vout, utxo_dict_vout)


if __name__ == '__main__':
	unittest.main()
