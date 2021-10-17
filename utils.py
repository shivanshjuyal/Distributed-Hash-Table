import hashlib, random
  
def getHashValue(str):
  
    result = hashlib.sha256(str.encode()) 

    return result.hexdigest()[-32:]

def genRandomIP():
    ipNumList = []
    for i in range(4):
        ipNumList.append(random.randint(0,255))
    ipNumList = map(str, ipNumList)
    return ".".join(ipNumList)

def getRandomCoordinates():
    coord = []
    coord.append(random.randint(0, 100))
    coord.append(random.randint(0, 100))
    return coord

def getValueOfB():
    return 4

def lexicographicDiff(str1, str2):
    i = 0
    while(i < len(str1) and i < len(str2) and str1[i] == str2[i]):
        i += 1
    # return abs(ord(str1[i]) - ord(str2[i]))
    return abs(int(str1[i], 16) - int(str2[i], 16))
    
    


def longestCommonPrefix(str1, str2):
    i = 0
    while(i < len(str1) and i < len(str2) and str1[i] == str2[i]):
        i += 1
    return i

# print(longestCommonPrefix("abc", "abd"))