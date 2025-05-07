import algo
import Parser
import Generator
import argparse

def make_dest_name(src_file: str) -> str:
        term = src_file.rfind('\\')
        if term == -1:
                term = src_file.rfind('/')
                if term == -1:
                        term = 0
                else:
                        term += 1
        else:
                term += 1

        return src_file[term:-5] + '_out.json'

def run_van_gin(src_file: str, tech_file: str) -> None:
        tree = Parser.ParseInputData(techFilePath=tech_file, netFilePath=src_file)
        # tree.VisualizeTree('before.png')

        scouted = algo.scout_tree(tree.root)
        best_scen = algo.choose_best_scen(scouted)
        algo.update_tree(tree.root, tree, best_scen['buf'])
        # tree.VisualizeTree('after.png')

        Generator.GenerateOutputJson(make_dest_name(src_file), tree)

def main():
        argparser = argparse.ArgumentParser()
        argparser.add_argument('tech')
        argparser.add_argument('src')
        args = argparser.parse_args()

        run_van_gin(args.src, args.tech)


main()
