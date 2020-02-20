import unittest
import blockchain


class TestGetUnspentOutputs(unittest.TestCase):
	def test_dummy(self):
		# unspent = blockchain.get_unspent_outputs("1MUz4VMYui5qY1mxUiG8BQ1Luv6tqkvaiL")
		unspent = blockchain.get_unspent_outputs("1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr")
		self.assertIsNotNone(unspent)
		self.assertTrue(len(unspent) > 0)
		print(f"unspent({len(unspent)}): {unspent}")
		for utxo in unspent:
			print(f"utxo: {utxo}")

	# def test_isupper(self):
	#     self.assertTrue('FOO'.isupper())
	#     self.assertFalse('Foo'.isupper())
	#
	# def test_split(self):
	#     s = 'hello world'
	#     self.assertEqual(s.split(), ['hello', 'world'])
	#     # check that s.split fails when the separator is not a string
	#     with self.assertRaises(TypeError):
	#         s.split(2)


if __name__ == '__main__':
	unittest.main()
