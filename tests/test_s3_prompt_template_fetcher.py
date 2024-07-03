import os

import unittest
from unittest.mock import MagicMock, patch

from interface.impl.S3PromptTemplateFetcher import S3PromptTemplateFetcher



class TestS3PromptTemplateFetcher(unittest.TestCase):

    @patch('boto3.client')
    def setUp(self, mock_aws_client):

        # env setting
        os.environ["AWS_ACCESS_KEY"] = "test"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
        os.environ["REGION"] = "us-east-1"

        # mock s3 client
        self.mock_s3_client = MagicMock()
        mock_aws_client.return_value = self.mock_s3_client

        # template data setting
        self.bucket_name = "test-bucket"
        self.template_name = "test-template.txt"
        self.template_content = "This is a test template."

        # create S3PromptTemplateFetcher object
        self.fetcher = S3PromptTemplateFetcher(bucket_name=self.bucket_name)

    # success
    def test_get_prompt_template(self):
        # create get_object method to mock_s3_client
        self.mock_s3_client.get_object.return_value = {
            'Body': MagicMock(read=MagicMock(return_value=self.template_content.encode('utf-8')))
        }

        # test get_prompt_template method 
        content = self.fetcher.get_prompt_template(self.template_name)
        self.assertEqual(content, self.template_content)

        # test s3 get_object call
        self.mock_s3_client.get_object.assert_called_once_with(Bucket=self.bucket_name, Key=self.template_name)

    #fail
    def test_get_prompt_template_not_found(self):
        # mock_s3_client get_object method setting -> exception
        self.mock_s3_client.get_object.side_effect = Exception("boto3-client-error")

        # test get_prompt_template method
        content = self.fetcher.get_prompt_template("non-existent-template.txt")
        self.assertEqual(content, "", "Expected empty string for non-existent template")

        # test get_object call
        self.mock_s3_client.get_object.assert_called_once_with(Bucket=self.bucket_name, Key="non-existent-template.txt")

if __name__ == '__main__':
    unittest.main()
