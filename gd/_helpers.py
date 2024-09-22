import httpx

class ResponseError(Exception):
    pass

async def post(**kwargs):
    async with httpx.AsyncClient() as client:
        response = await client.post(**kwargs, headers={"User-Agent": ""})
        if response.status_code == 200:
            return await response.json()
        else:
            raise ResponseError(f"Unable to fetch data, got {response.status_code}.")