import os
from commitgpt.prompts import COMMIT_PROMPT
from typing import Optional
from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter


class GPT:
    """
    GPT class to interact with openai.
    """

    SUMMARY_FILE = "summarize.txt"
    MAX_GPT_TOKENS = 2048

    def __init__(
        self, api_key: Optional[str] = "", temp_loc: Optional[str] = ""
    ) -> None:
        """
        GPT class to interact with openai.

        Args:
            `api_key` (str): openai api key

            `temp_loc` (str): temporary location to store files

        Returns:
            `None`
        """

        if api_key == "":
            api_key = os.environ.get("OPENAI_API_KEY", "dummy")
        self.temp_loc = temp_loc
        self.llm = ChatOpenAI(
            openai_api_key=api_key,
        )
        # Either `map_reduce` or `refine` depending output accuracy.
        self.chain = load_summarize_chain(
            llm=self.llm, chain_type="map_reduce", verbose=False
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.MAX_GPT_TOKENS,
            chunk_overlap=0,
        )

    def api_key(self, api_key: str) -> None:
        """
        `api_key` sets the openai api key.

        Args:
            `api_key` (str): openai api key

        Returns:
            `None`
        """

        self.llm.openai_api_key = api_key

    def summarise(self, text: str) -> str:
        """
        `summarise` summarises the git diff.

        Args:
            `text` (str): Long input text to summarise.

        Returns:
            `summary` (str): summary of the input text
        """

        file_path = self.temp_loc + self.SUMMARY_FILE

        with open(file_path, "w") as f:
            f.write(text)

        loader = UnstructuredFileLoader(file_path)
        doc = loader.load()
        split_docs = self.text_splitter.split_documents(doc)
        summary = self.chain.run(split_docs)

        return str(summary)

    def generate_message(
        self, git_dif: str, role: str, guidelines: str
    ) -> str:
        """
        `generate_message` generates a commit message
        based on the provided Git diff.

        Args:
            `git_dif` (str): git diff

            `role` (str): role

            `guidelines` (str): guidelines

        Returns:
            `commit message` (str): commit message
        """

        if len(git_dif) > self.MAX_GPT_TOKENS:
            git_dif = self.summarise(git_dif)

        prompt = COMMIT_PROMPT.replace(
            "{professional_role}", role).replace(
                "{commit_guidelines}", guidelines).replace(
                    "{git_diff}", git_dif)

        response = self.llm.predict(text=prompt)

        return str(response)
