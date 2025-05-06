from Parser import ParseInputData
from Generator import GenerateOutputJson

if __name__ == '__main__':
    tree = ParseInputData(techFilePath='tech1.json', netFilePath='test10.json')
    GenerateOutputJson('out.json', tree)