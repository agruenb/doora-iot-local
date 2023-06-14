import requests
import os

#Pull all associations from the backend
def getAssociations():
    with open("remote_associations.json", "w") as file:
        response = requests.get(os.environ.get("BACKEND_URL") + "/api/getAllItemSets")
        content = response.content.decode("utf-8")
        file.write(content)
        return content

#Pull all items from the backend
def getKnownTags():
    with open("remote_all_items.json", "w") as file:
        response = requests.get(os.environ.get("BACKEND_URL") + "/api/getAllItems")
        content = response.content.decode("utf-8")
        file.write(content)
        return content

#Report a unknown tag to the backend
def reportNewItem(tagId):
    response = requests.post(os.environ.get("BACKEND_URL") + "/api/detectedNewTag" + "?tagID=" + tagId)
    content = response.content.decode("utf-8")
    return content