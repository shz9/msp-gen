import msprime
import numpy as np
import sys
from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime

def status(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

parser = ArgumentParser("msp_sim_gen.py")
parser.add_argument("genealogy", help="Genealogy file")
parser.add_argument("output_dir", type=Path, help="Output directory for tree sequences")
parser.add_argument("--prefix", "-a", default="", help="Prefix for output files for batch runs")

parser.add_argument("--proband-file", "-p", default=None, help="List of probands")
parser.add_argument("--length", "-l", default=1, type=int, help="Length of chromosome in basepairs")
parser.add_argument("--recomb-rate", "-r", default=0, type=float, help="Recombination rate per base pair per generation")
parser.add_argument("--replicates", "-n", type=int, default=1, help="Number of replicate simulations")
parser.add_argument("--no-provenance", action="store_true", help="Do not record additional info")

args = parser.parse_args()

clock_start = datetime.now()
status(f"Started at {clock_start}")

if not  args.output_dir.exists():
    status(f"Creating {args.output_dir}...")
    args.output_dir.mkdir()

status("Reading pedigree file...")
ped = msprime.Pedigree.read_txt(args.genealogy)
status(f"Read pedigree with {ped.num_individuals} individuals...")

if args.proband_file:
    status(f"Using proband file {args.proband_file}...")
    proband_ID = np.loadtxt(args.proband_file, dtype=int)
    sample_size = len(proband_ID)    
    ped.set_samples(sample_IDs=proband_ID, probands_only=True)
else:
    status(f"Finding probands...")
    proband_idx = ped.get_proband_indices()
    sample_size = len(proband_idx)
    ped.set_samples(num_samples=sample_size)
status(f"Using {sample_size} probands...")

t = int(max(ped.time))

replicates = msprime.simulate(sample_size,
                              pedigree=ped,
                              model='wf_ped',
                              end_time=t,
                              length=args.length,
                              recombination_rate=args.recomb_rate,
                              num_replicates=args.replicates,
                              record_provenance=not args.no_provenance)

status(f"Simulating {args.replicates} replicates...")
for i, ts in enumerate(replicates, 1):
    outfile = f"{args.output_dir}/replicate_{args.prefix}_{i:04}.ts"
    ts.dump(outfile)
    status(i, end=" ")

clock_stop = datetime.now()
status(f"\nDone at {clock_stop}")
status(f"Took {clock_stop - clock_start}")
