import httpx
import json


headers = {'Authorization': 'Bearer dRVzJiMkHJBlncJWwCnxM5FYahCdGwknBvMg8ypaKsyX6MCP'}

client = httpx.Client(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=20)
        )
BASE_URL = 'https://soul-goodman.space:8443/qgwcqFXkhD6gxZqHlT/panel/api'

response = client.get(url=f'{BASE_URL}/clients/get/002c0ck0oh', headers=headers)
print(json.loads(response.text)['obj'])
