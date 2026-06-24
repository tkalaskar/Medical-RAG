from typing import Any, List, Mapping, Optional

from huggingface_hub import InferenceClient
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import HUGGINGFACE_REPO_ID, HF_TOKEN

logger = get_logger(__name__)


class HuggingFaceChatCompletionLLM(LLM):
    """Expose Hugging Face chat completion models through LangChain's LLM API."""

    client: Any
    repo_id: str
    max_new_tokens: int = 256
    temperature: float = 0.3

    @property
    def _llm_type(self) -> str:
        return "huggingface_chat_completion"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {
            "repo_id": self.repo_id,
            "max_new_tokens": self.max_new_tokens,
            "temperature": self.temperature,
        }

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        response = self.client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get("max_new_tokens", self.max_new_tokens),
            temperature=kwargs.get("temperature", self.temperature),
            stop=stop,
        )

        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("Hugging Face returned an empty response.")

        return content


def load_llm(
    huggingface_repo_id: Optional[str] = None,
    hf_token: Optional[str] = None,
) -> HuggingFaceChatCompletionLLM:
    repo_id = huggingface_repo_id or HUGGINGFACE_REPO_ID
    token = hf_token or HF_TOKEN

    try:
        if not token:
            raise RuntimeError(
                "HF_TOKEN or HUGGINGFACEHUB_API_TOKEN is not configured."
            )

        logger.info(
            "Loading Hugging Face chat-completion model: %s",
            repo_id,
        )
        llm = HuggingFaceChatCompletionLLM(
            client=InferenceClient(
                model=repo_id,
                token=token,
                timeout=120,
            ),
            repo_id=repo_id,
            max_new_tokens=256,
            temperature=0.3,
        )
        logger.info("LLM client initialized successfully.")
        return llm

    except Exception as e:
        error_message = CustomException.get_detailed_error_message(
            f"Failed to load Hugging Face model: {repo_id}",
            e,
        )
        logger.error(str(error_message))
        raise CustomException("Failed to load LLM", e) from e
