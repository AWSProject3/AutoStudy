import boto3

from interface.prompt_template_fetcher import PromptTemplateFetcher
from core.config import env_vars

REGION = env_vars.REGION
AWS_ACCESS_KEY=env_vars.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=env_vars.AWS_SECRET_ACCESS_KEY

class S3PromptTemplateFetcher(PromptTemplateFetcher):    
    def __init__(self, bucket_name: str):
        self.s3_client = boto3.client(
            's3',
            region_name=REGION, 
            aws_access_key_id=AWS_ACCESS_KEY, 
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        self.bucket_name = bucket_name

    def get_prompt_template(self, template_name: str) -> str:
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=template_name)
            content = response['Body'].read().decode('utf-8')
            return content
        except Exception as e:
            print(f"Error getting object from S3: {e}")
            return ""
        
