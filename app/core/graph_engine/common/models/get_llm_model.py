from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from configuration.configs import settings


def get_llm_model(
        model_name: str = settings.LLM_MODEL
) -> ChatOpenAI | ChatGoogleGenerativeAI:
    if model_name == "gpt-4o":
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            request_timeout=settings.LLM_SERVICE_TIMEOUT,
            api_key=settings.OPENAI_API_KEY
        )

    if model_name == "gemini-2.0-flash":
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            api_key=settings.GEMINI_API_KEY,
            max_output_tokens=2000000
        )
