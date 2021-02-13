import msprime
import numpy as np
import sys
from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime


def status(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


parser = ArgumentParser("simulate.py")
parser.add_argument("genealogy", help="Genealogy file")
parser.add_argument("output_ts", type=Path, help="Output tree sequence file")
parser.add_argument("--proband-file", "-p", default=None, help="List of probands")
parser.add_argument(
    "--length", "-l", default=1000, type=int, help="Length of chromosome in base-pairs"
)
parser.add_argument(
    "--recomb-rate",
    "-r",
    default=0,
    type=float,
    help="Recombination rate per base-pair per generation",
)

args = parser.parse_args()

clock_start = datetime.now()
status(f"Started at {clock_start}")

status("Reading pedigree file...")
ped = msprime.Pedigree.read_txt(args.genealogy)
status(f"Read pedigree with {ped.num_individuals} individuals...")

if args.proband_file:
    status(f"Using proband file {args.proband_file}...")
    proband_ID = np.loadtxt(args.proband_file, dtype=int)
    sample_size = len(proband_ID)
    ped.set_samples(sample_IDs=proband_ID, probands_only=True)
else:
    status("Finding probands...")
    proband_idx = ped.get_proband_indices()
    sample_size = len(proband_idx)
    ped.set_samples(num_samples=sample_size)
status(f"Using {sample_size} probands...")

t = int(max(ped.time))

sim = msprime.simulate(
    sample_size,
    pedigree=ped,
    model="wf_ped",
    end_time=t,
    length=args.length,
    recombination_rate=args.recomb_rate,
    num_replicates=1
)

next(sim).dump(args.output_ts)

clock_stop = datetime.now()
status(f"Done at {clock_stop}")
status(f"Took {clock_stop - clock_start}")
