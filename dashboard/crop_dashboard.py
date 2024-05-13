from typing import Any, Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from .utils import load_llm, flatten_nested_dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
    RunnableParallel,
)
from operator import itemgetter
from logger import log_function_time
from langchain_core.runnables import Runnable, RunnableBranch
from langchain_core.language_models import BaseChatModel


class CropDashboard(BaseModel):
    llm: BaseChatModel | None = Field(default_factory=load_llm)
    fallback_llm: BaseChatModel | None = None

    class Config:
        arbitrary_types_allowed = True

    @log_function_time
    def create_chain(
        self,
        prompt_template,
        schema: BaseModel = None,
    ) -> Runnable:
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = (
            RunnableParallel(
                {
                    "farm_data": itemgetter("farm_data")
                    | RunnableLambda(flatten_nested_dict),
                    "weather_data": itemgetter("weather_data") | RunnablePassthrough(),
                }
            )
            | (lambda x: {**x["farm_data"], **x["weather_data"]})
            | prompt
            | (
                (
                    self.llm
                    if self.fallback_llm is None
                    else self.llm.with_fallbacks([self.fallback_llm])
                )
                if schema is None
                else (
                    self.llm.bind_tools(
                        tools=[convert_to_openai_tool(schema)],
                        # tool_choice=schema.__name__,
                    )
                    if self.fallback_llm is None
                    else self.llm.bind_tools(
                        tools=[convert_to_openai_tool(schema)],
                        # tool_choice=schema.__name__,
                    ).with_fallbacks(
                        fallbacks=[
                            self.fallback_llm.bind_tools(
                                tools=[schema],  # tool_choice=schema.__name__
                            )
                        ]
                    )
                )
            )
            | (StrOutputParser() if schema is None else JsonOutputToolsParser())
            | RunnableBranch(
                (lambda x: isinstance(x, list) and len(x) > 0, lambda x: x[0]["args"]),
                (lambda x: x),
            )
        )
        return chain

    @classmethod
    def from_llm(
        cls,
        llm,
        fallback_llm,
        prompt_template,
        schema: BaseModel = None,
    ):
        return CropDashboard(llm=llm, fallback_llm=fallback_llm).create_chain(
            prompt_template, schema=schema
        )
