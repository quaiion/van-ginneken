import json

from Tree import Tree
import Config as cfg
import Node 
import PathMaker as pathmaker

def ParseNetworkFile(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Парсинг узлов
        nodes = []
        for node in data['node']:
            node_info = {
                'id': node['id'],
                'x': node['x'],
                'y': node['y'],
                'type': node['type'],
                'name': node['name'],
                'capacitance': node.get('capacitance'),  # Опциональное поле
                'rat': node.get('rat')                   # Опциональное поле
            }
            nodes.append(node_info)
        
        # Парсинг рёбер
        edges = []
        for edge in data['edge']:
            edge_info = {
                'id': edge['id'],
                'vertices': edge['vertices'],
                'segments': edge['segments']
            }
            edges.append(edge_info)
        
        return {
            'nodes': nodes,
            'edges': edges
        }
        
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
        return None
    except json.JSONDecodeError:
        print("Ошибка: Некорректный формат JSON")
        return None
    except KeyError as e:
        print(f"Ошибка: Отсутствует обязательное поле {e} в JSON-структуре")
        return None

def GetNodeById(id, result):
    for item in result['nodes']:
        if item['id'] == id:
            if item['type'] == 's':
                return Node.NodeSteiner(id, item['x'], item['y'], item['name'])
            if item['type'] == 't':
                return Node.NodeSync(id, item['x'], item['y'], item['name'], item['capacitance'], item['rat'])

def FindChildren(nodeId : int, tree : Tree, parseResult):
    print('FindChildren, nodeId = ', nodeId)
    currNode = tree.GetNodeById(nodeId)
    children = []
    for item in parseResult['edges']:
        listVertices = item['vertices']
        if listVertices[0] == nodeId:
            if currNode.parent:
                if listVertices[1] != currNode.parent.id:
                    children.append(GetNodeById(listVertices[1], parseResult))
            else:
                children.append(GetNodeById(listVertices[1], parseResult))
        if listVertices[1] == nodeId:
            if currNode.parent:
                if listVertices[0] != currNode.parent.id:
                    children.append(GetNodeById(listVertices[0], parseResult))
            else:
                children.append(GetNodeById(listVertices[0], parseResult))
    
    for item in children:
        tree.AddNode(nodeId, item)
        FindChildren(item.id, tree, parseResult)

# Пример использования
if __name__ == "__main__":
    cfg.ParseConfig('tech1.json')
    result = ParseNetworkFile('test01.json')
    print(result['edges'])
    tree = None

    # Ищем buf1x node
    # bufName = cfg.DriverArr[0]['type']
    for item in result['nodes']:
        if item['type'] == 'b':
            rootNode = Node.NodeDriver(int(item['id']), int(item['x']), int(item['y']), str(item['name']))
            tree = Tree(rootNode)
    
    # Ищем связи всех нод
    rootId = tree.root.id
    FindChildren(rootId, tree, result)

    # Вставляем провода
    for item in result['edges']:
        vertices = item['vertices']
        segments = item['segments']
        
        wirePath = pathmaker.GetFullPath(segments)
        savedId = vertices[0]

        for i in range(len(wirePath) - 1):
            nodeWire = Node.NodeWire(0, wirePath[i][0], wirePath[i][1], wirePath[i + 1][0], wirePath[i + 1][1],)
            tree.InsertNodeWithNoId(nodeWire, savedId, vertices[1])
            savedId = nodeWire.id
            

            

    tree.VisualizeTree()
    

    