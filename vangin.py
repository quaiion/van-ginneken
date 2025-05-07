import algo
import Parser
import Generator
import argparse

def run_van_gin(src_file: str, dest_file: str) -> None:
        tree = Parser.ParseInputData(techFilePath='tech1.json', netFilePath=src_file)
        # tree.VisualizeTree('before.png')

        scouted = algo.scout_tree(tree.root)
        best_scen = algo.choose_best_scen(scouted)
        algo.update_tree(tree.root, tree, best_scen['buf'])
        # tree.VisualizeTree('after.png')

        Generator.GenerateOutputJson(dest_file, tree)

def main():
        argparser = argparse.ArgumentParser()
        argparser.add_argument('src')
        argparser.add_argument('dest')
        args = argparser.parse_args()

        run_van_gin(args.src, args.dest)


main()
