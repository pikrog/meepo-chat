import httpx


async def get_external_ip_info(api_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        ip_info = response.json()
        ip, country, city = ip_info['query'], ip_info['country'], ip_info['city']
        return ip, country, city
