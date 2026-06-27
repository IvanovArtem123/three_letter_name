import httpx
import asyncio
import json

BASE_URL = "https://soul-goodman.space:8443/qgwcqFXkhD6gxZqHlT"


async def main():
    headers = {'Authorization': 'Bearer dRVzJiMkHJBlncJWwCnxM5FYahCdGwknBvMg8ypaKsyX6MCP'}
    async with httpx.AsyncClient(
        timeout=30.0,
        limits=httpx.Limits(max_keepalive_connections=20)
    ) as client:
        response = await client.get(
            url=f"{BASE_URL}/panel/api/inbounds/list",
            headers=headers
            )
        data = json.loads(response.text)
        print(data['obj'])

asyncio.run(main())
