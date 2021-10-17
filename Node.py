import math
import utils, random
class Node:
    def __init__(self):
        self.IP = utils.genRandomIP()
        self.nodeId = utils.getHashValue(self.IP)
        self.coordinates = utils.getRandomCoordinates()
        self.leafNodes = [self]
        self.neighbourNodes = [self]
        self.routingTable = [[None for i in range(pow(2,utils.getValueOfB()))] for j in range(32)]
        self.dataTable = {}
        self.uniqueId = random.randint(0, 1000000000)
        self.nodeVal=int(self.nodeId, 16)
        
    def getNodesFromRoutingTable(self):
        table = self.routingTable
        ans = set()
        for i in range(len(table)):
            for j in range(len(table[0])):
                if table[i][j] is not None:
                    ans.add(table[i][j])
        return list(ans)

    def print_leafset(self):
        print("leaf set of node " + self.nodeId + " are : =================")
        for i in self.leafNodes:
            print(i.nodeId)
        print("=============================================================")
    
    def isCircularOrderBrokenInLeadSet(self):
        for i in range(len(self.leafNodes)-1):
            if self.leafNodes[i].nodeId > self.leafNodes[i+1].nodeId:
                return False
        return True
    
    def printRoutingTable(self):
        ans = []
        for i in range(32):
            for j in range(16):
                if self.routingTable[i][j] is not None:
                    target = self.nodeId[:i] + str(hex(j))[2:] + "XX"
                    succ = self.routingTable[i][j].uniqueId
                    ans.append((target, succ))
        
        print("Routing table of node with id = " + str(self.uniqueId) + " and hashed node ID = " + self.nodeId)
        print("=========================")
        print("Sno--------------Target-------------Successor")
        for i in range(len(ans)):
            print(str(i+1) + " -------------- " + str(ans[i][0]) + " ----------------- " + str(ans[i][1]))
        print("==========================")
