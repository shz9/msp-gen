import msprime
import tskit
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("output_file")
parser.add_argument("-u", "--mutation_rate", default=1e-8, type=float)

args = parser.parse_args()

ts = tskit.load(args.input_file)

tsm = msprime.mutate(ts, rate=args.mutation_rate)

tsm.dump(args.output_file)
