import json
import unittest
from unittest.mock import MagicMock, patch
import re

from domains.prompt_builder import build_prompt
from interface.impl.S3PromptTemplateFetcher import S3PromptTemplateFetcher

class TestBuildPrompt(unittest.TestCase):

    @patch.object(S3PromptTemplateFetcher, 'get_prompt_template')
    def test_build_prompt(self, mock_get_prompt_template):
        # Mock S3PromptTemplateFetcher의 get_prompt_template 메서드 설정
        mock_template = "{{source_language}} to {{target_language}} in {{difficulty}}"
        mock_get_prompt_template.return_value = mock_template

        # replacements setting
        replacements = {
            "source_language": "test",
            "target_language": "test",
            "difficulty": "test",
        }

        # call build_prompt
        request = build_prompt(replacements)

        # test request type JSON
        try:
            json.loads(request)
        except ValueError:
            self.fail("반환 값이 JSON 형식이 아닙니다.")

        # test pattern
        self.assertNotRegex(request, r'\{\{(\w+)\}\}', "반환 값에 아직 대체되지 않은 패턴이 있습니다.")

        # request에서 실제 값이 올바르게 대체되었는지 확인
        self.assertIn("test to test in test", request, "반환 값이 예상한 값과 다릅니다.")

if __name__ == "__main__":
    unittest.main()
