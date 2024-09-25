import asyncio

from openai import AsyncOpenAI

from bot.config import settings

client = AsyncOpenAI(api_key=settings.openai.api_key)


async def generate_text(query: str) -> str:
    if not settings.openai.enabled or settings.openai.stub_responses:
        await asyncio.sleep(2)
        return "Stub text response"

    completion = await client.chat.completions.create(
        model=settings.openai.model, messages=[{"role": "user", "content": query}]
    )
    return completion.choices[0].message.content
