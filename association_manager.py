import json
import time

def checkAssociations(tags):
    with open('associations.json') as raw_associations:
        associations = json.load(raw_associations)
        for association in associations["associations"]:
            for tagId in tags:
                if tagId in association["requiredItemTags"]:
                    if not set(association["requiredItemTags"]).issubset(tags):
                        print("Incomplete set {}".format(association["associationName"]))
                        for missingTagId in set(association["requiredItemTags"]) - set(tags).intersection(association["requiredItemTags"]):
                            print("Missing {}".format(getItemName(missingTagId)))
                        return False
    return True

def getItemName(tagId):
    with open('associations.json') as raw_associations:
        associations = json.load(raw_associations)
        for item in associations["items"]:
            if item["tagId"] == tagId:
                return item["itemName"]
            
def checkAlwaysRequired(tags):
    with open('associations.json') as raw_associations:
        associations = json.load(raw_associations)
        complete = set(associations["alwaysRequired"]) == set(tags).intersection(associations["alwaysRequired"])
        return complete
    
def extractInTimeTags(tags_list, timeout):
    in_time_tags = []
    for tag, value in tags_list.items():
        if value.get("lastSeen") > time.time() - timeout:
            in_time_tags.append(tag)
    return in_time_tags