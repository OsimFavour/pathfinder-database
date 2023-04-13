import json
from config import Config

# with open("secrets/client_secret.json") as file:
#         content = json.load(file)

file = Config().content

file = json.loads(file)
# print(file["web"])
client_id = file["web"]["client_id"]
project_id = file["web"]["project_id"]
print(f"{client_id}\n{project_id}" )

# print(os.environ["CLIENT_SECRET"] )