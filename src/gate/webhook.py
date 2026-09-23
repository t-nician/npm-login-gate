import aiohttp


from gate import env


async def on_success(address: str):
    if env.WEBHOOK_ON_SUCCESS:
        data = {
            "content": env.WEBHOOK_SUCCESS_MESSAGE.format(address)
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(env.WEBHOOK_URL, data=data) as response:
                pass


async def on_failure(address: str):
    if env.WEBHOOK_ON_FAILURE:
        data = {
            "content": env.WEBHOOK_FAILURE_MESSAGE.format(address)
        }
                
        async with aiohttp.ClientSession() as session:
            async with session.post(env.WEBHOOK_URL, data=data) as response:
                pass


async def on_timeout(address: str):
    if env.WEBHOOK_ON_TIMEOUT:
        data = {
            "content": env.WEBHOOK_TIMEOUT_MESSAGE.format(address)
        }
                
        async with aiohttp.ClientSession() as session:
            async with session.post(env.WEBHOOK_URL, data=data) as response:
                pass