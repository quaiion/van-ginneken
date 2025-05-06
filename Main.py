from Parser import ParseInputData
from Generator import GenerateCustomJson

if __name__ == '__main__':
    tree = ParseInputData(techFilePath='tech1.json', netFilePath='test10.json')
    GenerateCustomJson('out.json', tree)