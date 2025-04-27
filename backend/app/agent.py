from __future__ import annotations

import logging

from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

from app.settings import OPENAI_MODEL_NAME
from app.tools import get_tools

logger = logging.getLogger(__name__)


class Agent:
    def __init__(self) -> None:
        memory = InMemorySaver()
        tools = get_tools()
        llm = init_chat_model(OPENAI_MODEL_NAME, temperature=0)

        self._agent = create_react_agent(model=llm, tools=tools, checkpointer=memory)
        logger.info("Agent initialised with model=%s", OPENAI_MODEL_NAME)

    # Public API
    def chat(self, prompt: str, thread_id: str) -> str:
        config = {"configurable": {"thread_id": thread_id}}
        response = self._agent.invoke(
            {"messages": [{"role": "user", "content": prompt}]},
            config=config,
        )
        return response["messages"][-1].content


agent = Agent()  # singleton
