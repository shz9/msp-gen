import numpy as np
import pandas as pd
from argparse import ArgumentParser

parser = ArgumentParser("fild-probands.py - filter all individuals with no children")
parser.add_argument("genealogy", help="Genealogy file")
parser.add_argument("output", help="Output file")

args = parser.parse_args()

ped = pd.read_table(args.genealogy)

everyone = set(ped.ind)
fathers  = set(ped.father)
mothers  = set(ped.mother)

probands = everyone.difference(mothers.union(fathers))

np.savetxt(args.output, np.array(list(probands)), fmt="%d")
