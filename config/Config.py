
import json

DriverArr = []
Wire = None

def ParseConfig(file_path : str):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            
        # Парсинг секции module
        modules = []
        for module in data['module']:
            mod_info = {
                'name': module['name'],
                'outputs': [],
                'inputs': []
            }
            
            # Обработка выходов
            for output in module['output']:
                mod_info['outputs'].append({
                    'name': output['name'],
                    'inverting': output['inverting']
                })
            
            # Обработка входов
            for input_port in module['input']:
                mod_info['inputs'].append({
                    'name': input_port['name'],
                    'capacitance': input_port['C'],
                    'resistance': input_port['R'],
                    'delay': input_port['intrinsic_delay']
                })
            
            modules.append(mod_info)
        
        # Парсинг секции technology
        technology = {
            'wire_resistance': data['technology']['unit_wire_resistance'],
            'wire_capacitance': data['technology']['unit_wire_capacitance'],
            'resistance_unit': data['technology']['unit_wire_resistance_comment0'].split()[0],
            'capacitance_unit': data['technology']['unit_wire_capacitance_comment0'].split()[0]
        }
        
        global DriverArr
        DriverArr = modules
        global Wire
        Wire = technology

        return {
            'modules': modules,
            'technology': technology
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

def GetDriverDescriptor(name : str):
    for item in DriverArr:
        if item['name'] == name:
            return item        
    raise Exception("Driver \"", name, "\" not found")

def GetDriverCapacitance(name : str):
    driver = GetDriverDescriptor(name)
    return driver['inputs'][0]['capacitance']

def GetDriverResistance(name : str):
    driver = GetDriverDescriptor(name)
    return driver['inputs'][0]['resistance']

def GetDriverDelay(name : str):
    driver = GetDriverDescriptor(name)
    return driver['inputs'][0]['delay']
    
def GetWireCapacitance():
    return Wire['wire_capacitance']

def GetWireResistance():
    return Wire['wire_resistance']

def GetWireRat():
    pass


ParseConfig("./tech1.json")
