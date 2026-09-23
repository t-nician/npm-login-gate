import asyncio

#from gate import npm
from gate import server


#async def main():
    #client = npm.NPMClient()
    #await client.login()
    
    #await client.remove_address("2.2.2.2")


if __name__ == "__main__":
    #asyncio.run(main())
    server.launch()