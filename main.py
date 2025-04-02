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
    def __init__(self, email, displayName, id):
        self.Email = email
        self.DisplayName = displayName
        self.Id = id

class Graph:
    def __init__(self):
        credential = InteractiveBrowserCredential(
            client_id=os.getenv('CLIENT_ID'),
            tenant_id=os.getenv('TENANT_ID'),
            redirect_uri='http://localhost:8400' # Hosts locally on this port until Auth is finished
        )
        scopes = ["User.Read","User.Read.All","GroupMember.Read.All"]

        # credential = DefaultAzureCredential()
        # scopes = ["https://graph.microsoft.com/.default"]

        self.client = GraphServiceClient(credentials=credential, scopes=scopes)

# Basic info about the Signed-in User
async def GetMe():
    try:
        info = await client.me.get()
    except KeyboardInterrupt: # this doesn't work?
        print("Exiting due to CTRL-C") 
    except APIError as ex:
        print(f"Error: {ex.error.message}")
        exit()

    if info:
        print(info.display_name)
        print(info.user_principal_name)
        print(info.id)
    
async def GetUser(client: Graph, email):
    try:
        user = await client.users.by_user_id(email).get()
    except APIError as ex:
        print(f"Could not find User: {user}")
        print(f"Error: {ex.error.message}")
        exit()

    return UserInfo (
        user.user_principal_name,
        user.display_name,
        user.id
    )

async def GetGroups(client: Graph, user):
    try:
        GraphGroups = await client.users.by_user_id(user).member_of.get()
    except APIError as ex:
        print(f"Could not get Groups for User: {user}")
        print(f"Error: {ex.error.message}")
        exit()
    
    groups = []
    roles = []
    for group in GraphGroups.value:
        if group.odata_type == "#microsoft.graph.group":
            print(group.display_name)
            groups.append(group.display_name)
        elif group.odata_type == "#microsoft.graph.directoryRole":
            print(group.display_name)
            roles.append(group.display_name)

    return {
        "Groups": groups,
        "Roles": roles
    }

if __name__ == "__main__":
    client = Graph().client
    # asyncio.run(GetMe())
    
    # Get User #
    print("Please type in the Email of the User: ")
    Email = input()
    
    data = asyncio.run(GetUser(client, Email))
    print(f"\nDisplay Name: {data.DisplayName}")
    print(f"Email: {data.Email}")
    print(f"ID: {data.Id}")


    # Get Groups #
    print(f"\nDo you want to get the Groups for {data.DisplayName}?")
    answer = ""
    
    while (answer == ""):
        answer = input()
        if (answer.upper() == "Y"):
            break
        elif (answer.upper() == "N"):
            exit()
        else:
            print("Please give a correct input.")
            answer = ""
    
    # Can't make more than one Graph call for some reason?
    group_data = asyncio.run(GetGroups(client, Email))

    for Group in group_data["Groups"]:
        print(f"Group: {Group}")

    for Role in group_data["Roles"]:
        print(f"Role: {Role}")
