import tskit
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("output_file")

args = parser.parse_args()

ts = tskit.load(args.input_file)

with open(args.output_file, "w") as output_vcf:
    ts.write_vcf(output_vcf, ploidy=2)
