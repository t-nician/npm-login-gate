import time
import asyncio

from gate import webhook, model, npm, env
from contextlib import asynccontextmanager

npm_client = npm.NPMClient()
cached_attempts: dict[str, int] = {}


async def is_timed_out(address: str):
    return await model.Timedout.get_or_none(address=address) != None


async def is_whitelisted(address: str):
    return await model.Whitelisted.get_or_none(address=address) != None


async def gate(nginx_address, client_address: str):
    if nginx_address != env.NGINX_HOST:
        return "Wait a second... who are you?!"
    
    timed_out = await is_timed_out(client_address)
    whitelisted = await is_whitelisted(client_address)
    
    if timed_out:
        return "You are timed out!"
    
    if whitelisted:
        return "You are already whitelisted!"

    return None


async def timeout_address(address: str):
    await model.Timedout.create(
        address=address,
        untimeout_at=int(time.time()) + (env.LOGIN_FAIL_TIMEOUT * 60)
    )


async def whitelist_address(address: str):    
    await model.Whitelisted.create(
        address=address,
        unwhitelist_at=int(time.time()) + (env.LOGIN_LIFETIME * 3600)
    )
    
    await npm_client.add_address(address)
    

async def heartbeat():
    while True:
        await asyncio.sleep(30)
        await npm_client.refresh_token()
        
        current_time = int(time.time())
        
        for timedout in await model.Timedout.all():
            if timedout.untimeout_at <= current_time:
                print(timedout.address, " timeout has been removed.")
                
                await timedout.delete()
        
        for whitelisted in await model.Whitelisted.all():
            if whitelisted.unwhitelist_at <= current_time:
                print(whitelisted.address, " whitelist has been removed.")
                
                await whitelisted.delete()
                await npm_client.remove_address(whitelisted.address)


@asynccontextmanager
async def lifespan(app):
    await npm_client.login()
    
    task = asyncio.create_task(heartbeat())
    
    yield
    
    npm_client.session.close()
    task.cancel()
    

async def attempt_login(address: str, password: str):
    if not address in cached_attempts:
        cached_attempts[address] = 0
    
    if password != env.LOGIN_PASSWORD:
        cached_attempts[address] += 1
        
        if cached_attempts[address] >= env.LOGIN_MAX_ATTEMPTS:
            del cached_attempts[address]
            
            await timeout_address(address)
            await webhook.on_timeout(address)
            
            print(address, " has been timed out!")
            
            return "You have been timed out!"
        
        await webhook.on_failure(address)
        
        print(address, " failed to login!")
        
        return "Login attempt failed!"
    else:
        await whitelist_address(address)
        await webhook.on_success(address)
        
        print(address, " has been whitelisted!")
        
        return "You have been whitelisted!"
    