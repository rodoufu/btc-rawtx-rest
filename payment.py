from flask import abort


def create(transaction):
	"""
	This function creates a new person in the people structure
	based on the passed in person data
	:param transaction:  person to create in people structure
	:return:        201 on success, 406 on person exists
	"""

	print(
		f"source: {transaction['source_address']}, outputs: {transaction['outputs']}, fee_kb: {transaction['fee_kb']}")

	return \
		{
			"raw": "1564sx",
			"inputs": [
				{
					"txid": "a",
					"vout": 1,
					"script_pub_key": "apub",
					"amount": 1
				},
				{
					"txid": "ab",
					"vout": 12,
					"script_pub_key": "apub2",
					"amount": 2
				}
			]
		}, 201
# abort(406, f"Person with the last name {lname} already exists")
