import unittest
import payment


class TestPayment(unittest.TestCase):
	def test_create(self):
		transaction = {
			"source_address": "1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr",
			"outputs": {"1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cA2": 1},
			"fee_kb": 0
		}
		created_transaction, http_code = payment.create(transaction)
		self.assertEqual(http_code, 201)
		self.assertIsNotNone(created_transaction['raw'])
		self.assertIsNotNone(created_transaction['inputs'])
		for inp in created_transaction['inputs']:
			self.assertIsNotNone(inp['txid'])
			self.assertIsNotNone(inp['vout'])
			self.assertIsNotNone(inp['script_pub_key'])
			self.assertIsNotNone(inp['amount'])


if __name__ == '__main__':
	unittest.main()
