import numpy as np
import config.Config as cfg

class NodeType:
    Empty   = 0
    Wire    = 1
    Sync    = 2
    Steiner = 3 
    Driver  = 4

class Node:
    id : int
    x : int
    y : int
    name : str

    capacitance = float(0)
    resistance  = float(0)
    rat         = float(0)

    nodeType = NodeType.Empty

    parent = None
    children : list

    def __init__(self, id : int, x : int, y : int, name: str, type : NodeType):
        self.id = id
        self.x = x
        self.y = y
        self.name = name
        self.nodeType = type
        self.parent = None
        self.children = []

    def GetType(self):
        return self.nodeType

    def GetCapacitance(self):
        return self.capacitance
    
    def GetRat(self):
        return self.rat
    
    def SetParent(self, node):
        self.parent = node
    
    def AddChild(self, node):
        self.children.append(node)

    def GetParent(self):
        return self.parent
    
    def GetChildren(self):
        return self.children
    
    def RemoveChild(self, childId : int):
        self.children = [x for x in self.children if x.id != childId]
    

class NodeDriver(Node):
    def __init__(self, id : int, x : int, y : int, name : str):
        super().__init__(id, x, y, name, NodeType.Driver)
        super().capacitance = cfg.GetDriverCapacitance(name)
        super().resistance  = cfg.GetDriverResistance(name)
        super().rat         = cfg.GetDriverRat(name)

class NodeSteiner(Node):
    def __init__(self, id : int, x : int, y : int, name : str):
        super().__init__(id, x, y, name, NodeType.Steiner)

class NodeSync(Node):
    def __init__(self, id : int, x : int, y : int, name : str, capacitance : float, rat : float):
        super().__init__(id, x, y, name, NodeType.Sync)
        self.capacitance = capacitance
        self.rat = rat

class NodeWire(Node):
    def __init__(self, id, x, y):
        super().__init__(id, x, y, "w" + str(id), NodeType.Wire)
        super().capacitance = cfg.GetWireCapacitance()
        super().resistance  = cfg.GetWireResistance()
        super().rat         = cfg.GetWireRat()