import algo
import Parser
import Generator
import argparse

def run_van_gin(src_file: str, tech_file: str) -> None:
        tree = Parser.ParseInputData(techFilePath=tech_file, netFilePath=src_file)
        # tree.VisualizeTree('before.png')

        scouted = algo.scout_tree(tree.root)
        best_scen = algo.choose_best_scen(scouted)
        algo.update_tree(tree.root, tree, best_scen['buf'])
        # tree.VisualizeTree('after.png')

        Generator.GenerateOutputJson(src_file[:-5] + '_out.json', tree)

def main():
        argparser = argparse.ArgumentParser()
        argparser.add_argument('tech')
        argparser.add_argument('src')
        args = argparser.parse_args()

        run_van_gin(args.src, args.tech)


main()
