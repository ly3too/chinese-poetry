from elasticsearch_dsl.connections import connections
import argparse
import glob
import os
import importlib
from importlib import machinery


def load_mod(file):
    print("loading: " + file)
    name = os.path.splitext(os.path.basename(file))[0]
    mod = importlib.import_module("." + name, "chinese-poetry")
    mod.do_es_import()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--connection", action='append', help='set es connections', required=True)
    parser.add_argument("-m", "--module", required=False, default="")

    args = parser.parse_args()
    print("args: {}".format(args))

    con = connections.create_connection(hosts=args.connection)

    cur_dir = os.path.dirname((os.path.abspath(__file__)))
    if not args.module:
        all_pys = glob.glob("{}/es_import_*.py".format(cur_dir))
    else:
        all_pys = [cur_dir + "/es_import_" + args.module + ".py"]

    for file in all_pys:
        load_mod(file)

