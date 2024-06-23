import json


def ensureEnoughDifferentItems(itemType, differentItemsNeeded, data):
    itemsFound = []
    itemType = itemType.split(";")
    for i in range(len(data)):
        found = data[i]
        for x in range(len(itemType)):
            found = found[itemType[x]]
        if found not in itemsFound:
            itemsFound.append(found)
    return len(itemsFound) >= differentItemsNeeded
