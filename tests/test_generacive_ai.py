import os
import json
import unittest
from unittest.mock import MagicMock, patch

from botocore.exceptions import ClientError

from domains.generative_ai import GenerativeAI


class TestGenerativeAI(unittest.TestCase):

    @patch('boto3.client')
    def setUp(self, mock_boto_client):
        
        # env setting
        os.environ["AWS_ACCESS_KEY"] = "test"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
        os.environ["REGION"] = "us-east-1"

        # mock bedrock runtime
        self.mock_bedrock_runtime = MagicMock()
        mock_boto_client.return_value = self.mock_bedrock_runtime

        # create GenerativeAI
        self.generative_ai = GenerativeAI()

    # success
    def test_invoke_model_success(self):
        # mock response
        mock_response_body = json.dumps({
            "content": [{"text": '{"result": "test response"}'}]
        }).encode('utf-8')
        self.mock_bedrock_runtime.invoke_model.return_value = {
            "body": MagicMock(read=MagicMock(return_value=mock_response_body))
        }

        # test prompt
        prompt = "Test prompt"

        # call invoke_model
        response = self.generative_ai.invoke_model(prompt)

        # expected result
        expected_response = {"result": "test response"}

        # test
        self.assertEqual(response, expected_response)

    # fail (bedrock runtime error)
    def test_invoke_model_client_error(self):
        # mock bedrock_runtime error response
        self.mock_bedrock_runtime.invoke_model.side_effect = ClientError(
            error_response={'Error': {'Code': '400', 'Message': 'Bad Request'}},
            operation_name='invoke_model'
        )

        # test
        prompt = "Test prompt"
        response = self.generative_ai.invoke_model(prompt)
        self.assertIsNone(response)

    # fail (json decode error)
    def test_invoke_model_json_decode_error(self):
        # mock invaild json error response
        mock_response_body = b'Invalid JSON'
        self.mock_bedrock_runtime.invoke_model.return_value = {
            "body": MagicMock(read=MagicMock(return_value=mock_response_body))
        }

        # test
        prompt = "Test prompt"
        response = self.generative_ai.invoke_model(prompt)
        self.assertIsNone(response)

    # fail (unexpected)
    def test_invoke_model_unexpected_error(self):
        # mock unexpected error response
        self.mock_bedrock_runtime.invoke_model.side_effect = Exception("Unexpected error")

        # test
        prompt = "Test prompt"
        response = self.generative_ai.invoke_model(prompt)
        self.assertIsNone(response)

if __name__ == "__main__":
    unittest.main()
