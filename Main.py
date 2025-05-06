from Parser import ParseInputData
from Generator import GenerateCustomJson

if __name__ == '__main__':
    tree = ParseInputData()
    GenerateCustomJson('out.json', tree)