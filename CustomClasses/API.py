import aiohttp
import asyncio
import json

async def malkTalk(key, preprompt, data):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "qwen/qwq-32b:free",  # Optional
        "messages": [
            {
                "role": "user",
                "content": f"{preprompt} \n\n {data}"
            }
        ]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            result = await response.json()
            return result