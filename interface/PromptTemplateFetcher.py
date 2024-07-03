from abc import ABC, abstractmethod


class PromptTemplateFetcher(ABC):
    
    @abstractmethod
    def get_prompt_template(self, template_identifier: str) -> str:
        pass

