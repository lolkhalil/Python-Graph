# Python Graph - Script by Khalil
# MS Docs: https://github.com/microsoftgraph/msgraph-sdk-python // https://learn.microsoft.com/en-us/graph/tutorials/python?tabs=aad
# .\env\Scripts\Activate.ps1
from dotenv import load_dotenv
import os

load_dotenv()

print(f"Client ID: {os.getenv('CLIENT_ID')}")
print(f"Tenant ID: {os.getenv('TENANT_ID')}")