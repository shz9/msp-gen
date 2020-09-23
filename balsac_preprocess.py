import numpy as np
from argparse import ArgumentParser
import msprime

parser = ArgumentParser("balsac_preprocess.py")
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

table = np.genfromtxt(args.input, delimiter=",", skip_header=1, usecols=(0,1,2), dtype=int, filling_values=0)

individuals = set(table[:,0])
fathers = set(table[:,1])
mothers = set(table[:,2])
parents = fathers.union(mothers)
missing_parents = parents - individuals
missing_parents.remove(0)

extra_rows = np.array([(parent, 0, 0) for parent in missing_parents])

np.savetxt(args.output, np.row_stack([extra_rows, table]),
           fmt="%d", delimiter="\t", header="individual\tfather\tmother")
