import os
import asyncio
from dotenv import load_dotenv

from autogen_core import (
    SingleThreadedAgentRuntime,
    TopicId,
)

from autogen_ext.models.openai import OpenAIChatCompletionClient

# Updated import to use tone_memory (ListMemory-based)
from memory_store import tone_memory, user_id  # tone_memory is your ListMemory instance

# Import agent classes and topic types
from agents.resume_agent import ResumeAgent, resume_topic_type
from agents.keyword_agent import KeywordAgent, keyword_topic_type
from agents.user_agent import UserAgent, user_topic_type

# Import the shared message schema
from schemas.message_schema import ResumeMessage

# -------------------------- Memory Initialization --------------------------
user_memory = tone_memory  # This is the ListMemory used in app.py

# -------------------------- Load API Key --------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# -------------------------- Main Runtime --------------------------
async def main(resume_text: str, jd_text: str, tone: str):  # ⬅ Add tone here
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash",
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        model_info={
            "family": "GEMINI_2_0_FLASH",
            "function_calling": True,
            "json_output": True,
            "vision": False,
            "structured_output": True
        }
    )

    runtime = SingleThreadedAgentRuntime()

    # Register agents
    await ResumeAgent.register(runtime, type=resume_topic_type, factory=lambda: ResumeAgent(model_client))
    await KeywordAgent.register(runtime, type=keyword_topic_type, factory=lambda: KeywordAgent(model_client))
    await UserAgent.register(runtime, type=user_topic_type, factory=lambda: UserAgent())

    # Start runtime
    runtime.start()

    # ✅ Send ResumeMessage with tone
    await runtime.publish_message(
        ResumeMessage(resume=resume_text, job_description=jd_text, tone=tone),  # ⬅ FIXED HERE
        topic_id=TopicId(resume_topic_type, source="user")
    )

    await runtime.stop_when_idle()
    await model_client.close()
