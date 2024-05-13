from functools import lru_cache


@lru_cache
def load_llm(model: str = "gpt-3.5-turbo-0125", temperature=0.0):
    if "gpt" in model:
        try:
            from langchain_openai.chat_models import ChatOpenAI
        except ImportError:
            raise ImportError(
                "Please, install langchain_openai. `pip install langchain-openai`"
            )
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            model_kwargs={"stop": ["Please, Note", "It is important"]},
        )
    elif "claude" in model:
        try:
            from langchain_anthropic.chat_models import ChatAnthropic
        except ImportError:
            raise ImportError(
                "Please, install langchain_anthropic. `pip install langchain-anthropic`"
            )
        return ChatAnthropic(
            model=model,
            temperature=temperature,
        )
    else:
        raise ValueError(
            "Invalid model name. Please, only openai or anthropic models are supported."
        )


def flatten_nested_dict(nested_dict):
    """
    Flattens a nested dictionary.

    Args:
        nested_dict (dict): The nested dictionary to be flattened.

    Returns:
        dict: A flattened dictionary containing the data from the nested dictionary.
    """
    result = {}

    for key, value in nested_dict.items():
        if isinstance(value, dict):
            flattened_dict = flatten_nested_dict(value)
            result.update(flattened_dict)
        elif isinstance(value, list):
            result[key] = ", ".join(map(str, value))
        else:
            result[key] = value

    return result
