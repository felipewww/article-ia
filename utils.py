def calcInvertedPercent(num):
    if num == 0:
        return 0

    ttl = num + 10
    percent = (num * 100) / ttl
    invert = percent - 100

    if invert < 0:
        invert = invert * -1

    percentFinal = round(invert / 100, 3)

    return percentFinal


def sumIndex(index, arr):
    # return sum(dic[idx][index] for idx in dic)
    return sum(item[index] for item in arr)


def percent(x, total):
    if total == 0:
        return 0

    return round(((x * 100) / total) / 100, 3)


def getBigger(index, arr):
    return max(item[index] for item in arr)


def pretty_json(json):
    print(json.dumps(json, indent=2, sort_keys=True))