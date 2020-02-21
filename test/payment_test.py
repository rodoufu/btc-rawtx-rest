import unittest
from werkzeug.exceptions import BadRequest, InternalServerError

import payment


class TestPayment(unittest.TestCase):
	def test_create_empty_source_address(self):
		transaction = {
			"source_address": "",
			"outputs": {"1CK6KHY6MHgYvmRQ4PAafKYDrg1ejbH1cE": 1},
			"fee_kb": int(10 * 1e3)
		}
		self.assertRaises(BadRequest, payment.create, transaction)

		transaction = {
			"outputs": {"1CK6KHY6MHgYvmRQ4PAafKYDrg1ejbH1cE": 1},
			"fee_kb": int(10 * 1e3)
		}
		self.assertRaises(BadRequest, payment.create, transaction)

		transaction = {
			"source_address": None,
			"outputs": {"1CK6KHY6MHgYvmRQ4PAafKYDrg1ejbH1cE": 1},
			"fee_kb": int(10 * 1e3)
		}
		self.assertRaises(BadRequest, payment.create, transaction)

	def test_create_empty_output(self):
		transaction = {
			"source_address": "1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr",
			"outputs": {},
			"fee_kb": int(10 * 1e3)
		}
		self.assertRaises(BadRequest, payment.create, transaction)

		transaction = {
			"source_address": "1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr",
			"fee_kb": int(10 * 1e3)
		}
		self.assertRaises(BadRequest, payment.create, transaction)

		transaction = {
			"source_address": "1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr",
			"outputs": None,
			"fee_kb": int(10 * 1e3)
		}
		self.assertRaises(BadRequest, payment.create, transaction)

	def test_create_empty_fee_kb(self):
		transaction = {
			"source_address": "1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr",
			"outputs": {"1CK6KHY6MHgYvmRQ4PAafKYDrg1ejbH1cE": 1},
		}
		self.assertRaises(BadRequest, payment.create, transaction)

		transaction = {
			"source_address": "1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr",
			"outputs": {"1CK6KHY6MHgYvmRQ4PAafKYDrg1ejbH1cE": 1},
			"fee_kb": None
		}
		self.assertRaises(BadRequest, payment.create, transaction)

	def test_create(self):
		transaction = {
			"source_address": "1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr",
			"outputs": {"1CK6KHY6MHgYvmRQ4PAafKYDrg1ejbH1cE": 1},
			"fee_kb": int(10 * 1e3)
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

	def test_create_not_enough_funds(self):
		transaction = {
			"source_address": "1DAXdwNNd4KEhZfGJYanYaVVaUz1XY2cAr",
			"outputs": {"1CK6KHY6MHgYvmRQ4PAafKYDrg1ejbH1cE": int(1e8)},
			"fee_kb": int(10 * 1e3)
		}
		self.assertRaises(InternalServerError, payment.create, transaction)


if __name__ == '__main__':
	unittest.main()
