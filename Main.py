from Parser import ParseInputData
from Generator import GenerateOutputJson

if __name__ == '__main__':
    tree = ParseInputData(techFilePath='tech1.json', netFilePath='test01.json')
    tree.VisualizeTree()
    GenerateOutputJson('out.json', tree)