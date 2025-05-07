import json
from SegmentsMaker import RestoreKeyPoints
import Tree 
import Node

def GetNodeDataFromTree(tree):
    nodeData = []

    for item in tree.nodeList:
        if item:
            if item.nodeType == Node.NodeType.Driver:
                nodeData.append({
                    "id" : item.id,
                    "x"  : item.x,
                    "y"  : item.y,
                    "type" : "b",
                    "name" : item.name
                })
            if item.nodeType == Node.NodeType.Sink:
                nodeData.append({
                    "id" : item.id,
                    "x"  : item.x,
                    "y"  : item.y,
                    "type" : "t",
                    "name" : item.name,
                    "capacitance": item.GetCapacitance(),
                    "rat": item.GetRat()
                })
            if item.nodeType == Node.NodeType.Steiner:
                nodeData.append({
                    "id" : item.id,
                    "x"  : item.x,
                    "y"  : item.y,
                    "type" : "s",
                    "name" : item.name,
                })
    
    nodeData = sorted(nodeData, key = lambda x : x['id'])

    return nodeData

# start - начало провода
def GetEdgeToChild(edgeId : int, start : Node.Node):
    if start:
        pointList = []
        startId = start.parent.id
        node = start
    
        while True:
            pointList.append([node.x, node.y])
            if node.nodeType == Node.NodeType.Wire:
                node = node.GetChildren()[0] # инвариант провода
            else:
                break
            
        endId = node.id
    
        segments = RestoreKeyPoints(pointList)
    
        edges = [{
            "id" : edgeId,
            "vertices" : [startId, endId],
            "segments" : segments
        }]
    
        for child in node.children:
            edges += GetEdgeToChild(0, child)

        return edges
    else:
        return []

def GetEdgeDataFromTree(tree : Tree.Tree):
    edges = []
    for child in tree.root.children:
        edges += GetEdgeToChild(0, child)
    
    id = 0
    for item in edges:
        item['id'] = id
        id += 1
    return edges

def GenerateOutputJson(output_file, tree : Tree.Tree):
    # Создаем структуру данных
    nodeData = GetNodeDataFromTree(tree)

    edgeData = GetEdgeDataFromTree(tree)

    data = {
        "node": nodeData,
        "edge": edgeData
    }

    # Сохраняем в JSON файл с красивым форматированием
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

# Использование
# generate_custom_json("network_config.json")