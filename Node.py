import Config as cfg

class NodeType:
    Empty   = "Empty"
    Wire    = "Wire"
    Sink    = "Sink"
    Steiner = "Steiner"
    Driver  = "Driver"
    
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
        self.id = int(id)
        self.x = int(x)
        self.y = int(y)
        self.name = str(name)
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
        self.capacitance = cfg.GetDriverCapacitance(name)
        self.resistance  = cfg.GetDriverResistance(name)
        self.rat         = cfg.GetDriverDelay(name)

class NodeSteiner(Node):
    def __init__(self, id : int, x : int, y : int, name : str):
        super().__init__(id, x, y, name, NodeType.Steiner)

class NodeSync(Node):
    def __init__(self, id : int, x : int, y : int, name : str, capacitance : float, rat : float):
        super().__init__(id, x, y, name, NodeType.Sink)
        self.capacitance = capacitance
        self.rat = rat

class NodeWire(Node):
    xEnd : int
    yEnd : int
    def __init__(self, id, x, y, xEnd, yEnd):
        super().__init__(id, x, y, "w" + str(id), NodeType.Wire)
        self.capacitance = cfg.GetWireCapacitance()
        self.resistance  = cfg.GetWireResistance()
        self.rat         = cfg.GetWireRat()
        self.xEnd        = xEnd
        self.yEnd        = yEnd

    def IsNull(self):
        return (self.x == self.xEnd) and (self.y == self.yEnd)