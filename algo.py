import Node
import Config
import Tree

def update_tree(node: Node.Node, tree: Tree.Tree, best_buf_scen: list) -> None:
        links = node.GetChildren()

        for link in links.copy():
                update_tree(link, tree, best_buf_scen)

        if node.GetType() == Node.NodeType.Wire:
                assert best_buf_scen

                if best_buf_scen[0]:
                        tree.InsertBufferBeforeNode(node)
                        if node.GetParent().GetParent().GetType() != Node.NodeType.Wire:
                                tree.InsertNullWireBeforeNode(node.GetParent())
                
                best_buf_scen.pop(0)

def choose_best_scen(scouted: list) -> dict:
        max_rat = -float('inf')
        best_scen = None

        for scenario in scouted:
                if scenario['rat'] > max_rat:
                        max_rat = scenario['rat']
                        best_scen = scenario

        return best_scen

def scout_tree(node: Node.Node) -> list:
        links = node.GetChildren()

        if node.GetType() == Node.NodeType.Sink:
                assert len(links) == 0

                scouted = [{
                        'buf': [],
                        'cap': node.GetCapacitance(),
                        'rat': node.GetRat(),
                }]

        elif node.GetType() == Node.NodeType.Wire:
                assert len(links) == 1

                scouted = scout_tree(links[0])
                add_wire(scouted, 0 if node.IsNull() else 1)
                add_candidate(scouted)

        elif node.GetType() == Node.NodeType.Steiner:
                assert len(links) > 1

                scouted = []
                for link in links:
                        if scouted:
                                scouted = merge_scouted(scouted, scout_tree(link))
                        else:
                                scouted = scout_tree(link)

        else: # Driver
                assert len(links) == 1

                scouted = scout_tree(links[0])
                add_driver(scouted)
        
        return scouted

def add_wire(scouted: list, wire_len: int) -> None:
        for scenario in scouted:
                scenario['cap'] = endwire_cap(scenario['cap'], wire_len)
                scenario['rat'] = endwire_rat(scenario['cap'], wire_len,
                                              scenario['rat'])

def add_candidate(scouted: list) -> None:
        for i in range(len(scouted)):
                scouted.append({
                        'buf': scouted[i]['buf'].copy() + [True],
                        'cap': Config.GetDriverCapacitance('buf1x'),
                        'rat': endbuf_rat(scouted[i]['cap'], scouted[i]['rat'])
                })
                scouted[i]['buf'].append(False)

        prune_scouted(scouted)

def add_driver(scouted: list) -> None:
        for scenario in scouted:
                scenario['cap'] = Config.GetDriverCapacitance('buf1x')
                scenario['rat'] = endbuf_rat(scenario['cap'], scenario['rat'])

def endwire_cap(load_cap: float, wire_len: int) -> float:
        assert wire_len in (0, 1)
        return load_cap + float(wire_len) * Config.GetWireCapacitance()

def endwire_rat(load_cap: float, wire_len: int, load_rat: float) -> float:
        assert wire_len in (0, 1)
        return (load_rat - ((Config.GetWireCapacitance() * Config.GetWireResistance() *
                             (float(wire_len)**2) / 2) +
                             float(wire_len) * load_cap * Config.GetWireResistance()))

def endbuf_rat(load_cap: float, load_rat: float) -> float:
        return load_rat - (Config.GetDriverDelay('buf1x') + Config.GetDriverResistance('buf1x') * load_cap)

def merge_scouted(scouted_1: list, scouted_2: list) -> list:
        scouted = []
        for scenario_1 in scouted_1:
                for scenario_2 in scouted_2:
                        buf_1, buf_2 = scenario_1['buf'], scenario_2['buf']
                        cap_1, cap_2 = scenario_1['cap'], scenario_2['cap']
                        rat_1, rat_2 = scenario_1['rat'], scenario_2['rat']

                        scouted.append({
                                'buf': buf_1 + buf_2,
                                'cap': cap_1 + cap_2,
                                'rat': min(rat_1, rat_2),
                        })

        prune_scouted(scouted)
        return scouted
        
def prune_scouted(scouted: list) -> None:
        i = 0
        while i < len(scouted):
                pivot = scouted[i]
                pivot_out = False

                j = i + 1
                while j < len(scouted):
                        candidate = scouted[j]
                        if (pivot['cap'] <= candidate['cap'] and
                            pivot['rat'] >= candidate['rat']):
                                scouted.pop(j)
                        elif (pivot['cap'] >= candidate['cap'] and
                              pivot['rat'] <= candidate['rat']):
                                scouted.pop(i)
                                pivot_out = True
                                break
                        else:
                                j += 1

                if not pivot_out:
                        i += 1
