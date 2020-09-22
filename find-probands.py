import sys
import numpy as np
import pandas as pd
from argparse import ArgumentParser

def status(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

parser = ArgumentParser("fild-probands.py - filter all individuals with no children")
parser.add_argument("genealogy", help="Genealogy file")
parser.add_argument("output", help="Output file")
parser.add_argument("--year", "-y", default=None, help="Remove individuals before this year")
parser.add_argument("--delimiter", "-d", default=None, help="Delimiter for genealogy")

args = parser.parse_args()

status(f"Reading input genealogy {args.genealogy}...")
ped = pd.read_table(args.genealogy, delimiter=args.delimiter)

status("Finding probands...")
everyone = set(ped.ind)
fathers  = set(ped.father)
mothers  = set(ped.mother)
probands = everyone.difference(mothers.union(fathers))
status(f"Found {len(probands)} probands...")

if args.year is not None:
    pass

status(f"Writing output to {args.output}...")
np.savetxt(args.output, np.array(list(probands)), fmt="%d")

status("Done")
