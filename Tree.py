from Node import Node
from Node import NodeType
from Node import ParseNodeType

from graphviz import Digraph

class Tree:
    root : Node
    nodeList : list[Node]

    def __init__(self, rootNode):
        self.root = rootNode
        self.nodeList = [rootNode]

    def AddNodeWithNoId(self, parentId : int, node : Node):
        nodeIds = [item.id for item in self.nodeList]
        node.id = max(nodeIds) + 1
        
        self.AddNode(parentId, node)

    def AddNode(self, parentId : int, node : Node):
        # Check for the same ID
        for item in self.nodeList:
            if item.id == node.id:
                raise Exception("In tree item with id = ", node.id, "already exists")

        parent = self.GetNodeById(parentId)
        parent.AddChild(node)
        node.SetParent(parent)
        self.nodeList.append(node)
        
    # Изымет ноду, передав детей своему родителю
    def EjectNode(self, id : int):
        ejectingNode = self.GetNodeById(id)

        itemParent = ejectingNode.parent
        itemChildren = ejectingNode.children
    
        # Удаляем у родителя ребёнка
        itemParent.RemoveChild(id)
        # Передаём родителю всех детей удалённого ребёнка
        for itemChild in itemChildren:
            itemParent.AddChild(itemChild)
            # Меняем родителей всех детей
            itemChild.SetParent(itemParent)
                
        self.nodeList = [x for x in self.nodeList if x.id != id]
    
    # Изымет ноду и всех детей
    def RemoveNode(self, id : int):
        node = self.GetNodeById(id)
        childList = node.GetChildren()
        
        for item in childList:
            self.RemoveNode(item.id)

        self.EjectNode(id)
        
    def InsertNode(self, node : Node, ParentNodeId : int, ChildrenNodeId : int):
        # Проверка на родственников
        child = self.GetNodeById(ChildrenNodeId)
        if child.GetParent().id != ParentNodeId:
            raise Exception("Parent with id = ", ParentNodeId, " and child with id = ", ChildrenNodeId, " are not relatives")

        # Прикрепим ноду к родителю
        self.AddNode(ParentNodeId, node)
        
        # Передадим ребёнка новому родителю
        child.SetParent(node)
        node.AddChild(child)

        # Заберём ребёнка у старого родителя
        oldParent = self.GetNodeById(ParentNodeId)
        oldParent.RemoveChild(ChildrenNodeId)

    def InsertNodeWithNoId(self, node, ParentNodeId : int, ChildrenNodeId : int):
        nodeIds = [item.id for item in self.nodeList]
        node.id = max(nodeIds) + 1

        self.InsertNode(node, ParentNodeId, ChildrenNodeId)

    def GetNodeById(self, nodeId : int) -> Node:
        for item in self.nodeList:
            if item.id == nodeId:
                return item
            
        raise Exception("No item with id = ", nodeId)

    def printNode(self, node : Node):
        parentId = None
        if (node.parent != None):
            parentId = node.parent.id
        print("NodeId = ", node.id, "ParentId = ", parentId)
        
        childList = node.GetChildren()
        for item in childList:
            self.printNode(item)

    def PrintTree(self):
        self.printNode(self.root)
    
    def VisualizeTree(self):
        dot = Digraph(comment="N-ary Tree", format="pdf")  # Можно выбрать формат: pdf, svg, png и т.д.

        # Рекурсивное добавление узлов и связей
        def add_nodes_edges(node : Node):
            if node:
                if node.nodeType == NodeType.Driver:
                    dot.node(str(node.id), "NodeId = " + str(node.id) + "\ntype: " + ParseNodeType(node.nodeType) + '\n (x, y) = (' + str(node.x) + ', ' + str(node.y) + ')')
                if node.nodeType == NodeType.Sink:
                    dot.node(str(node.id), "NodeId = " + str(node.id) + "\ntype: " + ParseNodeType(node.nodeType) + '\n (x, y) = (' + str(node.x) + ', ' + str(node.y) + ')' + '\ncapacitance = ' + str(node.capacitance) + '\nrot = ' + str(node.rat))
                if node.nodeType == NodeType.Wire:
                    dot.node(str(node.id), "NodeId = " + str(node.id) + '\n (x0, y0) = (' + str(node.x) + ', ' + str(node.y) + ')' + '\n (x1, y1) = (' + str(node.xEnd) + ', ' + str(node.yEnd) + ')' + '\nIsNull = ' + str(node.IsNull()))
                if node.nodeType == NodeType.Steiner:
                    dot.node(str(node.id), "NodeId = " + str(node.id) + "\ntype: " + ParseNodeType(node.nodeType) + '\n (x, y) = (' + str(node.x) + ', ' + str(node.y) + ')')
                for child in node.children:
                    dot.edge(str(node.id), str(child.id))
                    add_nodes_edges(child)

        add_nodes_edges(self.root)
        dot.render("n_ary_tree", view=True)  # Сохраняет файл и открывает его

# TODO: insert buffer before node
# TODO: insert null-wire before node

# rootNode = Node(0, 0, 0, "test", NodeType.Empty)
# tree = Tree(rootNode)

# node1 = Node(1, 0, 0, "test", NodeType.Empty)
# node2 = Node(2, 0, 0, "test", NodeType.Empty)
# node3 = Node(10, 0, 0, "test", NodeType.Empty)
# node4 = Node(4, 0, 0, "test", NodeType.Empty)
# node5 = Node(16, 0, 0, "test", NodeType.Empty)
# tree.AddNode(0, node1)
# tree.AddNode(0, node2)
# tree.AddNode(1, node3)
# tree.AddNode(1, node4)
# tree.InsertNodeWithNoId(node5, 1, 10)

# tree.VisualizeTree()