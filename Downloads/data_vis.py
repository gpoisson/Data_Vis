import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


# user-defined variables
debug = True
axisOn = False
labelsOn = True
maxNodes = 20
edgeColor = 'g'
dottedLine = ':'
darkGrey = '#191919'
lightGrey = '#a3a3a3'
plotBackgroundColor = darkGrey
fontColor = lightGrey
gridColor = 'k'



# global variables
hTable = []
ax = None
numNodes = 0

# initialize plot
def initPlot():
    global ax, fontColor
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', axisbg=plotBackgroundColor)
    if axisOn == False:
        ax.set_axis_off()
    else:
        ax.set_axis_on()
        fontColor = darkGrey

# gives n random float values between vmin and vmax
def randrange(n, vmin, vmax):
    return (vmax - vmin) * np.random.rand(n) + vmin

# builds an empty node with a given value, helper method for makeNode
def makeNodeS(value):
    global hTable, numNodes
    n = Node(value)
    hTable.append(n)
    numNodes = len(hTable)
    return n

# builds a node with given parameters
def makeNode(value, location, color, marker):
    n = makeNodeS(value)
    n.setLoc(location)
    n.setStyle(color, marker)
    if debug:
        print("Building node {} at {} with color = {}, marker = {}, and associations = {}.".format(value, location, color, marker, n.assocs))
    return n

# aggregate nodes in hTable and plot them in 3D
def plotNodes():
    global hTable
    if debug:
        print("Plotting Graph...")
    for elem in hTable:
        if debug:
            print(" Plotting node {}...".format(elem.value))
        ax.scatter(elem.location[0], elem.location[1], elem.location[2], c=elem.color, marker=elem.marker)
        for c in elem.assocs:
            if (getNode(c).value != elem.value):
                if elem.count in getNode(c).assocs:   # if the two nodes are associated to each other, draw solid line
                    ax.plot([elem.location[0], getNode(c).location[0]], [elem.location[1], getNode(c).location[1]], [elem.location[2], getNode(c).location[2]], edgeColor)
                    if debug:
                        print("  Plotting double edge between {} and {}...".format(elem.value, getNode(c).value))
                else:
                    ax.plot([elem.location[0], getNode(c).location[0]], [elem.location[1], getNode(c).location[1]], [elem.location[2], getNode(c).location[2]], edgeColor + dottedLine)
                    if debug:
                        print("  Plotting single edge from {} to {}...".format(elem.value, getNode(c).value))

# build single connection from node A to node B
def sConnect(nodeA, nodeB):
    nodeA.addAssoc(nodeB)
    if debug:
        print(" Drawing single connection from node {} to node {}...".format(nodeA.value, nodeB.value))

# build double connection from node A to node B, and from node B to node A
def dConnect(nodeA, nodeB):
    if debug:
        print("\nDouble node connection steps:")
    sConnect(nodeA, nodeB)
    sConnect(nodeB, nodeA)

def getNode(count):
    global hTable
    n = hTable[count-1]
    return n

# set up axis info
def defineAxis():
    ax.set_xlabel('X Label')
    ax.xaxis.label.set_color(lightGrey)
    ax.tick_params(axis='x', colors=lightGrey)
    ax.set_ylabel('Y Label')
    ax.yaxis.label.set_color(lightGrey)
    ax.tick_params(axis='y', colors=lightGrey)
    ax.set_zlabel('Z Label')
    ax.zaxis.label.set_color(lightGrey)
    ax.tick_params(axis='z', colors=lightGrey)

# randomly populate nodes and connect them
def test():
    for i in range (0, maxNodes):
        rand = np.random.rand(2)
        if (0 <= rand[0] <= 0.25):
            q = makeNode(i, np.random.rand(3), 'r', '^')
        elif (0.25 < rand[0] <= 0.5):
            q = makeNode(i, np.random.rand(3), 'b', 'o')
        elif (0.5 < rand[0] <= 0.75):
            q = makeNode(i, np.random.rand(3), 'g', 'v')
        elif (0.75 < rand[0]):
            q = makeNode(i, np.random.rand(3), 'w', 'o')

        if (0 < i < maxNodes-1):
            if (rand[1] <= 0.2):
                dConnect(q, getNode(q.count-1))
            elif (rand[1] < 0.5):
                sConnect(q, getNode(q.count-1))

# class structure for Node class
class Node(str):
    value = None
    location = None
    assocs = None
    count = 0
    color = None
    marker = None

    # initiate node
    def __init__(self, val):
        self.value = val
        global numNodes
        numNodes += 1
        self.count = numNodes
        self.assocs = []
        self.color = 'b'
        self.marker = '^'

    # set node location and setup 3D text label
    def setLoc(self, coords):
        self.location = coords
        global labelsOn
        if labelsOn:
            ax.text(self.location[0], self.location[1], self.location[2], self.value, color=fontColor)

    # define node style
    def setStyle(self, color, marker):
        self.color = color
        self.marker = marker

    # define new association
    def addAssoc(self, newAssociation):
        self.assocs.append(newAssociation.count)
        if debug:
            print("  Informing node association:   Node {} ->  Node {}".format(self.value, newAssociation.value))




## MAIN PROGRAM

initPlot()

test()

plotNodes()

defineAxis()

plt.show()