import re
import json

from interface.impl.S3PromptTemplateFetcher import S3PromptTemplateFetcher

def build_prompt(replacements: dict, template: str) -> json:

    # get prompt template to S3
    prompt_template_fetcher = S3PromptTemplateFetcher(bucket_name="autostudy-prompt")
    prompt_template = prompt_template_fetcher.get_prompt_template(template)

    pattern = r'\{\{(\w+)\}\}'  # {{ }} 패턴 정규 표현식
    prompt = re.sub(pattern, lambda x: replacements.get(x.group(1), x.group()), prompt_template)

    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1500,
        "temperature": 0.8,
        "top_p": 0.5,
        "top_k": 50,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    return request

