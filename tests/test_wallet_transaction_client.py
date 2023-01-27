import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.models import WalletTransaction
from lago_python_client.clients.base_client import LagoApiError


def wallet_transaction_object():
    return WalletTransaction(
        wallet_id='123',
        paid_credits='10',
        granted_credits='10'
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/wallet_transaction.json')

    with open(data_path, 'r') as wallet_transaction_response:
        return wallet_transaction_response.read()


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/wallet_transaction_index.json')

    with open(data_path, 'r') as wallet_transaction_index_response:
        return wallet_transaction_index_response.read()


class TestWalletTransactionClient(unittest.TestCase):
    def test_valid_create_wallet_transaction_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/wallet_transactions', text=mock_response())
            response = client.wallet_transactions().create(wallet_transaction_object())

        self.assertEqual(response['wallet_transactions'][0].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac1111')
        self.assertEqual(response['wallet_transactions'][1].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac1222')

    def test_invalid_create_wallet_transaction_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/wallet_transactions', status_code=401, text='')

            with self.assertRaises(LagoApiError):
                client.wallet_transactions().create(wallet_transaction_object())

    def test_valid_find_all_groups_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri(
                'GET',
                'https://api.getlago.com/api/v1/wallets/555/wallet_transactions',
                text=mock_collection_response()
            )
            response = client.wallet_transactions().find_all('555')

        self.assertEqual(response['wallet_transactions'][0].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac1111')
        self.assertEqual(response['meta']['current_page'], 1)


if __name__ == '__main__':
    unittest.main()
