from DHT import *
from Node import Node
import matplotlib.pyplot as plt
import sys

def CountFrequency(my_list): 
   
    freq = {} 
    for item in my_list: 
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1
    
    x = []
    y = []

    temp = []
    for key, value in freq.items(): 
        print ("% d : % d"%(key, value)) 
        temp.append([key, value])
    temp.sort()
    for i in temp:
        x.append(i[0])
        y.append(i[1])
    # print("haha")
    return x, y
    

dht = DHT()
numOfNodes = 1000
if (len(sys.argv) >  1):
    numOfNodes = int(sys.argv[1])
    
for i in range(numOfNodes):
    node = Node()
    dht.addNodeToDHT(node)

# dht.redoRoutingTable()

print("Nodes added successfully")

routing_table = dht.nodes[0].routingTable

count=0

for i in range(len(routing_table)):
    for j in range(len(routing_table[0])):
        if routing_table[i][j] is not None:
            count+=1
# print(count)

numOfKeys = 10000
numOfQueries = 1000000
# dht.print_nodes()
for i in range(numOfKeys):
    dht.addKeyToDHT(i, "val" + str(i))
# dht.addKeyToDHT(1, "shivansh")
# dht.addKeyToDHT(3, "ritu")
# dht.addKeyToDHT("yoyo", "mom")

print("Keys added successfully")

hops = []
for i in range(numOfQueries):
    key = random.randint(0, numOfKeys-1)
    val,hop = dht.getValueFromDHT(key)
    if val is None:
        print("Some error")
    else:
        hops.append(hop)

print("Values retrieved successfully")
# print(sum(hops)*1.0/numOfKeys)
print("Average hops with 1000000 queries and " + str(numOfNodes) + " nodes and " + str(numOfKeys) + " data points are " + str(sum(hops)*1.0/numOfQueries))
print("============")

x, y = CountFrequency(hops)
y_pos = []
for i in range(len(x)):
    y_pos.append(i)
plt.bar(y_pos, y, align='center', alpha=0.5, width=0.2)
plt.xticks(y_pos, x)
plt.ylabel('Frequency')
plt.xlabel('Number of hops')
plt.title('Distribution of hops with ' + str(numOfNodes) + 'nodes with 1 million queries')
plt.savefig(str(numOfNodes) + ".svg")


while(dht.numberOfNodes > numOfNodes/2):
    # print("Num of nodes in dht are " + str(dht.numberOfNodes))
    ind = random.randint(0, len(dht.nodes)-1)
    dht.deleteNodeFromDHT(dht.nodes[ind])



# dht.addKeyToDHT("yoyo", "dad")
# dht.redoRoutingTable()
print("Nodes deleted successfully")

hops1 = []

for i in range(numOfQueries):
    key = random.randint(0, numOfKeys-1)
    val,hop = dht.getValueFromDHT(key)
    if val is None:
        print("Some error")
    else:
        hops1.append(hop)

print("Values retrieved successfully")
print("Average hops with 1000000 queries and " + str(numOfNodes//2) + " nodes and " + str(numOfKeys) + " data points are " + str(sum(hops1)*1.0/numOfQueries))
# hops = map(int, hops)
plt.clf()
print("============")
x, y = CountFrequency(hops1)
y_pos = []
for i in range(len(x)):
    y_pos.append(i)
plt.bar(y_pos, y, align='center', alpha=0.5, width=0.2)
plt.xticks(y_pos, x)
plt.ylabel('Frequency')
plt.xlabel('Number of hops')
plt.title('Distribution of hops with ' + str(numOfNodes//2) + 'nodes left after deletion with 1 million queries')
plt.savefig(str(numOfNodes//2) + ".svg")


print("Total number of nodes : " + str(numOfNodes))
print("Total number of data elements : " + str(numOfKeys))
print("Total search queries : " + str(numOfQueries))
print("Total node add queries : " + str(numOfNodes))
print("Total node delete queries : " + str(numOfNodes//2))
print("Total data add queries : " + str(numOfKeys))

dht.nodes[random.randint(0, len(dht.nodes)-1)].printRoutingTable()