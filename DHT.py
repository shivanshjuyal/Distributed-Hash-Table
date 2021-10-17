import utils, random, math


from Node import Node
class DHT:
    def __init__(self):
        self.nodes = []
        self.nodeIdToNodeDict = {}
        self.numberOfNodes = 0


    def addNodeToDHT(self, node):

        if (self.numberOfNodes == 0):
            self.nodes.append(node)
            self.nodes.sort(key=lambda x: x.nodeId)
            self.nodeIdToNodeDict[node.nodeId] = node
            self.numberOfNodes += 1
            # print("Added first============")
            return

        # inititalNodeToConnect = self.__getRandomNodeFromDHT()
        inititalNodeToConnect = self.__getClosestGeoNodeFromDHT(node)
        # node.leafNodes = self.nodes #remove this, just for testing
        keyHash = utils.getHashValue(node.nodeId)
        targetNode,hops,encounteredNodes = self.__route(keyHash, node.nodeId, inititalNodeToConnect,1, [inititalNodeToConnect])
        # print("Num of encountered nodes are ============" + str(len(encounteredNodes)))
        self.__buildRoutingTable(encounteredNodes, node)
        self.nodes.append(node)
        self.nodes.sort(key=lambda x: x.nodeId)
        self.nodeIdToNodeDict[node.nodeId] = node
        self.numberOfNodes += 1

        self.redoLeavesSet()
        # print("Added total " + str(self.numberOfNodes))

        if (self.numberOfNodes == 1):
            return
        
        
    

    def __buildRoutingTable(self, encounteredNodes, currNode):
        allNewNodes = set()
        for i in encounteredNodes:
            allNewNodes.update(set(i.getNodesFromRoutingTable()))
            allNewNodes.update(set([i]))
        allNewNodes = list(allNewNodes)
        for node in allNewNodes:
            if (currNode.nodeId == node.nodeId):
                continue
            row = utils.longestCommonPrefix(currNode.nodeId, node.nodeId)
            col = int(node.nodeId[row], 16)
            if currNode.routingTable[row][col] is None:
                currNode.routingTable[row][col] = node 
        
        for node in allNewNodes:
            if (currNode.nodeId == node.nodeId):
                continue
            row = utils.longestCommonPrefix(currNode.nodeId, node.nodeId)
            col = int(currNode.nodeId[row], 16)
            if node.routingTable[row][col] is None:
                node.routingTable[row][col] = currNode


        
    def redoLeavesSet(self):
        leafOffset = 2 ** utils.getValueOfB()
        # print("leaf offset is " + str(leafOffset))
        for i in range(len(self.nodes)):
            currNode = self.nodes[i]
            if self.numberOfNodes <= leafOffset * 2 + 1:
                # print("Copying " + currNode.nodeId)
                currNode.leafNodes = []
                for node in self.nodes:
                    currNode.leafNodes.append(node)
            else:
                
                if i-leafOffset < 0:
                    currNode.leafNodes = self.nodes[i-leafOffset:self.numberOfNodes] + self.nodes[0:i+leafOffset+1]
                elif i+leafOffset>self.numberOfNodes-1:
                    currNode.leafNodes = self.nodes[i-leafOffset:self.numberOfNodes] + self.nodes[0: leafOffset-self.numberOfNodes+i+1]
                else:
                    currNode.leafNodes = self.nodes[i-leafOffset: i+1] + self.nodes[i+1:i+leafOffset+1]


    def redoRoutingTable(self):
        for node in self.nodes:
            node.routingTable = [[None for i in range(pow(2,utils.getValueOfB()))] for j in range(32)]
        
        for currNode in self.nodes:
            for node in self.nodes:
                if (currNode.nodeId == node.nodeId):
                    continue
                row = utils.longestCommonPrefix(currNode.nodeId, node.nodeId)
                col = int(node.nodeId[row], 16)
                if currNode.routingTable[row][col] is None:
                    currNode.routingTable[row][col] = node
                

    def deleteNodeFromDHT(self, node):
        # self.nodes.remove(node)
        self.numberOfNodes -= 1
        self.__shiftKeysAndRemoveNode(node)
        self.__removeNodeFromAllRoutingTable(node)
        self.redoLeavesSet()
        # Todo: remove from nodeIdToIPDict
        
    def __removeNodeFromAllRoutingTable(self, node):
        for currNode in self.nodes:
            for i in range(len(currNode.routingTable)):
                for j in range(len(currNode.routingTable[0])):
                    if currNode.routingTable[i][j] is not None and currNode.routingTable[i][j].nodeId==node.nodeId:
                        currNode.routingTable[i][j] = None
       
    def __shiftKeysAndRemoveNode(self, node):
        ind = self.__getIndexOfNode(self.nodes, node)
        leftNeighbour = self.nodes[ind-1]
        rightNeighbour = None
        if ind == len(self.nodes)-1:
            rightNeighbour = self.nodes[0]
        else:
            rightNeighbour = self.nodes[ind+1]
        for key in node.dataTable.keys():
            minDiff = abs(int(leftNeighbour.nodeId, 16) - int(key, 16))
            nodeToShift = leftNeighbour
            if (abs(int(rightNeighbour.nodeId, 16) - int(key, 16)) < minDiff):
                nodeToShift = rightNeighbour
            nodeToShift.dataTable[key] = node.dataTable[key]
            # print("shifting key " + key + " to " + nodeToShift.nodeId)
        self.nodes.pop(ind)

    def __getIndexOfNode(self, nodes, node):
        for i in range(len(nodes)):
            if self.nodes[i].nodeId == node.nodeId:
                return i

    def addKeyToDHT(self, key, value):
        inititalNodeToConnect = self.__getRandomNodeFromDHT()
        # inititalNodeToConnect.print_leafset()
        key = str(key)
        keyHash = utils.getHashValue(key)
        # print("Hash value to insert is " + keyHash)
        # return inititalNodeToConnect
        targetNode,hops,encounteredNodes = self.__route(keyHash, key, inititalNodeToConnect,1, [inititalNodeToConnect])
        # print("key :" + key + " added to " + targetNode.nodeId)
        targetNode.dataTable[keyHash] = value


    def getValueFromDHT(self, key):
        initialNodeToConnect = self.__getRandomNodeFromDHT()
        # initialNodeToConnect.print_leafset()
        key = str(key)
        keyHash = utils.getHashValue(key)
        # print("Hash value to get is " + keyHash)
        targetNode,hops,encounteredNodes = self.__route(keyHash, key, initialNodeToConnect,1, [initialNodeToConnect])
        # print("key :" + key + " found in " + targetNode.nodeId)
        if keyHash in targetNode.dataTable:
            return targetNode.dataTable[keyHash], hops
        print("Hash to find is " + keyHash)
        targetNode.print_leafset()
        return None


    def __getRandomNodeFromDHT(self):
        return self.nodes[random.randint(0, len(self.nodes) - 1)]

    def __getClosestGeoNodeFromDHT(self, node):
        closest = self.nodes[0]
        minDiff = math.inf
        for currNode in self.nodes:
            temp = ((node.coordinates[0]-currNode.coordinates[0])**2 + (node.coordinates[1]-currNode.coordinates[1])**2)**0.5
            if temp < minDiff:
                minDiff = temp
                closest = currNode
        return closest

    def __isKeyHashInRangeLeafSet(self, keyHash, leafSet):

        leafOffset = 2 ** utils.getValueOfB()
        if len(leafSet) < 2*leafOffset+1:
            return True

        isCircularOverlap = self.__isCircularOrderBrokenInLeafSet(leafSet)
        # print("Bool " + str(isCircularOverlap))
        if isCircularOverlap:
            if keyHash <= leafSet[0].nodeId  and keyHash >= leafSet[-1].nodeId:
                # print("Returning false")
                return False
            return True
        else:
            # print(len(leafSet))
            if keyHash >=leafSet[0].nodeId and keyHash <= leafSet[-1].nodeId:
                # print("Returning true=========")
                return True
            # print("Returning false")
            return False

    
    def __isCircularOrderBrokenInLeafSet(self, leafSet):
        for i in range(len(leafSet)-1):
            if leafSet[i].nodeId > leafSet[i+1].nodeId:
                return True
        return False

    def __findClosestNodeInLeafSet(self, keyHash, leafSet):
        minDiff = abs(int(keyHash, 16) - int(leafSet[0].nodeId, 16))
        ansNode = leafSet[0]
        for node in leafSet:
            # diff = utils.lexicographicDiff(keyHash, node.nodeId)
            diff = abs(int(keyHash, 16) - int(node.nodeId, 16))
            if diff < minDiff:
                minDiff = diff
                ansNode = node
        # print("smallest node is " + ansNode.nodeId)
        return ansNode


    def __route(self, keyHash, key, node, hops, encounteredNodes):
        if self.__isKeyHashInRangeLeafSet(keyHash, node.leafNodes):
            # print("Found in leaf set of " + node.nodeId + "============================")
            smallestNode = self.__findClosestNodeInLeafSet(keyHash, node.leafNodes)
            # print("Found in node " + smallestNode.nodeId + "=============================")
            if smallestNode.nodeId == node.nodeId:
                return smallestNode, hops, encounteredNodes
            return smallestNode,hops+1, encounteredNodes + [smallestNode]
        longCommonPrefix = utils.longestCommonPrefix(keyHash, node.nodeId)
        row = longCommonPrefix 
        col = int(keyHash[row], 16)
        if (node.routingTable)[row][col] is not None:
            # print("Routing from " + node.nodeId + " to " + (node.routingTable)[row][col].nodeId)
            return self.__route(keyHash, key, (node.routingTable)[row][col], hops+1, encounteredNodes+[(node.routingTable)[row][col]])
        # print("Handling rare case")
        #rare case
        totalSet = set()
        for i in node.leafNodes:
            totalSet.add(i)
        for i in node.neighbourNodes:
            totalSet.add(i)
        for i in node.getNodesFromRoutingTable():
            totalSet.add(i)

        totalSet.add(node)
        totalList = list(totalSet)

        # minDiff = math.inf
        # smallestNode = None
        # for i in totalList:
        #     if (utils.longestCommonPrefix(keyHash, i.nodeId) >= longCommonPrefix) and utils.lexicographicDiff(i.nodeId, keyHash) < minDiff:
        #         minDiff = utils.lexicographicDiff(i.nodeId, keyHash)
        #         smallestNode = i

        smallestNode = self.__findClosestNodeInLeafSet(keyHash, totalList)
        # print("Routing from " + node.nodeId + " to " + smallestNode.nodeId)
        if (smallestNode.nodeId == node.nodeId):
            return smallestNode, hops, encounteredNodes
        return self.__route(keyHash, key, smallestNode, hops+1, encounteredNodes+[smallestNode])
        




