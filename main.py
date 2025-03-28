# Python Graph - Script by Khalil
# MS Docs: https://github.com/microsoftgraph/msgraph-sdk-python
# .\venv\Scripts\Activate.ps1
from azure.identity import InteractiveBrowserCredential
from msgraph import GraphServiceClient
from kiota_abstractions.api_error import APIError
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

class UserInfo:
    def __init__(self, email, displayName, id, groups, roles):
        self.Email = email
        self.DisplayName = displayName
        self.Id = id
        self.Groups = groups
        self.Roles = roles

credential = InteractiveBrowserCredential(
    client_id=os.getenv('CLIENT_ID'),
    tenant_id=os.getenv('TENANT_ID'),
    redirect_uri='http://localhost:8400' # Hosts locally on this port until Auth is finished
)
scopes = ["User.Read","User.Read.All","GroupMember.Read.All"]

# credential = DefaultAzureCredential()
# scopes = ["https://graph.microsoft.com/.default"]

client = GraphServiceClient(credentials=credential, scopes=scopes)

# Basic info about the Signed-in User
async def GetME():
    try:
        info = await client.me.get()
    except KeyboardInterrupt:
        print("Exiting due to CTRL-C") 
    except APIError as ex:
        print(f"Error: {ex.error.message}")
        exit()

    if info:
        print(info.display_name)
        print(info.user_principal_name)
        print(info.id)
        info.member_of
    
async def GetUser(email):
    try:
        user = await client.users.by_user_id(email).get()
        GraphGroups = await client.users.by_user_id(email).member_of.get()
    except APIError as ex:
        print(f"Could not find User: {user}")
        print(f"Error: {ex.error.message}")
        exit()
    
    groups = []
    roles = []
    for group in GraphGroups.value:
        if group.odata_type == "#microsoft.graph.group":
            groups.append(group.display_name)
        elif group.odata_type == "#microsoft.graph.directoryRole":
            roles.append(group.display_name)

    return UserInfo (
        user.user_principal_name,
        user.display_name,
        user.id,
        groups,
        roles
    )

if __name__ == "__main__":
    # asyncio.run(GetME())
    
    print("Please type in the Email of the User: ")
    Email = input()
    
    data = asyncio.run(GetUser(Email))
    print(f"\n\n\nDisplay Name: {data.DisplayName}")
    print(f"Email: {data.Email}")
    print(f"ID: {data.Id}")

    for Group in data.Groups:
        print(f"Group: {Group}")

    for Role in data.Roles:
        print(f"Role: {Role}")

# print(f"Client ID: {os.getenv('CLIENT_ID')}")
# print(f"Tenant ID: {os.getenv('TENANT_ID')}")