import re
import json

from interface.impl.s3_prompt_template_fetcher import S3PromptTemplateFetcher
from core.config import env_vars

BUCKET_NAME = env_vars.BUCKET_NAME

def build_prompt(replacements: dict, template: str, recent_categories: list) -> json:

    # get prompt template to S3
    prompt_template_fetcher = S3PromptTemplateFetcher(bucket_name=BUCKET_NAME)
    prompt_template = prompt_template_fetcher.get_prompt_template(template)

    pattern = r'\{\{(\w+)\}\}'  # {{ }} 패턴 정규 표현식
    prompt = re.sub(pattern, lambda x: replacements.get(x.group(1), x.group()), prompt_template)

    # if recent_categories exist -> add prompt
    if recent_categories:
        # bytes를 str로 변환하고 리스트가 비어있지 않은 경우에만 처리
        str_categories = [cat.decode('utf-8') if isinstance(cat, bytes) else cat for cat in recent_categories]
        if str_categories:
            if len(str_categories) == 1:
                categories_str = str_categories[0]
            else:
                categories_str = ", ".join(str_categories)
            prompt += f"\nPlease create problems excluding [{categories_str}]"

    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1500,
        "temperature": 0.8,
        "top_p": 0.8,
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

