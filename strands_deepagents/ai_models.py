"""
Default model configuration for Strands DeepAgents.
"""



from strands.models import BedrockModel
from botocore.config import Config

boto_config = Config(
    retries={"max_attempts": 3, "mode": "standard"}, connect_timeout=600, read_timeout=900
)


def get_default_model() -> BedrockModel:
    """
    Get the default model identifier for DeepAgents.
    
    Returns:
        Model identifier string for Claude Sonnet 4
    """
    return BedrockModel(
        model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
        additional_request_fields={
            "anthropic_beta": ["interleaved-thinking-2025-05-14"],
            "thinking": {"type": "enabled", "budget_tokens": 8000},
        },
        boto_client_config=boto_config,
    )


def basic_claude_haiku_4_5() -> BedrockModel:
    """
    Get Basic Claude Haiku 4.5 model, without any additional request fields.

    Returns:
        Model for Claude Haiku 4.5
    """
    return BedrockModel(model_id="global.anthropic.claude-haiku-4-5-20251001-v1:0", boto_client_config=boto_config)
