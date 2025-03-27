# Python Graph - Script by Khalil
# MS Docs: https://github.com/microsoftgraph/msgraph-sdk-python
# .\env\Scripts\Activate.ps1
from dotenv import load_dotenv
from azure.identity import InteractiveBrowserCredential
from msgraph import GraphServiceClient
import os
import asyncio

load_dotenv()

credential = InteractiveBrowserCredential(
    client_id=os.getenv('CLIENT_ID'),
    tenant_id=os.getenv('TENANT_ID'),
    redirect_uri='http://localhost:8400' # Hosts on this port until Auth is finished
)
scopes = ["User.Read"]

# credential = DefaultAzureCredential()
# scopes = ["https://graph.microsoft.com/.default"]

client = GraphServiceClient(credentials=credential, scopes=scopes)

async def GetME():
    try:
        info = await client.me.get()
    except KeyboardInterrupt:
        print("Exiting due to CTRL-C") 
    except Exception as ex:
        print(f"Error: {ex}")
        exit()

    if info:
        print(info.display_name)
        print(info.user_principal_name)
        print(info.id)

if __name__ == "__main__":
    asyncio.run(GetME())

# print(f"Client ID: {os.getenv('CLIENT_ID')}")
# print(f"Tenant ID: {os.getenv('TENANT_ID')}")