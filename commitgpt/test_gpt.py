import pytest
from commitgpt.gpt import GPT

@pytest.fixture
def gpt_instance():
    return GPT()

def test_api_key(gpt_instance):
    api_key = "my_api_key"
    gpt_instance.api_key(api_key)
    assert gpt_instance.llm.openai_api_key == api_key

if __name__ == "__main__":
    pytest.main()
