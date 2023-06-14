import json
import time

#return all tags that were scanned in less time ago then timeout
def extractInTimeTags(tags_list, timeout):
    in_time_tags = []
    for tag, value in tags_list.items():
        if value.get("lastSeen") > time.time() - timeout:
            in_time_tags.append(tag)
    return in_time_tags

#get an item from the items file
def getItem(tagId):
    with open('remote_all_items.json') as raw_items:
        items = json.load(raw_items)
        item = list(filter(lambda item:item["tagID"] == tagId, items))
        if len(item) != 0:
            return item[0]
        else:
            return None

#check if all associations hold true with the input tags
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
