import os
import json

import boto3
from botocore.exceptions import ClientError

from core.config import env_vars

AWS_ACCESS_KEY=env_vars.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=env_vars.AWS_SECRET_ACCESS_KEY
REGION=env_vars.REGION

class GenerativeAI:
    def __init__(self):
        self.client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION,
        )

    def invoke_model(self, prompt):
        try:
            response = self.client.invoke_model(
                body=prompt,
                modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0" 
                # modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
            )

            # Decode the response body.
            model_response = json.loads(response["body"].read().decode('utf-8'))
            print("!!!!!!!!!!!!!!!!!!!!!")
            print(model_response)
            
            # Extract and print the response text.
            response_text = model_response["content"][0]["text"]
            clean_text = fr"{response_text}"
            response = json.loads(clean_text)


            return response
        
        except ClientError as e:
            print(f"Error invoking model: {e}")
            return None
        
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        

