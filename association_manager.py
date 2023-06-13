import json
import time

def getItemName(tagId):
    with open('associations.json') as raw_associations:
        associations = json.load(raw_associations)
        for item in associations["items"]:
            if item["tagId"] == tagId:
                return item["itemName"]
    
def extractInTimeTags(tags_list, timeout):
    in_time_tags = []
    for tag, value in tags_list.items():
        if value.get("lastSeen") > time.time() - timeout:
            in_time_tags.append(tag)
    return in_time_tags

def checkAssociations(tags = []):
    with open('remote_associations.json') as raw_associations:
        assoc = json.load(raw_associations)
        for association in assoc:
            if association["alwaysRequired"] == True:
                for item in association["assignedItems"]:
                    if str(item["tagID"]) not in tags:
                        print("missing " + str(item["tagID"]))
                        return False
            else:
                tags_in_set = list(map(lambda item:item["tagID"], association["assignedItems"]))
                intersection = set(tags).intersection(set(tags_in_set))
                if len(intersection) != 0 and intersection != set(tags_in_set):
                    return False
    return True
