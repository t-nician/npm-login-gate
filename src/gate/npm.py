import aiohttp

from gate import env


class NPMClient:
    email = env.NPM_ACCOUNT_EMAIL
    password = env.NPM_ACCOUNT_PASSWORD
    
    access_list_name = env.NPM_ACCESS_LIST_NAME
    
    session = None
    token = ""
    
    async def login(self):
        self.session = aiohttp.ClientSession()

        response = await (await self.session.post(
            env.NPM_ENDPOINT_GET_TOKEN,
            json={
                "identity": self.email,
                "secret": self.password
            }
        )).json()
        
        self.token = response.get("token")
        
    
    async def refresh_token(self):
        response = await (await self.session.get(env.NPM_ENDPOINT_GET_TOKEN, headers={
            "Authorization": "Bearer " + self.token
        })).json()
        
        self.token = response.get("token")
    
    
    async def get_access_list(self):
        response = await (await self.session.get(
            env.NPM_ENDPOINT_GET_ACCESS_LISTS,
            headers={
                "Authorization": "Bearer " + self.token
            }
        )).json()

        for access_list in response:
            if access_list.get("name") == self.access_list_name:
                return access_list
    
    
    async def create_update_list(self):
        access_list_data = await self.get_access_list()
        access_list_id = access_list_data.get("id")
        
        update_access_list = {
            "name": self.access_list_name,
            "satisfy_any": access_list_data.get("satisfy_any"),
            "pass_auth": access_list_data.get("pass_auth"),
            "items":[],
            "clients": []
        }
        
        for client in access_list_data.get("clients"):
            address = client.get("address")
            directive = client.get("directive")
            
            update_access_list.get("clients").append({
                "address": address,
                "directive": directive
            })
        
        return update_access_list, access_list_id
        
        
    
    async def add_address(self, address: str):
        access_list, id = await self.create_update_list()
        
        already_added = False
        
        for client in access_list.get("clients"):
            if client.get("address") == address:
                already_added = True
                break
        
        if not already_added:
            access_list.get("clients").append({
                "address": address,
                "directive": "allow"
            })
        
        await self.session.put(
            env.NPM_ENDPOINT_PUT_ACCESS_LIST.format(id),
            json=access_list,
            headers={
                "Authorization": "Bearer " + self.token
            }
        )
    
    
    async def remove_address(self, address: str):
        access_list, id = await self.create_update_list()
        
        remove_index = -1
        
        for index, value in enumerate(access_list.get("clients")):
            if value.get("address") == address:
                remove_index = index
                break
        
        if remove_index != -1:
            del access_list.get("clients")[remove_index]
            
            await self.session.put(
                env.NPM_ENDPOINT_PUT_ACCESS_LIST.format(id),
                json=access_list,
                headers={
                    "Authorization": "Bearer " + self.token
                }
            )
        
        
    