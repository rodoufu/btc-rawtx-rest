import requests


def get_unspent_outputs(address: str, confirmations: int = 6, limit: int = 250):
	req = requests.get(f"https://blockchain.info/unspent?active={address}&limit={limit}&confirmations={confirmations}")
	return req.json()['unspent_outputs']
