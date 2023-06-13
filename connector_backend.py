import requests
import os

def getAssociations():
    with open("remote_associations.json", "w") as file:
        response = requests.get(os.environ.get("BACKEND_URL") + "/api/getAllItemSets")
        content = response.content.decode("utf-8")
        file.write(content)
        return content

def getKnownTags():
    with open("remote_all_items.json", "w") as file:
        response = requests.get(os.environ.get("BACKEND_URL") + "/api/getAllItems")
        content = response.content.decode("utf-8")
        file.write(content)
        return content