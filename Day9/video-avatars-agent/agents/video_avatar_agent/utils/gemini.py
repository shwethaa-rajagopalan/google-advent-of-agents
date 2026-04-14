import os
from google.adk.models.google_llm import Gemini

def get_proxied_gemini_model(
    model_name: str,
    base_url: str
) -> Gemini:
    model = Gemini(model=model_name)
    api_client = model.api_client._api_client
    api_client.api_key = os.environ.get("GEMINI_API_KEY", None)
    if api_client.api_key:
        api_client.vertexai = False
        api_client.project = None
        api_client.location = None
    api_client._http_options.base_url = base_url
    return model

