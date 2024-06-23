import json


def ensureEnoughDifferentItems(itemType, differentItemsNeeded, data):
    itemsFound = []
    itemType = itemType.split(";")
    for i in range(len(data)):
        found = data[i]
        for x in range(len(itemType)):
            if itemType[x] == "0":
                itemType[x] = 0
            elif itemType[x] == "1":
                itemType[x] = 1
            found = found[itemType[x]]
        if found not in itemsFound:
            itemsFound.append(found)
    return len(itemsFound) >= differentItemsNeeded
