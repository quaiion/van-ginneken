import matplotlib.pyplot as plt
from time import time
import Parser
import Generator
import algo

LBOUND  = 1
UBUOUND = 100
STEP    = 1

wire_lens = range(LBOUND, UBUOUND, STEP)

def run_dump_van_gin(src_file: str, dest_file: str) -> tuple:
        tree = Parser.ParseInputData(techFilePath='tech1.json', netFilePath=src_file)

        timestamp_1 = time()

        scouted = algo.scout_tree(tree.root)
        best_scen = algo.choose_best_scen(scouted)
        algo.update_tree(tree.root, tree, best_scen['buf'])

        timestamp_2 = time()

        Generator.GenerateOutputJson(dest_file, tree)

        return best_scen['rat'], timestamp_2 - timestamp_1

for wire_len in wire_lens:
        file = open('artifacts/' + str(wire_len) + '.json', 'w')
        file.write('{\n' +
                   '  "node": [\n' +
                   '    { "id": 0, "x": 0, "y": 0, "type": "b", "name": "buf1x" },\n' +
                   '    { "id": 1, "x": ' + str(wire_len) + ', "y": 0, "type": "t", "name": "z", "capacitance": 1.5, "rat": 10000.0 }\n' +
                   '  ],\n' +
                   '  "edge": [\n' +
                   '    { "id": 0, "vertices": [0, 1], "segments": [ [0, 0], [' + str(wire_len) + ', 0] ] }\n' +
                   '  ]\n' +
                   '}\n')
        file.close()

times, rats = [], []

for wire_len in wire_lens:
        rat, durat = run_dump_van_gin('artifacts/' + str(wire_len) + '.json', 'artifacts/' + str(wire_len) + '_out.json')
        times.append(durat * 1000)
        rats.append(10000.0 - rat)

fig, axes = plt.subplot_mosaic([['time'], ['rat']], dpi=200, figsize=(10, 8))
axes['time'].set_xlabel('initial wire length, um', loc='right', fontfamily='monospace')
axes['rat'].set_xlabel('initial wire length, um', loc='right', fontfamily='monospace')
axes['time'].set_ylabel('time consumed, ms', fontfamily='monospace')
axes['rat'].set_ylabel('min delay reached, ps', fontfamily='monospace')
axes['time'].grid()
axes['rat'].grid()

axes['time'].plot(wire_lens, times, '-r')
axes['rat'].plot(wire_lens, rats, '-g')

fig.savefig('stats.png', format='png')
