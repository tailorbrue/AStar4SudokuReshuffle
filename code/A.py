import copy
from graphviz import Digraph

def makeSquare(node):
    return str(node.array2d[0]) + '\n' + str(node.array2d[1]) + '\n' + str(node.array2d[2])

def move(array2d, srcX, srcY, drcX, drcY):
    temp = array2d[srcX][srcY]
    array2d[srcX][srcY] = array2d[drcX][drcY]
    array2d[drcX][drcY] = temp
    return array2d

def getStatus(array2d):
    a=[]
    for x in range(0, 3):
        for y in range(0, 3):
            if array2d[x][y] != 0:
                a.append(array2d[x][y])
    ans = 0
    for i in range(len(a)):
        for j in range(i):
            if a[j] > a[i]:
                ans += 1
    return ans

class Node:
    def __init__(self, array2d, g=0, h=0):
        self.array2d = array2d
        self.father = None
        self.g = g
        self.h = h
    def setH(self, endNode):
        for x in range(0, 3):
            for y in range(0, 3):
                for m in range(0, 3):
                    for n in range(0, 3):
                        if self.array2d[x][y] == endNode.array2d[m][n]:
                            self.h += abs(x - m) + abs(y - n)

    def setG(self, g):
        self.g = g

    def setFather(self, node):
        self.father = node

    def getG(self):
        return self.g

class A:
    def __init__(self, startNode, endNode):
        self.openList = []
        self.closeList = []
        self.startNode = startNode
        self.endNode = endNode
        self.currentNode = startNode
        self.pathlist = []
        self.step = 0
        self.tree = Digraph('solving-tree', filename='solving-tree', format='png')
        self.tree.attr(label='Figure.1. Solving tree. Moving path is show with red boxes.', fontsize='70')
        return

    def getMinFNode(self):
        nodeTemp = self.openList[0]
        for node in self.openList:
            if node.g + node.h < nodeTemp.g + nodeTemp.h:
                nodeTemp = node
        return nodeTemp

    def nodeInOpenlist(self, node):
        for nodeTmp in self.openList:
            if nodeTmp.array2d == node.array2d:
                return True
        return False

    def nodeInCloselist(self, node):
        for nodeTmp in self.closeList:
            if nodeTmp.array2d == node.array2d:
                return True
        return False

    def endNodeInOpenList(self):
        for nodeTmp in self.openList:
            if nodeTmp.array2d == self.endNode.array2d:
                return True
        return False

    def getNodeFromOpenList(self, node):
        for nodeTmp in self.openList:
            if nodeTmp.array2d == node.array2d:
                return nodeTmp
        return None

    def searchOneNode(self, node):
        if self.nodeInCloselist(node):
            return
        gTemp = self.step

        if self.nodeInOpenlist(node) == False:
            node.setG(gTemp)
            node.setH(self.endNode)
            self.openList.append(node)
            node.father = self.currentNode
            self.tree.node(makeSquare(node))
            self.tree.edge(makeSquare(self.currentNode), makeSquare(node))
        else:
            nodeTmp = self.getNodeFromOpenList(node)
            if self.currentNode.g + gTemp < nodeTmp.g:
                nodeTmp.g = self.currentNode.g + gTemp
                nodeTmp.father = self.currentNode
                self.tree.node(makeSquare(nodeTmp))
                self.tree.edge(makeSquare(self.currentNode), makeSquare(nodeTmp))
        return

    def searchNear(self):
        x=0
        y=0
        flag = False
        for x in range(0, 3):
            for y in range(0, 3):
                if self.currentNode.array2d[x][y] == 0:
                    flag = True
                    break
            if flag == True:
                break
        self.step += 1
        if x - 1 >= 0:
            arrayTemp = move(copy.deepcopy(self.currentNode.array2d), x, y, x - 1, y)
            self.searchOneNode(Node(arrayTemp))
        if x + 1 < 3:
            arrayTemp = move(copy.deepcopy(self.currentNode.array2d), x, y, x + 1, y)
            self.searchOneNode(Node(arrayTemp))
        if y - 1 >= 0:
            arrayTemp = move(copy.deepcopy(self.currentNode.array2d), x, y, x, y - 1)
            self.searchOneNode(Node(arrayTemp))
        if y + 1 < 3:
            arrayTemp = move(copy.deepcopy(self.currentNode.array2d), x, y, x, y + 1)
            self.searchOneNode(Node(arrayTemp))
        return

    def start(self):
        
        startY = getStatus(self.startNode.array2d)
        endY = getStatus(self.endNode.array2d)

        if startY % 2 != endY % 2:
            return False

        self.startNode.setH(self.endNode)
        self.startNode.setG(self.step)
        self.openList.append(self.startNode)

        while True:

            self.currentNode = self.getMinFNode()
            self.closeList.append(self.currentNode)
            self.openList.remove(self.currentNode)
            self.step = self.currentNode.getG()
            self.searchNear()

            if self.endNodeInOpenList():
                nodeTmp = self.getNodeFromOpenList(self.endNode)
                while True:
                    self.pathlist.append(nodeTmp)
                    if nodeTmp.father != None:
                        nodeTmp = nodeTmp.father
                    else:
                        return True
            elif len(self.openList) == 0:
                return False
            elif self.step > 30:
                return False
        return True

    def labelPath(self):
        for node in self.pathlist[::-1]:
            self.tree.node(makeSquare(node), shape='box', color='red')

    def saveTree(self):
        self.tree.render(view=False)
