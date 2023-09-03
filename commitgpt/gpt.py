import openai
from .prompts import COMMIT_PROMPT
from typing import Optional


class GPT:
    def __init__(self, api_key: Optional[str] = "") -> None:
        """init.
        Set the openai api key.

        Args:
            api_key (str): openai api key

        Returns:
            None
        """
        openai.api_key = api_key
        self.model = "gpt-3.5-turbo-0613"
        self.temperature = 0.3
        self.max_tokens = 256
        self.n = 1
        self.stop = None

    def api_key(self, api_key: str) -> None:
        """api_key sets the openai api key.

        Args:
            api_key (str): openai api key

        Returns:
            None
        """
        openai.api_key = api_key

    def generate_message(
        self, git_dif: str, role: str, guidelines: str
    ) -> str:
        """generate_message generates a commit message
        based on the provided Git diff.

        Args:
            git_dif (str): git diff
            role (str): role
            guidelines (str): guidelines

        Returns:
            str: commit message
        """

        prompt = COMMIT_PROMPT.replace(
            "{git_diff}", git_dif).replace(
            "{commit_guidelines}", guidelines)

        reponse = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
        )

        return reponse['choices'][0]['message']['content']
