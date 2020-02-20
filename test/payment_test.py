import unittest
import payment


class TestCreate(unittest.TestCase):
	def test_dummy(self):
		transaction = {
			'source_address': "1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr",
			'outputs': {'1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cA2': 1},
			'fee_kb': 0
		}
		created_transaction = payment.create(transaction)
		self.assertIsNotNone(created_transaction['raw'])
		self.assertIsNotNone(created_transaction['inputs'])
		for inp in created_transaction['inputs']:
			self.assertIsNotNone(inp['txid'])
			self.assertIsNotNone(inp['vout'])
			self.assertIsNotNone(inp['script_pub_key'])
			self.assertIsNotNone(inp['amount'])

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
