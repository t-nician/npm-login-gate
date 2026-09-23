from gate import model, env


cached_attempts: dict[str, int] = {}


async def is_timed_out(address: str):
    return await model.Timedout.get_or_none(address=address) != None


async def is_whitelisted(address: str):
    return await model.Whitelisted.get_or_none(address=address) != None


async def attempt_login(address: str, password: str):
    
    
    return "You have been whitelisted!"