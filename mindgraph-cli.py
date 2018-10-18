from mindgraph.graph import read_yaml
from yaml import load
from yaml.scanner import ScannerError
import argparse


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--yaml-file", dest="files", help="one or more yaml files separated by comma",
                        required=True)
    return parser.parse_args()


def main():
    args = arg_parser()
    file_list = args.files.split(",")
    print("Reading the following files:")
    print(", ".join(file_list))
    for file in file_list:
        filename = file.strip() # Remove preceeding and trailing spaces if any
        try:
            # Validating yaml file using pyyaml simple load
            with open(filename, "r") as f:
                load(f)
        except ScannerError:
            print("ERROR: File {} is not a valid yaml. Ignoring.".format(filename))
        else:
            graph = read_yaml(filename)
            print("Graph output of {}:".format(filename))
            print(graph)


if __name__ == '__main__':
    main()

